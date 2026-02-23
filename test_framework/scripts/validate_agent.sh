#!/bin/bash

# Agent Validation Script

AGENT_CONFIG=$1

if [ -z "$AGENT_CONFIG" ]; then
    echo "Usage: $0 <agent_config.json>"
    exit 1
fi

if [ ! -f "$AGENT_CONFIG" ]; then
    echo "Agent config file not found: $AGENT_CONFIG"
    exit 1
fi

echo "Validating agent configuration: $AGENT_CONFIG"

# Validate JSON syntax
if ! jq empty "$AGENT_CONFIG" 2>/dev/null; then
    echo "ERROR: Invalid JSON syntax"
    exit 1
fi

# Check required fields
REQUIRED_FIELDS=("name" "skills" "security")
for field in "${REQUIRED_FIELDS[@]}"; do
    if ! jq -e ".${field}" "$AGENT_CONFIG" >/dev/null 2>&1; then
        echo "ERROR: Missing required field: $field"
        exit 1
    fi
done

# Validate skills
if ! jq -e '.skills.required | length > 0' "$AGENT_CONFIG" >/dev/null 2>&1; then
    echo "ERROR: At least one required skill must be specified"
    exit 1
fi

# Validate security rules
if ! jq -e '.security.rules | length > 0' "$AGENT_CONFIG" >/dev/null 2>&1; then
    echo "ERROR: At least one security rule must be specified"
    exit 1
fi

# Validate privileges
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_DIR="$(dirname "$SCRIPT_DIR")"
PRIVILEGES_FILE="$FRAMEWORK_DIR/security/privileges.json"
RULES_FILE="$FRAMEWORK_DIR/security/rules.json"

if [ -f "$PRIVILEGES_FILE" ]; then
    # Get all valid privileges from the privileges file
    VALID_PRIVILEGES=$(jq -r '.specific_privileges | keys[]' "$PRIVILEGES_FILE" 2>/dev/null)
    VALID_LEVELS=$(jq -r '.privilege_levels[].level' "$PRIVILEGES_FILE" 2>/dev/null)

    # Check each privilege in the agent config
    AGENT_PRIVILEGES=$(jq -r '.security.privileges[]' "$AGENT_CONFIG" 2>/dev/null)
    for priv in $AGENT_PRIVILEGES; do
        if ! echo "$VALID_PRIVILEGES $VALID_LEVELS" | grep -q -w "$priv"; then
            echo "ERROR: Invalid privilege: $priv"
            exit 1
        fi
    done
fi

# Validate security rules
if [ -f "$RULES_FILE" ]; then
    # Get all valid rules from the rules file
    VALID_RULES=$(jq -r '.rules[].id' "$RULES_FILE" 2>/dev/null)

    # Check each rule in the agent config
    AGENT_RULES=$(jq -r '.security.rules[]' "$AGENT_CONFIG" 2>/dev/null)
    for rule in $AGENT_RULES; do
        if ! echo "$VALID_RULES" | grep -q -w "$rule"; then
            echo "ERROR: Invalid security rule: $rule"
            exit 1
        fi
    done
fi

# Check credential encryption
if jq -e '.credentials.encrypted == true' "$AGENT_CONFIG" >/dev/null 2>&1; then
    if [ ! -f "credentials/.master_key" ]; then
        echo "ERROR: Master key not found for encrypted credentials"
        exit 1
    fi
fi

echo "Agent configuration is valid!"
echo "Skills: $(jq -r '.skills.required | join(", ")' "$AGENT_CONFIG")"
echo "Security rules: $(jq -r '.security.rules | length' "$AGENT_CONFIG") rules defined"