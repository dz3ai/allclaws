#!/bin/bash

# Test Suite for Agent Configuration Validation
# Test Case 1.1: Valid agent config with all required fields should pass validation

set -e

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_DIR="$(dirname "$TEST_DIR")"
SCRIPT_DIR="$FRAMEWORK_DIR/scripts"

echo "Running Agent Configuration Validation Tests..."

# Test 1.1: Valid agent config should pass
echo "Test 1.1: Valid agent config should pass validation"
VALID_CONFIG="$FRAMEWORK_DIR/agents/example_agent.json"
if [ ! -f "$VALID_CONFIG" ]; then
    echo "FAIL: Valid config file not found: $VALID_CONFIG"
    exit 1
fi

# Run validation script
if "$SCRIPT_DIR/validate_agent.sh" "$VALID_CONFIG" > ./tmp/test_output.log 2>&1; then
    if grep -q "Agent configuration is valid!" ./tmp/test_output.log; then
        echo "PASS: Test 1.1"
    else
        echo "FAIL: Test 1.1 - Validation passed but no success message"
        cat ./tmp/test_output.log
        exit 1
    fi
else
    echo "FAIL: Test 1.1 - Validation failed for valid config"
    cat ./tmp/test_output.log
    exit 1
fi

# Test 1.2: Missing required fields should fail
echo "Test 1.2: Agent config missing required fields should fail"
INVALID_CONFIG="./tmp/invalid_agent.json"
cat > "$INVALID_CONFIG" << 'EOF'
{
  "name": "InvalidAgent"
}
EOF

if "$SCRIPT_DIR/validate_agent.sh" "$INVALID_CONFIG" > ./tmp/test_output2.log 2>&1; then
    echo "FAIL: Test 1.2 - Validation should have failed for missing fields"
    cat ./tmp/test_output2.log
    exit 1
else
    if grep -q "Missing required field:" ./tmp/test_output2.log; then
        echo "PASS: Test 1.2"
    else
        echo "FAIL: Test 1.2 - Validation failed but not for expected reason"
        cat ./tmp/test_output2.log
        exit 1
    fi
fi

# Test 1.3: Invalid JSON should fail
echo "Test 1.3: Invalid JSON syntax should fail validation"
INVALID_JSON="./tmp/invalid_json.json"
echo '{"name": "Test", "invalid": json}' > "$INVALID_JSON"

if "$SCRIPT_DIR/validate_agent.sh" "$INVALID_JSON" > ./tmp/test_output3.log 2>&1; then
    echo "FAIL: Test 1.3 - Validation should have failed for invalid JSON"
    cat ./tmp/test_output3.log
    exit 1
else
    if grep -q "Invalid JSON syntax" ./tmp/test_output3.log; then
        echo "PASS: Test 1.3"
    else
        echo "FAIL: Test 1.3 - Validation failed but not for JSON syntax"
        cat ./tmp/test_output3.log
        exit 1
    fi
fi

# Test 1.4: Empty required skills should fail
echo "Test 1.4: Agent with empty required skills array should fail"
EMPTY_SKILLS_CONFIG="./tmp/empty_skills_agent.json"
cat > "$EMPTY_SKILLS_CONFIG" << 'EOF'
{
  "name": "EmptySkillsAgent",
  "skills": {
    "required": [],
    "optional": ["test"]
  },
  "security": {
    "rules": ["no_external_network"],
    "privileges": ["read_home_dir"]
  }
}
EOF

if "$SCRIPT_DIR/validate_agent.sh" "$EMPTY_SKILLS_CONFIG" > ./tmp/test_output4.log 2>&1; then
    echo "FAIL: Test 1.4 - Validation should have failed for empty skills"
    cat ./tmp/test_output4.log
    exit 1
else
    if grep -q "At least one required skill must be specified" ./tmp/test_output4.log; then
        echo "PASS: Test 1.4"
    else
        echo "FAIL: Test 1.4 - Validation failed but not for empty skills"
        cat ./tmp/test_output4.log
        exit 1
    fi
fi

# Test 1.5: Encrypted credentials without master key should fail
echo "Test 1.5: Agent with encrypted credentials but no master key should fail"
ENCRYPTED_CONFIG="./tmp/encrypted_agent.json"
cat > "$ENCRYPTED_CONFIG" << 'EOF'
{
  "name": "EncryptedAgent",
  "skills": {
    "required": ["test"]
  },
  "security": {
    "rules": ["no_external_network"],
    "privileges": ["read_home_dir"]
  },
  "credentials": {
    "encrypted": true,
    "providers": []
  }
}
EOF

# Temporarily move master key if it exists
if [ -f "$FRAMEWORK_DIR/credentials/.master_key" ]; then
    mv "$FRAMEWORK_DIR/credentials/.master_key" "$FRAMEWORK_DIR/credentials/.master_key.bak"
fi

if "$SCRIPT_DIR/validate_agent.sh" "$ENCRYPTED_CONFIG" > ./tmp/test_output5.log 2>&1; then
    echo "FAIL: Test 1.5 - Validation should have failed without master key"
    cat ./tmp/test_output5.log
    exit 1
else
    if grep -q "Master key not found for encrypted credentials" ./tmp/test_output5.log; then
        echo "PASS: Test 1.5"
    else
        echo "FAIL: Test 1.5 - Validation failed but not for missing master key"
        cat ./tmp/test_output5.log
        exit 1
    fi
fi

# Restore master key
if [ -f "$FRAMEWORK_DIR/credentials/.master_key.bak" ]; then
    mv "$FRAMEWORK_DIR/credentials/.master_key.bak" "$FRAMEWORK_DIR/credentials/.master_key"
fi

# Clean up
rm -f ./tmp/test_output*.log ./tmp/invalid_agent.json ./tmp/invalid_json.json ./tmp/empty_skills_agent.json ./tmp/encrypted_agent.json

echo "All Agent Configuration Validation Tests PASSED!"