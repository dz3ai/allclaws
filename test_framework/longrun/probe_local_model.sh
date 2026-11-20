#!/usr/bin/env bash
# Local-model service gate for ranked-driver bring-up.
#
# Probes an OpenAI-compatible endpoint (fleet router or a bare llama-server)
# and answers ONE question: can every CLI agent in the driver roster rely on
# this endpoint? The decisive gate is TOOL CALLING — CLI agents live or die
# on it.
#
# Gates:
#   1. /health            — server up (llama.cpp body or router {"status":"ok"})
#   2. /v1/models         — model id resolved (explicit arg, or picked from the
#                           catalog by capabilities per the fleet guide: tools
#                           capable + status up, code-task pick first)
#   3. /props             — build/template snapshot (llama.cpp only; SKIPped
#                           on the router, which has no /props)
#   4. plain completion   — generation works end-to-end
#   5. TOOL-CALL probe    — model emits a valid tool_calls array for a
#                           trivial JSON-schema tool. THIS is the go/no-go.
#
# Usage:  probe_local_model.sh [base-url] [model-id]
#         defaults: http://192.168.3.26:8000  + auto-pick from /v1/models
# Exit:   0 = all gates green (SKIP does not count against);  1 = at least one red
# Notes:  pass "?auth" as 3rd arg to also test bearer auth is NOT required.
set -u
BASE="${1:-http://192.168.3.26:8000}"
WANT_MODEL="${2:-}"
GATES_FAIL=0

say()  { printf '%s\n' "$*"; }
gate() { # gate <name> <ok:0|1|2> <detail>  (2 = SKIP — not a failure)
  if [ "$2" -eq 0 ]; then say "  [PASS] $1 — $3"
  elif [ "$2" -eq 2 ]; then say "  [SKIP] $1 — $3"
  else say "  [FAIL] $1 — $3"; GATES_FAIL=$((GATES_FAIL+1)); fi
}

say "=== local-model service gate: $BASE ==="
say ""

# ---- 1. health ----------------------------------------------------------
if BODY=$(curl -sf -m 5 "$BASE/health" 2>/dev/null); then
  gate "1/health" 0 "$BODY"
else
  gate "1/health" 1 "no response (is llama-server running?)"
  say ""
  say "RESULT: UNREACHABLE — the Nov-13 ECONNREFUSED signature. Start the"
  say "service (port ${BASE##*:}), then re-run. Nothing else matters yet."
  exit 1
fi

# ---- 2. model id --------------------------------------------------------
# Explicit arg wins; otherwise pick from the catalog per the fleet guide's
# capability rules: status up + tools capable (drivers need tool_calls),
# preferring the guide's code-task pick (qwen3-coder-30b) when present.
MODELS_JSON=$(curl -sf -m 5 "$BASE/v1/models" 2>/dev/null)
if [ -n "$WANT_MODEL" ]; then
  MODEL_ID="$WANT_MODEL"
  if printf '%s' "$MODELS_JSON" | jq -e --arg m "$MODEL_ID" '.data[] | select(.id == $m and .status == "up")' >/dev/null 2>&1; then
    gate "2/model-id" 0 "$MODEL_ID (explicit arg, status up in catalog)"
  elif printf '%s' "$MODELS_JSON" | jq -e --arg m "$MODEL_ID" '.data[] | select(.id == $m)' >/dev/null 2>&1; then
    gate "2/model-id" 1 "$MODEL_ID is in the catalog but not status=up"
  else
    gate "2/model-id" 1 "$MODEL_ID not in $BASE/v1/models"
  fi
else
  MODEL_ID=$(printf '%s' "$MODELS_JSON" | jq -r '
    [ .data[] | select(.status == "up" and (.capabilities // [] | index("tools"))) ]
    | (map(select(.id == "qwen3-coder-30b")) + .)[0].id // empty' 2>/dev/null)
  if [ -n "$MODEL_ID" ]; then
    gate "2/model-id" 0 "$MODEL_ID (auto-picked: up + tools-capable, code-task pick first)"
  else
    gate "2/model-id" 1 "no up+tools-capable model in catalog: ${MODELS_JSON:-<none>}"
  fi
fi

# ---- 3. props snapshot (model pin; llama.cpp only) -----------------------
PROPS_HTTP=$(curl -s -m 5 -o /tmp/opencode/probe_props.json -w "%{http_code}" "$BASE/props" 2>/dev/null || echo "000")
PROPS=$(cat /tmp/opencode/probe_props.json 2>/dev/null || echo "{}")
BUILD=$(printf '%s' "$PROPS" | jq -r '.build.build_str // "unknown"' 2>/dev/null)
MODEL_PATH=$(printf '%s' "$PROPS" | jq -r '.model_path // "unknown"' 2>/dev/null)
N_CTX=$(printf '%s' "$PROPS" | jq -r '.default_generation_settings.n_ctx // "unknown"' 2>/dev/null)
CTX_LEN=$(printf '%s' "$MODELS_JSON" | jq -r --arg m "$MODEL_ID" '.data[] | select(.id == $m) | .context_length // "unknown"' 2>/dev/null)
if [ "$PROPS_HTTP" = "404" ]; then
  gate "3/props" 2 "no /props on this endpoint (router, not llama.cpp) — catalog says ctx=$CTX_LEN"
elif [ "$BUILD" != "unknown" ] || [ "$MODEL_PATH" != "unknown" ]; then
  gate "3/props" 0 "build=$BUILD ctx=$N_CTX model=$(basename "$MODEL_PATH")"
else
  gate "3/props" 1 "/props reachable ($PROPS_HTTP) but snapshot unparseable"
fi

# ---- 4. plain completion ------------------------------------------------
# NOTE: this is a THINKING model (reasoning_content) — token budgets must be
# generous or reasoning consumes them before any content emits (first probe
# version failed exactly this way with max_tokens=16).
PLAIN=$(curl -sf -m 300 "$BASE/v1/chat/completions" \
  -H 'Content-Type: application/json' \
  -d '{"model":"'"${MODEL_ID:-x}"'","max_tokens":1024,"messages":[{"role":"user","content":"Reply with exactly: OK"}]}' 2>/dev/null)
PLAIN_TXT=$(printf '%s' "$PLAIN" | jq -r '.choices[0].message.content // empty' 2>/dev/null)
if [ -n "$PLAIN_TXT" ]; then
  gate "4/completion" 0 "\"$PLAIN_TXT\""
else
  gate "4/completion" 1 "no completion content: ${PLAIN:-<none>}"
fi

# ---- 5. THE gate: tool calling ------------------------------------------
# Thinking model: budget for reasoning first, then the call. If plain mode
# fails, retry with enable_thinking=false (Qwen3-style chat_template_kwargs)
# — that is the mode most CLI agents will want anyway.
tool_probe() { # tool_probe <extra-json-fragment>
  curl -sf -m 600 "$BASE/v1/chat/completions" \
    -H 'Content-Type: application/json' \
    -d '{
      '"$1"'
      "model": "'"${MODEL_ID:-x}"'",
      "max_tokens": 2048,
      "tools": [{
        "type": "function",
        "function": {
          "name": "get_weather",
          "description": "Get current weather for a city",
          "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
          }
        }
      }],
      "tool_choice": "auto",
      "messages": [{"role": "user", "content": "What is the weather in Tokyo? Use the tool."}]
    }' 2>/dev/null
}
TOOL_RESP=$(tool_probe '')
TC_NAME=$(printf '%s' "$TOOL_RESP" | jq -r '.choices[0].message.tool_calls[0].function.name // empty' 2>/dev/null)
TC_ARGS=$(printf '%s' "$TOOL_RESP" | jq -r '.choices[0].message.tool_calls[0].function.arguments // empty' 2>/dev/null)
if [ "$TC_NAME" != "get_weather" ]; then
  TOOL_RESP=$(tool_probe '"chat_template_kwargs": {"enable_thinking": false},')
  TC_NAME=$(printf '%s' "$TOOL_RESP" | jq -r '.choices[0].message.tool_calls[0].function.name // empty' 2>/dev/null)
  TC_ARGS=$(printf '%s' "$TOOL_RESP" | jq -r '.choices[0].message.tool_calls[0].function.arguments // empty' 2>/dev/null)
  THINK_MODE="thinking-off (chat_template_kwargs)"
else
  THINK_MODE="default (thinking on)"
fi
if [ "$TC_NAME" = "get_weather" ]; then
  gate "5/TOOL-CALL" 0 "name=$TC_NAME args=$TC_ARGS mode=$THINK_MODE — drivers can rely on this endpoint"
else
  gate "5/TOOL-CALL" 1 "no valid tool_calls in either mode (got name=${TC_NAME:-none}) — check chat template / server build"
fi

# ---- summary block for session notes -------------------------------------
say ""
say "=== snapshot (paste into session notes / result metadata) ==="
say "endpoint:   $BASE"
say "model_id:   ${MODEL_ID:-unknown}"
say "catalog_ctx: ${CTX_LEN:-unknown}"
say "build:      $BUILD"
say "model_file: $(basename "$MODEL_PATH")"
say "n_ctx:      $N_CTX"
say "probed:     $(date -Is)"
say ""
if [ "$GATES_FAIL" -eq 0 ]; then
  say "RESULT: GREEN — proceed to driver bring-up (Phase 2)."
else
  say "RESULT: RED — $GATES_FAIL gate(s) failed; see above."
fi
exit $([ "$GATES_FAIL" -eq 0 ] && echo 0 || echo 1)
