# AllClaws Test Framework FAQ

## Credentials Management

### How is the credentials folder created?

The credentials folder is created automatically during the framework setup process:

1. **Setup Script Execution**: When you run `./scripts/setup.sh`, it creates the necessary directory structure:
   ```bash
   mkdir -p credentials/.encrypted
   ```

2. **Master Key Generation**: The setup script also generates a unique encryption key:
   ```bash
   openssl rand -hex 32 > credentials/.master_key
   chmod 600 credentials/.master_key  # Restricts access to owner only
   ```

### How to keep information in the credentials folder local and private?

The framework implements multiple layers of security to keep credential information private:

#### 1. Git Exclusion (.gitignore)
The entire `credentials/` directory is excluded from version control:
```
# Credentials and encryption keys
credentials/
*.key
*.pem
*.crt
*.p12
*.pfx
```

#### 2. Encryption at Rest
- Credentials are encrypted using **AES-256** encryption
- The master key is stored locally in `credentials/.master_key` (never committed to git)
- Encrypted credentials are stored in `credentials/.encrypted/` subdirectory

#### 3. File Permissions
- The master key file has restrictive permissions (`chmod 600`) - only the owner can read/write
- The `.encrypted/` directory has owner-only permissions (`chmod 700`) - only the owner can read/write/execute
- This prevents other users on the system from accessing the key or encrypted credential files

#### 4. Local-Only Storage
- All credential data stays on your local machine
- No credentials are transmitted or stored remotely
- The framework validates that encrypted credentials require a local master key

#### 5. Security Validation
The framework includes security checks:
- Agents requiring encrypted credentials will fail validation if no master key exists
- All credential access is validated through the framework's security rules

#### Usage Example
When defining an agent with credentials:
```json
{
  "credentials": {
    "encrypted": true,
    "providers": [
      {
        "type": "api_key",
        "service": "openai",
        "key": "your-api-key-here"
      }
    ]
  }
}
```

The framework automatically encrypts these credentials using the local master key and stores them securely in the `credentials/.encrypted/` directory. This ensures that sensitive information never leaves your local environment and cannot be accidentally committed to version control.