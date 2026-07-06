#!/usr/bin/env python3
"""
MCP Token Overhead Measurement — Static Reconstruction

Reconstructs what each platform sends to the LLM API for MCP tool schemas,
then counts tokens to measure the actual overhead of each approach.

Platforms measured:
- Hermes (baseline): Full schemas, unmodified
- ZeroClaw (eager): Full schemas (same as baseline)
- ZeroClaw (deferred): Stubs (name+desc) + tool_search definition
- GoClaw (eager): Full schemas (same as baseline)
- GoClaw (search): mcp_tool_search definition replaces all MCP tools
- Reasonix (raw): Full schemas, unmodified (same as baseline)
- Reasonix (canonicalized): Schemas with sorted keys + sorted required arrays

MCP servers (representative set from official @modelcontextprotocol/servers):
- filesystem (8 tools): read_file, write_file, edit_file, list_directory, ...
- github (11 tools): create_issue, get_issue, list_repos, create_pull_request, ...
- postgres (7 tools): query, list_tables, describe_table, ...
- brave-search (3 tools): search, fetch, ...
- slack (8 tools): post_message, list_channels, ...
- sqlite (4 tools): query, execute, list_tables, describe_table
- memory (5 tools): create_entity, create_relation, query, ...
- fetch (1 tool): fetch
- puppeteer (7 tools): navigate, click, fill, evaluate, screenshot, ...
- time (2 tools): get_time, convert_time
"""

import json
import copy
import sys

try:
    import tiktoken
except ImportError:
    print("pip install tiktoken", file=sys.stderr)
    sys.exit(1)

# ============================================================
# Representative MCP Tool Definitions
# Based on official @modelcontextprotocol/servers schemas
# ============================================================

def make_tool(name, description, properties, required=None):
    """Build a tool definition matching MCP tools/list response format."""
    return {
        "name": name,
        "description": description,
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": required or [],
        },
    }


# --- Server 1: filesystem (8 tools) ---
SERVER_FILESYSTEM = [
    make_tool("read_file", "Read the complete contents of a file from the file system.", {
        "path": {"type": "string", "description": "The absolute path to the file to read"},
    }, ["path"]),
    make_tool("write_file", "Create a new file or completely overwrite an existing file.", {
        "path": {"type": "string", "description": "The absolute path to the file to write"},
        "content": {"type": "string", "description": "The content to write to the file"},
    }, ["path", "content"]),
    make_tool("edit_file", "Make line-based edits to a text file with preview.", {
        "path": {"type": "string", "description": "The absolute path to the file to edit"},
        "edits": {"type": "array", "items": {"type": "object", "properties": {
            "oldText": {"type": "string", "description": "Text to search for"},
            "newText": {"type": "string", "description": "Text to replace with"},
        }}, "description": "List of edits to apply"},
        "dryRun": {"type": "boolean", "description": "Preview changes without applying"},
    }, ["path", "edits"]),
    make_tool("list_directory", "Get a detailed listing of all files and directories.", {
        "path": {"type": "string", "description": "The absolute path to the directory to list"},
    }, ["path"]),
    make_tool("create_directory", "Create a new directory or ensure one exists.", {
        "path": {"type": "string", "description": "The absolute path to the directory to create"},
    }, ["path"]),
    make_tool("move_file", "Move or rename a file or directory.", {
        "source": {"type": "string", "description": "The source path"},
        "destination": {"type": "string", "description": "The destination path"},
    }, ["source", "destination"]),
    make_tool("search_files", "Recursively search for files matching a pattern.", {
        "path": {"type": "string", "description": "The starting path"},
        "pattern": {"type": "string", "description": "Glob pattern to match"},
    }, ["path", "pattern"]),
    make_tool("get_file_info", "Get detailed metadata about a file or directory.", {
        "path": {"type": "string", "description": "The absolute path"},
    }, ["path"]),
]

# --- Server 2: github (11 tools) ---
SERVER_GITHUB = [
    make_tool("create_issue", "Create a new issue in a GitHub repository.", {
        "owner": {"type": "string", "description": "Repository owner"},
        "repo": {"type": "string", "description": "Repository name"},
        "title": {"type": "string", "description": "Issue title"},
        "body": {"type": "string", "description": "Issue body"},
        "labels": {"type": "array", "items": {"type": "string"}, "description": "Labels to add"},
        "assignees": {"type": "array", "items": {"type": "string"}, "description": "Users to assign"},
    }, ["owner", "repo", "title"]),
    make_tool("get_issue", "Get details of a specific issue.", {
        "owner": {"type": "string", "description": "Repository owner"},
        "repo": {"type": "string", "description": "Repository name"},
        "issue_number": {"type": "integer", "description": "Issue number"},
    }, ["owner", "repo", "issue_number"]),
    make_tool("list_issues", "List issues in a repository with filtering.", {
        "owner": {"type": "string", "description": "Repository owner"},
        "repo": {"type": "string", "description": "Repository name"},
        "state": {"type": "string", "enum": ["open", "closed", "all"], "description": "Filter by state"},
        "labels": {"type": "string", "description": "Comma-separated labels"},
        "sort": {"type": "string", "enum": ["created", "updated", "comments"], "description": "Sort order"},
        "direction": {"type": "string", "enum": ["asc", "desc"], "description": "Sort direction"},
        "per_page": {"type": "integer", "description": "Results per page (max 100)"},
        "page": {"type": "integer", "description": "Page number"},
    }, ["owner", "repo"]),
    make_tool("create_pull_request", "Create a new pull request.", {
        "owner": {"type": "string", "description": "Repository owner"},
        "repo": {"type": "string", "description": "Repository name"},
        "title": {"type": "string", "description": "PR title"},
        "head": {"type": "string", "description": "The name of the source branch"},
        "base": {"type": "string", "description": "The name of the target branch"},
        "body": {"type": "string", "description": "PR body"},
        "draft": {"type": "boolean", "description": "Create as draft"},
    }, ["owner", "repo", "title", "head", "base"]),
    make_tool("merge_pull_request", "Merge a pull request.", {
        "owner": {"type": "string", "description": "Repository owner"},
        "repo": {"type": "string", "description": "Repository name"},
        "pull_number": {"type": "integer", "description": "PR number"},
        "commit_title": {"type": "string", "description": "Merge commit title"},
        "merge_method": {"type": "string", "enum": ["merge", "squash", "rebase"], "description": "Merge method"},
    }, ["owner", "repo", "pull_number"]),
    make_tool("create_branch", "Create a new branch in a repository.", {
        "owner": {"type": "string", "description": "Repository owner"},
        "repo": {"type": "string", "description": "Repository name"},
        "branch": {"type": "string", "description": "New branch name"},
        "from_branch": {"type": "string", "description": "Source branch (default: repo default)"},
    }, ["owner", "repo", "branch"]),
    make_tool("get_file_contents", "Get the contents of a file or directory.", {
        "owner": {"type": "string", "description": "Repository owner"},
        "repo": {"type": "string", "description": "Repository name"},
        "path": {"type": "string", "description": "File path"},
        "branch": {"type": "string", "description": "Branch name"},
    }, ["owner", "repo", "path"]),
    make_tool("list_commits", "List commits on a repository branch.", {
        "owner": {"type": "string", "description": "Repository owner"},
        "repo": {"type": "string", "description": "Repository name"},
        "sha": {"type": "string", "description": "SHA or branch name"},
        "per_page": {"type": "integer", "description": "Results per page"},
        "page": {"type": "integer", "description": "Page number"},
    }, ["owner", "repo"]),
    make_tool("add_issue_comment", "Add a comment to an issue.", {
        "owner": {"type": "string", "description": "Repository owner"},
        "repo": {"type": "string", "description": "Repository name"},
        "issue_number": {"type": "integer", "description": "Issue number"},
        "body": {"type": "string", "description": "Comment body"},
    }, ["owner", "repo", "issue_number", "body"]),
    make_tool("get_me", "Get details of the authenticated user.", {}, []),
    make_tool("search_repositories", "Search for repositories on GitHub.", {
        "query": {"type": "string", "description": "Search query"},
        "sort": {"type": "string", "enum": ["stars", "forks", "updated"], "description": "Sort field"},
        "order": {"type": "string", "enum": ["asc", "desc"], "description": "Sort direction"},
        "per_page": {"type": "integer", "description": "Results per page"},
    }, ["query"]),
]

# --- Server 3: postgres (7 tools) ---
SERVER_POSTGRES = [
    make_tool("query", "Execute a read-only SQL query.", {
        "sql": {"type": "string", "description": "SQL query to execute"},
    }, ["sql"]),
    make_tool("execute", "Execute a write SQL statement.", {
        "sql": {"type": "string", "description": "SQL statement to execute"},
    }, ["sql"]),
    make_tool("list_tables", "List all tables in the database.", {
        "schema": {"type": "string", "description": "Schema name (default: public)"},
    }, []),
    make_tool("describe_table", "Get column details for a table.", {
        "table": {"type": "string", "description": "Table name"},
        "schema": {"type": "string", "description": "Schema name (default: public)"},
    }, ["table"]),
    make_tool("list_schemas", "List all schemas in the database.", {}, []),
    make_tool("get_constraints", "Get constraints for a table.", {
        "table": {"type": "string", "description": "Table name"},
        "schema": {"type": "string", "description": "Schema name"},
    }, ["table"]),
    make_tool("get_indexes", "Get indexes for a table.", {
        "table": {"type": "string", "description": "Table name"},
        "schema": {"type": "string", "description": "Schema name"},
    }, ["table"]),
]

# --- Server 4: brave-search (3 tools) ---
SERVER_BRAVE = [
    make_tool("brave_web_search", "Search the web using Brave Search.", {
        "query": {"type": "string", "description": "Search query"},
        "count": {"type": "integer", "description": "Number of results (max 20)"},
        "offset": {"type": "integer", "description": "Pagination offset"},
    }, ["query"]),
    make_tool("brave_local_search", "Search for local businesses using Brave.", {
        "query": {"type": "string", "description": "Local search query"},
        "count": {"type": "integer", "description": "Number of results"},
    }, ["query"]),
    make_tool("brave_fetch", "Fetch content from a URL.", {
        "url": {"type": "string", "description": "URL to fetch"},
    }, ["url"]),
]

# --- Server 5: slack (8 tools) ---
SERVER_SLACK = [
    make_tool("post_message", "Post a message to a Slack channel.", {
        "channel": {"type": "string", "description": "Channel ID or name"},
        "text": {"type": "string", "description": "Message text"},
        "blocks": {"type": "array", "items": {"type": "object"}, "description": "Slack blocks"},
        "thread_ts": {"type": "string", "description": "Thread timestamp to reply to"},
    }, ["channel", "text"]),
    make_tool("list_channels", "List all channels in the workspace.", {
        "types": {"type": "string", "description": "Channel types (public_channel, private_channel)"},
        "limit": {"type": "integer", "description": "Max results"},
    }, []),
    make_tool("get_channel_history", "Get message history for a channel.", {
        "channel": {"type": "string", "description": "Channel ID"},
        "limit": {"type": "integer", "description": "Number of messages"},
        "cursor": {"type": "string", "description": "Pagination cursor"},
    }, ["channel"]),
    make_tool("reply_thread", "Reply to a thread.", {
        "channel": {"type": "string", "description": "Channel ID"},
        "thread_ts": {"type": "string", "description": "Thread timestamp"},
        "text": {"type": "string", "description": "Reply text"},
    }, ["channel", "thread_ts", "text"]),
    make_tool("upload_file", "Upload a file to a channel.", {
        "channels": {"type": "array", "items": {"type": "string"}, "description": "Channel IDs"},
        "filename": {"type": "string", "description": "File name"},
        "title": {"type": "string", "description": "File title"},
        "initial_comment": {"type": "string", "description": "Initial comment"},
        "content": {"type": "string", "description": "File content (text files)"},
    }, ["channels", "filename"]),
    make_tool("search_messages", "Search messages in the workspace.", {
        "query": {"type": "string", "description": "Search query"},
        "count": {"type": "integer", "description": "Results per page"},
        "page": {"type": "integer", "description": "Page number"},
    }, ["query"]),
    make_tool("create_channel", "Create a new channel.", {
        "name": {"type": "string", "description": "Channel name"},
        "is_private": {"type": "boolean", "description": "Whether channel is private"},
    }, ["name"]),
    make_tool("get_user_info", "Get info about a user.", {
        "user": {"type": "string", "description": "User ID"},
    }, ["user"]),
]

# --- Server 6: sqlite (4 tools) ---
SERVER_SQLITE = [
    make_tool("query", "Execute a read-only SQL query on SQLite.", {
        "sql": {"type": "string", "description": "SQL query to execute"},
    }, ["sql"]),
    make_tool("execute", "Execute a write SQL statement on SQLite.", {
        "sql": {"type": "string", "description": "SQL statement to execute"},
    }, ["sql"]),
    make_tool("list_tables", "List all tables in the SQLite database.", {}, []),
    make_tool("describe_table", "Describe a SQLite table schema.", {
        "table": {"type": "string", "description": "Table name"},
    }, ["table"]),
]

# --- Server 7: memory (5 tools) ---
SERVER_MEMORY = [
    make_tool("create_entities", "Create new entities in the memory knowledge graph.", {
        "entities": {"type": "array", "items": {"type": "object", "properties": {
            "name": {"type": "string", "description": "Entity name"},
            "entityType": {"type": "string", "description": "Entity type"},
            "observations": {"type": "array", "items": {"type": "string"}, "description": "Entity observations"},
        }}, "description": "Entities to create"},
    }, ["entities"]),
    make_tool("create_relations", "Create relations between entities.", {
        "relations": {"type": "array", "items": {"type": "object", "properties": {
            "from": {"type": "string", "description": "Source entity name"},
            "to": {"type": "string", "description": "Target entity name"},
            "relationType": {"type": "string", "description": "Relation type"},
        }}, "description": "Relations to create"},
    }, ["relations"]),
    make_tool("add_observations", "Add observations to existing entities.", {
        "entityName": {"type": "string", "description": "Entity name"},
        "observations": {"type": "array", "items": {"type": "string"}, "description": "Observations to add"},
    }, ["entityName", "observations"]),
    make_tool("search_nodes", "Search the memory knowledge graph.", {
        "query": {"type": "string", "description": "Search query"},
    }, ["query"]),
    make_tool("delete_entities", "Delete entities from the knowledge graph.", {
        "entityNames": {"type": "array", "items": {"type": "string"}, "description": "Entity names to delete"},
    }, ["entityNames"]),
]

# --- Server 8: fetch (1 tool) ---
SERVER_FETCH = [
    make_tool("fetch", "Fetch content from a URL and optionally extract as markdown.", {
        "url": {"type": "string", "description": "URL to fetch"},
        "max_length": {"type": "integer", "description": "Max content length in chars (default 5000)"},
        "start_index": {"type": "integer", "description": "Start offset for pagination"},
        "raw": {"type": "boolean", "description": "Return raw HTML (default: markdown)"},
    }, ["url"]),
]

# --- Server 9: puppeteer (7 tools) ---
SERVER_PUPPETEER = [
    make_tool("navigate", "Navigate to a URL.", {
        "url": {"type": "string", "description": "URL to navigate to"},
    }, ["url"]),
    make_tool("click", "Click an element by selector.", {
        "selector": {"type": "string", "description": "CSS selector"},
    }, ["selector"]),
    make_tool("fill", "Fill an input element.", {
        "selector": {"type": "string", "description": "CSS selector"},
        "value": {"type": "string", "description": "Value to fill"},
    }, ["selector", "value"]),
    make_tool("evaluate", "Execute JavaScript in the page.", {
        "script": {"type": "string", "description": "JavaScript to execute"},
    }, ["script"]),
    make_tool("screenshot", "Take a screenshot of the page or element.", {
        "selector": {"type": "string", "description": "CSS selector (optional)"},
        "full_page": {"type": "boolean", "description": "Capture full page"},
    }, []),
    make_tool("go_back", "Navigate back in browser history.", {}, []),
    make_tool("wait_for_selector", "Wait for an element to appear.", {
        "selector": {"type": "string", "description": "CSS selector"},
        "timeout": {"type": "integer", "description": "Timeout in ms"},
    }, ["selector"]),
]

# --- Server 10: time (2 tools) ---
SERVER_TIME = [
    make_tool("get_time", "Get the current time in a timezone.", {
        "timezone": {"type": "string", "description": "IANA timezone (e.g. America/New_York)"},
    }, ["timezone"]),
    make_tool("convert_time", "Convert time between timezones.", {
        "source_timezone": {"type": "string", "description": "Source IANA timezone"},
        "target_timezone": {"type": "string", "description": "Target IANA timezone"},
        "time": {"type": "string", "description": "Time in HH:MM format"},
    }, ["source_timezone", "target_timezone", "time"]),
]

ALL_SERVERS = [
    ("filesystem", SERVER_FILESYSTEM),    # 8 tools
    ("github", SERVER_GITHUB),            # 11 tools
    ("postgres", SERVER_POSTGRES),        # 7 tools
    ("brave-search", SERVER_BRAVE),       # 3 tools
    ("slack", SERVER_SLACK),              # 8 tools
    ("sqlite", SERVER_SQLITE),            # 4 tools
    ("memory", SERVER_MEMORY),            # 5 tools
    ("fetch", SERVER_FETCH),              # 1 tool
    ("puppeteer", SERVER_PUPPETEER),      # 7 tools
    ("time", SERVER_TIME),                # 2 tools
]

# Total: 56 tools across 10 servers


# ============================================================
# Platform Payload Builders
# ============================================================

def build_hermes_payload(servers):
    """Hermes: full schemas, unmodified. Matches OpenAI function-calling format."""
    tools = []
    for server_name, tool_defs in servers:
        for td in tool_defs:
            schema = td["inputSchema"]
            tools.append({
                "type": "function",
                "function": {
                    "name": f"{server_name}__{td['name']}",
                    "description": td["description"],
                    "parameters": schema,
                },
            })
    return json.dumps(tools, separators=(",", ":"))


def build_zeroclaw_eager(servers):
    """ZeroClaw eager: same as Hermes baseline."""
    return build_hermes_payload(servers)


def build_zeroclaw_deferred(servers):
    """ZeroClaw deferred: stubs (name+desc) + tool_search tool definition."""
    stubs = []
    for server_name, tool_defs in servers:
        for td in tool_defs:
            stubs.append({
                "name": f"{server_name}__{td['name']}",
                "description": td["description"],
            })

    # The tool_search tool definition (what the LLM sees instead of all schemas)
    tool_search = {
        "type": "function",
        "function": {
            "name": "tool_search",
            "description": (
                "Search for available MCP tools by keyword. Use this to find tools "
                "for external services (databases, APIs, file systems). Discovered "
                "tools are activated and become available immediately."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keyword search terms (e.g. 'read file', 'query database')",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 10)",
                    },
                },
                "required": ["query"],
            },
        },
    }

    # Stubs rendered as a compact list in system prompt context
    # (name + description only, no JSON schema)
    stub_text = json.dumps(stubs, separators=(",", ":"))
    # In deferred mode, stubs are lightweight references + one search tool
    return stub_text + "\n" + json.dumps([tool_search], separators=(",", ":"))


def build_goclaw_eager(servers):
    """GoClaw eager: same as Hermes baseline."""
    return build_hermes_payload(servers)


def build_goclaw_search(servers):
    """GoClaw search mode: mcp_tool_search replaces all MCP tools (above threshold)."""
    tool_search = {
        "type": "function",
        "function": {
            "name": "mcp_tool_search",
            "description": (
                "Search for available external integration tools (MCP) by keyword. "
                "IMPORTANT: You have access to external service integrations "
                "(databases, APIs, file systems, messaging, etc.) through MCP tools "
                "that are NOT loaded by default. Before performing any external service "
                "operation, you MUST search here first to discover available tools. "
                "Use English keywords describing what you need "
                "(e.g. 'database query', 'create issue', 'send email'). "
                "Discovered tools become immediately available for use."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "English keywords describing the operation you need (e.g. 'create github issue', 'query postgres', 'send slack message')",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of tools to return (default: 5)",
                    },
                },
                "required": ["query"],
            },
        },
    }
    return json.dumps([tool_search], separators=(",", ":"))


def build_reasonix_raw(servers):
    """Reasonix raw: same as Hermes baseline (no canonicalization)."""
    return build_hermes_payload(servers)


def canonicalize_schema(value, parent_key=None):
    """Reasonix canonicalization: sort keys, sort required arrays, preserve enum order."""
    SET_LIKE_KEYS = {"required"}  # Keys where arrays should be sorted

    if isinstance(value, list):
        mapped = [canonicalize_schema(item, parent_key) for item in value]
        if parent_key in SET_LIKE_KEYS and all(
            x is None or isinstance(x, (str, int, float, bool)) for x in mapped
        ):
            return sorted(mapped, key=lambda x: str(x))
        return mapped

    if not isinstance(value, dict):
        return value

    if parent_key == "dependentRequired":
        out = {}
        for key in sorted(value.keys()):
            arr = value[key]
            if isinstance(arr, list) and all(
                isinstance(x, (str, int, float, bool)) or x is None for x in arr
            ):
                out[key] = sorted(arr, key=lambda x: str(x))
            else:
                out[key] = canonicalize_schema(arr, key)
        return out

    out = {}
    for key in sorted(value.keys()):
        out[key] = canonicalize_schema(value[key], key)
    return out


def build_reasonix_canonicalized(servers):
    """Reasonix canonicalized: sorted keys, sorted required arrays, preserved enum order."""
    tools = []
    for server_name, tool_defs in servers:
        for td in tool_defs:
            canonical_schema = canonicalize_schema(td["inputSchema"])
            tools.append({
                "type": "function",
                "function": {
                    "name": f"srv_{td['name']}",  # Reasonix uses srv_ prefix
                    "description": td["description"],
                    "parameters": canonical_schema,
                },
            })
    return json.dumps(tools, separators=(",", ":"))


# ============================================================
# Token Counting
# ============================================================

# Use cl100k_base (GPT-4/Claude-family tokenizer approximation)
enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(enc.encode(text))


# ============================================================
# Measurement Matrix
# ============================================================

PLATFORMS = [
    ("Hermes (baseline)", build_hermes_payload),
    ("ZeroClaw (eager)", build_zeroclaw_eager),
    ("ZeroClaw (deferred)", build_zeroclaw_deferred),
    ("GoClaw (eager)", build_goclaw_eager),
    ("GoClaw (search mode)", build_goclaw_search),
    ("Reasönix (raw)", build_reasonix_raw),
    ("Reasönix (canonicalized)", build_reasonix_canonicalized),
]

N_VALUES = [0, 1, 3, 5, 10]

print("=" * 80)
print("MCP Token Overhead Measurement — Static Reconstruction")
print("=" * 80)
print()
print(f"Token encoder: cl100k_base (GPT-4/Claude approximation)")
print(f"Servers available: {len(ALL_SERVERS)} ({sum(len(s[1]) for s in ALL_SERVERS)} total tools)")
print()

# Build table
header = f"{'Platform':<30}"
for n in N_VALUES:
    header += f" | N={n:<3}"
print(header)
print("-" * len(header))

results = {}

for platform_name, builder in PLATFORMS:
    row = f"{platform_name:<30}"
    results[platform_name] = {}

    for n in N_VALUES:
        servers = ALL_SERVERS[:n]
        payload = builder(servers)
        tokens = count_tokens(payload)
        results[platform_name][n] = tokens
        row += f" | {tokens:>5}"
    print(row)

print()

# Analysis
print("=" * 80)
print("ANALYSIS")
print("=" * 80)
print()

# 1. Deferred loading savings
print("--- ZeroClaw Deferred vs Eager (token savings) ---")
for n in N_VALUES:
    if n == 0:
        continue
    eager = results["ZeroClaw (eager)"][n]
    deferred = results["ZeroClaw (deferred)"][n]
    savings = eager - deferred
    pct = (savings / eager * 100) if eager > 0 else 0
    print(f"  N={n:>2}: {eager:>5} -> {deferred:>5} tokens (saves {savings:>5}, {pct:.1f}%)")

print()

# 2. GoClaw search mode savings
print("--- GoClaw Search Mode vs Eager (token savings) ---")
for n in N_VALUES:
    if n == 0:
        continue
    eager = results["GoClaw (eager)"][n]
    search = results["GoClaw (search mode)"][n]
    savings = eager - search
    pct = (savings / eager * 100) if eager > 0 else 0
    print(f"  N={n:>2}: {eager:>5} -> {search:>5} tokens (saves {savings:>5}, {pct:.1f}%)")

print()

# 3. Canonicalization overhead
print("--- Reasönix Canonicalization Overhead (tokens added) ---")
for n in N_VALUES:
    if n == 0:
        continue
    raw = results["Reasönix (raw)"][n]
    canon = results["Reasönix (canonicalized)"][n]
    diff = canon - raw
    pct = (abs(diff) / raw * 100) if raw > 0 else 0
    print(f"  N={n:>2}: {raw:>5} -> {canon:>5} tokens ({'+' if diff >= 0 else ''}{diff:>5}, {pct:.1f}%)")

print()

# 4. Per-tool token cost (Hermes baseline)
print("--- Per-Tool Token Cost (Hermes baseline) ---")
for n in N_VALUES:
    if n == 0:
        continue
    tool_count = sum(len(ALL_SERVERS[i][1]) for i in range(n))
    total = results["Hermes (baseline)"][n]
    per_tool = total / tool_count if tool_count > 0 else 0
    print(f"  N={n:>2} ({tool_count:>2} tools): {total:>5} tokens, {per_tool:.0f} tokens/tool")

print()

# 5. Growth rate comparison
print("--- Growth Rate (N=1 to N=10) ---")
for platform_name in [p[0] for p in PLATFORMS]:
    t1 = results[platform_name][1]
    t10 = results[platform_name][10]
    ratio = t10 / t1 if t1 > 0 else 0
    print(f"  {platform_name:<30} {t1:>5} -> {t10:>5} ({ratio:.1f}x)")

print()
print("=" * 80)
