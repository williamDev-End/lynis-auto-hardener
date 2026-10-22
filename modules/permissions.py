import os

def audit_permissions():
    """Checks and offers granular permissions hardening and rollback for sensitive files."""
    print("\n--- Granular Sensitive Files Permissions Check & Rollback ---")
    
    # Format: (filepath, secure_permission, default_permission)
    sensitive_files = [
        ("/etc/shadow", 0o600, 0o640),
        ("/etc/gshadow", 0o600, 0o640),
        ("/etc/passwd", 0o644, 0o644),
        ("/etc/group", 0o644, 0o644)
    ]
    
    changes_made = False

    for filepath, secure_perm, default_perm in sensitive_files:
        if os.path.exists(filepath):
            current_perm = oct(os.stat(filepath).st_mode)[-4:]
            secure_perm_str = oct(secure_perm)[-4:]
            default_perm_str = oct(default_perm)[-4:]
            
            is_secure = (current_perm == secure_perm_str)
            print(f"   - {filepath}: current {current_perm} (secure target: {secure_perm_str})", end="")
            print(f" {'✅ Secured' if is_secure else '⚠️ Insecure'}")
            
            choice = input(f"     👉 Action: [y] Apply secure ({secure_perm_str}) | [r] Restore default ({default_perm_str}) | [N] Skip: ").strip().lower()
            
            if choice == 'y':
                apply_file_permission(filepath, secure_perm)
                changes_made = True
            elif choice == 'r':
                apply_file_permission(filepath, default_perm)
                changes_made = True
            else:
                print("     ❌ Action skipped.")

    if changes_made:
        print("✅ Permissions updates applied successfully.")
    else:
        print("ℹ️ No permission changes selected.")

def apply_file_permission(filepath, perm):
    """Applies specific permissions to a file."""
    print(f"🔒 Setting permissions {oct(perm)[-4:]} on {filepath}...")
    try:
        os.chmod(filepath, perm)
        print(f"✅ Success: Permissions updated for {filepath}.")
    except Exception as e:
        print(f"❌ Error updating permissions for {filepath}: {e}")