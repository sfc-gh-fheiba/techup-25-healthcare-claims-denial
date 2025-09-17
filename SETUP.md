# 🚀 Healthcare Claims Demo Setup Guide

This guide will help you set up your local environment to run the Snowflake Cortex Healthcare Claims Optimization demo.

## Prerequisites

- **Snowflake Account**: Access to `sfsenorthamerica-demo158` account
- **User Account**: Your own Snowflake user (different from `claimsadmin`)
- **Snowflake CLI**: Install from [Snowflake CLI Installation Guide](https://docs.snowflake.com/en/user-guide/snowflake-cli)
- **Database Access**: Permissions to `CLAIMS_DEMO` database and `CLAIMS_HOSPITAL_CLAIMS__REMITS_DATA` marketplace data

## 📋 Step-by-Step Setup

### Step 1: Clone the Repository

```bash
git clone [repository-url]
cd techup-25-healthcare-claims-denial
```

### Step 2: Generate RSA Key Pair for Snowflake Authentication

Create secure RSA keys for authentication (bypasses MFA requirements):

```bash
# Create .ssh directory if it doesn't exist
mkdir -p ~/.ssh

# Generate RSA private key in PKCS8 format (required by Snowflake)
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out ~/.ssh/snowflake_rsa_key.p8 -nocrypt

# Generate public key
openssl rsa -in ~/.ssh/snowflake_rsa_key.p8 -pubout -out ~/.ssh/snowflake_rsa_key.pub

# Set secure permissions
chmod 600 ~/.ssh/snowflake_rsa_key.p8 ~/.ssh/snowflake_rsa_key.pub
```

### Step 3: Get Public Key for Snowflake

Extract the public key in the format Snowflake requires:

```bash
openssl rsa -in ~/.ssh/snowflake_rsa_key.p8 -pubout -outform DER | openssl base64 -A
```

**Copy the output** - you'll need this for the next step.

### Step 4: Add Public Key to Your Snowflake User

#### Option A: Using Snowflake Web UI
1. Log in to: `https://sfsenorthamerica-demo158.snowflakecomputing.com`
2. Go to **Account** → **Users & Roles** → **Users**
3. Find your user account and click to edit
4. In the **RSA Public Key** field, paste the key from Step 3

#### Option B: Using SQL (if you have admin access)
Run this SQL command as ACCOUNTADMIN (replace `YOUR_USERNAME` and the key):

```sql
ALTER USER YOUR_USERNAME SET RSA_PUBLIC_KEY='[PASTE_YOUR_PUBLIC_KEY_HERE]';
```

### Step 5: Create Your Configuration File

```bash
# Copy the template to create your config
cp config.toml.template config.toml
```

Edit `config.toml` and update the following values:

```toml
[connections.healthcare_claims_demo]
account = "sfsenorthamerica-demo158"
user = "YOUR_SNOWFLAKE_USERNAME"                           # ← Replace with your username
private_key_path = "/Users/YOUR_LOCAL_USERNAME/.ssh/snowflake_rsa_key.p8"  # ← Update path
authenticator = "SNOWFLAKE_JWT"
role = "ACCOUNTADMIN"
warehouse = "DEMO_WH"
database = "CLAIMS_DEMO"
schema = "PUBLIC"
```

**Important**: Replace:
- `YOUR_SNOWFLAKE_USERNAME` with your Snowflake username
- `/Users/YOUR_LOCAL_USERNAME` with your actual home directory path

### Step 6: Test Your Connection

```bash
# Test the connection
snow --config-file ./config.toml connection test -c healthcare_claims_demo

# If successful, you should see:
# Status: OK
# Account: sfsenorthamerica-demo158
# User: [your-username]
```

### Step 7: Verify Database Access

```bash
# Test marketplace database access
snow --config-file ./config.toml sql -q "SHOW DATABASES LIKE '%CLAIMS_HOSPITAL%';"

# Test project database access  
snow --config-file ./config.toml sql -q "USE DATABASE CLAIMS_DEMO; SELECT CURRENT_DATABASE();"
```

## 🔧 Configuration Details

### Database Architecture

Your setup will have access to:

- **`CLAIMS_HOSPITAL_CLAIMS__REMITS_DATA`**: Snowflake Marketplace data (read-only)
  - Real healthcare claims and remittance data
  - Use for analysis and pattern recognition
  
- **`CLAIMS_DEMO`**: Main project database (full access)
  - Your working database for custom tables and processing
  - Store generated content, processed results, and demo data

### Warehouse Information

- **`DEMO_WH`**: Shared demo warehouse for all team members
- **Auto-suspend**: Configured to minimize costs
- **Size**: Optimized for demo workloads

## 🛠️ Troubleshooting

### Connection Issues

#### "MFA authentication is required"
- **Solution**: Ensure you're using RSA key authentication with `authenticator = "SNOWFLAKE_JWT"`

#### "No such file or directory" for private key
- **Solution**: Check that the `private_key_path` uses absolute path (not `~`)
- **Example**: `/Users/john/.ssh/snowflake_rsa_key.p8` ✅
- **Not**: `~/.ssh/snowflake_rsa_key.p8` ❌

#### "Private Key authentication requires authenticator set to SNOWFLAKE_JWT"  
- **Solution**: Add `authenticator = "SNOWFLAKE_JWT"` to your config.toml

#### "Database does not exist"
- **Solution**: Contact team lead to ensure you have access to `CLAIMS_DEMO` database

### Permission Issues

#### "Insufficient privileges"
- **Solution**: Ensure your user has `ACCOUNTADMIN` role or appropriate permissions
- **Contact**: Team lead to grant necessary permissions

#### "Cannot access marketplace data"
- **Solution**: Marketplace data access may need to be granted by account admin

## ✅ Verification Checklist

Before proceeding with demo development:

- [ ] RSA key pair generated and secured
- [ ] Public key added to Snowflake user account  
- [ ] `config.toml` created from template with your details
- [ ] Connection test passes (`Status: OK`)
- [ ] Can query marketplace database: `CLAIMS_HOSPITAL_CLAIMS__REMITS_DATA`
- [ ] Can access project database: `CLAIMS_DEMO`
- [ ] Warehouse `DEMO_WH` is accessible

## 🔐 Security Notes

- **Never commit** `config.toml` to git (it's in `.gitignore`)
- **Protect your private key**: Keep `~/.ssh/snowflake_rsa_key.p8` secure (600 permissions)
- **Share responsibly**: Only share the public key, never the private key
- **Team access**: Each team member should have their own user account and RSA keys

## 🆘 Need Help?

If you encounter issues:

1. **Check the error message** carefully - often provides specific guidance
2. **Verify credentials** in Snowflake web UI
3. **Test basic connectivity** before complex operations
4. **Ask team lead** for permission or access issues
5. **Check Snowflake documentation** for CLI troubleshooting

---

Once setup is complete, you'll be ready to develop and demo the Healthcare Claims Optimization system using the full power of Snowflake's Data Cloud and AI capabilities! 🎉
