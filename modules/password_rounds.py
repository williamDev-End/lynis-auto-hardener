import os

def audit_password_rounds():
    """Checks if secure password hashing rounds are configured in login.defs."""
    print("\n--- Granular Password Hashing Rounds Check (AUTH-9230) ---")
    
    login_defs_path = "/etc/login.defs"
    rounds_configured = False
    
    if os.path.exists(login_defs_path):
        with open(login_defs_path, "r") as f:
            content = f.read()
        if "SHA_CRYPT_MIN_ROUNDS" in content:
            rounds_configured = True

    print(f"   - Secure Password Hashing Rounds Configured: {'✅ Yes' if rounds_configured else '⚠️ No'}")

    if not rounds_configured:
        if input("👉 Do you want to configure secure password hashing rounds (SHA-512)? (y/N): ").strip().lower() == 'y':
            apply_password_rounds_hardening()
    else:
        print("ℹ️ Password hashing rounds are already configured.")

def apply_password_rounds_hardening():
    """Appends secure hashing round parameters to login.defs."""
    print("🔒 Configuring secure password hashing rounds...")
    login_defs_path = "/etc/login.defs"
    
    rounds_config = [
        "\n# Added by Hardener Script for AUTH-9230\n",
        "ENCRYPT_METHOD SHA512\n",
        "SHA_CRYPT_MIN_ROUNDS 5000\n",
        "SHA_CRYPT_MAX_ROUNDS 10000\n"
    ]
    
    try:
        with open(login_defs_path, "a") as f:
            f.writelines(rounds_config)
        print("✅ Success: Password hashing rounds configured successfully.")
    except Exception as e:
        print(f"❌ Error applying password rounds hardening: {e}")