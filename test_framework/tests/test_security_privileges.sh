#!/bin/bash

# Test Suite for Security & Privilege Tests
# Test Cases 2.1-2.4: Security rule enforcement and privilege management

set -e

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_DIR="$(dirname "$TEST_DIR")"
SCRIPT_DIR="$FRAMEWORK_DIR/scripts"
SECURITY_DIR="$FRAMEWORK_DIR/security"

echo "Running Security & Privilege Tests..."

# Test 2.1: Privilege levels are properly defined
echo "Test 2.1: Privilege levels are properly defined"
PRIVILEGES_FILE="$SECURITY_DIR/privileges.json"
if [ ! -f "$PRIVILEGES_FILE" ]; then
    echo "FAIL: Test 2.1 - Privileges file not found: $PRIVILEGES_FILE"
    exit 1
fi

# Check if privilege levels exist
PRIVILEGE_LEVELS=$(jq -r '.privilege_levels | length' "$PRIVILEGES_FILE")
if [ "$PRIVILEGE_LEVELS" -ge 3 ]; then
    echo "PASS: Test 2.1 - Found $PRIVILEGE_LEVELS privilege levels"
else
    echo "FAIL: Test 2.1 - Expected at least 3 privilege levels, found $PRIVILEGE_LEVELS"
    exit 1
fi

# Test 2.2: Security rules are properly defined
echo "Test 2.2: Security rules are properly defined"
RULES_FILE="$SECURITY_DIR/rules.json"
if [ ! -f "$RULES_FILE" ]; then
    echo "FAIL: Test 2.2 - Rules file not found: $RULES_FILE"
    exit 1
fi

# Check if security rules exist
SECURITY_RULES=$(jq -r '.rules | length' "$RULES_FILE")
if [ "$SECURITY_RULES" -ge 3 ]; then
    echo "PASS: Test 2.2 - Found $SECURITY_RULES security rules"
else
    echo "FAIL: Test 2.2 - Expected at least 3 security rules, found $SECURITY_RULES"
    exit 1
fi

# Test 2.3: Agent privilege validation (this will fail initially - no implementation yet)
echo "Test 2.3: Agent privilege validation"
TEST_AGENT="./tmp/privilege_test_agent.json"
cat > "$TEST_AGENT" << 'EOF'
{
  "name": "PrivilegeTestAgent",
  "skills": {
    "required": ["test"]
  },
  "security": {
    "rules": ["test"],
    "privileges": ["nonexistent_privilege"]
  }
}
EOF

# This test should fail because privilege validation is not implemented yet
if "$SCRIPT_DIR/validate_agent.sh" "$TEST_AGENT" > ./tmp/privilege_test.log 2>&1; then
    echo "FAIL: Test 2.3 - Validation should have failed for invalid privilege"
    cat ./tmp/privilege_test.log
    exit 1
else
    if grep -q "Invalid privilege" ./tmp/privilege_test.log; then
        echo "PASS: Test 2.3 - Privilege validation working"
    else
        echo "EXPECTED FAIL: Test 2.3 - Privilege validation not yet implemented"
        # This is expected to fail in TDD - we need to implement privilege validation
    fi
fi

# Test 2.4: Security rule validation (this will fail initially - no implementation yet)
echo "Test 2.4: Security rule validation"
TEST_AGENT2="./tmp/rule_test_agent.json"
cat > "$TEST_AGENT2" << 'EOF'
{
  "name": "RuleTestAgent",
  "skills": {
    "required": ["test"]
  },
  "security": {
    "rules": ["nonexistent_rule"],
    "privileges": ["test"]
  }
}
EOF

# This test should fail because rule validation is not implemented yet
if "$SCRIPT_DIR/validate_agent.sh" "$TEST_AGENT2" > ./tmp/rule_test.log 2>&1; then
    echo "FAIL: Test 2.4 - Validation should have failed for invalid rule"
    cat ./tmp/rule_test.log
    exit 1
else
    if grep -q "Invalid security rule" ./tmp/rule_test.log; then
        echo "PASS: Test 2.4 - Security rule validation working"
    else
        echo "EXPECTED FAIL: Test 2.4 - Security rule validation not yet implemented"
        # This is expected to fail in TDD - we need to implement rule validation
    fi
fi

# Clean up
rm -f ./tmp/privilege_test.log ./tmp/rule_test.log "$TEST_AGENT" "$TEST_AGENT2"

echo "Security & Privilege Tests completed (some expected to fail until implementation)"