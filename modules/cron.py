import os

def audit_cron():
    """Checks and offers granular hardening and rollback for cron permissions."""
    print("\n--- Granular Cron Permissions Hardening & Rollback Check ---")
    
    # Format: (path, secure_perm, default_perm)
    cron_paths = [
        ("/etc/crontab", 0o600, 0o644),
        ("/etc/cron.hourly", 0o700, 0o755),
        ("/etc/cron.daily", 0o700, 0o755),
        ("/etc/cron.weekly", 0o700, 0o755),
        ("/etc/cron.monthly", 0o700, 0o755),
        ("/etc/cron.d", 0o700, 0o755)
    ]
    
    changes_made = False

    for path, secure_perm, default_perm in cron_paths:
        if os.path.exists(path):
            stat = os.stat(path)
            current_perm = oct(stat.st_mode)[-4:]
            secure_perm_str = oct(secure_perm)[-4:]
            default_perm_str = oct(default_perm)[-4:]
            
            is_secure = (current_perm == secure_perm_str) and (stat.st_uid == 0)
            print(f"   - {path}: current {current_perm} (secure target: {secure_perm_str})", end="")
            print(f" {'✅ Secured' if is_secure else '⚠️ Insecure'}")
            
            choice = input(f"     👉 Action: [y] Secure ({secure_perm_str}) | [r] Restore default ({default_perm_str}) | [N] Skip: ").strip().lower()
            if choice == 'y':
                apply_cron_permissions(path, secure_perm)
                changes_made = True
            elif choice == 'r':
                apply_cron_permissions(path, default_perm)
                changes_made = True

    if changes_made:
        print("✅ Cron permissions hardening & rollback applied successfully.")
    else:
        print("ℹ️ No cron changes selected.")

def apply_cron_permissions(path, perm):
    """Applies specific permissions and root ownership to a cron path."""
    print(f"🔒 Setting permissions {oct(perm)[-4:]} on {path}...")
    try:
        if os.path.isfile(path):
            os.chmod(path, perm)
            os.chown(path, 0, 0)
        elif os.path.isdir(path):
            os.chmod(path, perm)
            os.chown(path, 0, 0)
        print(f"✅ Success: Updated {path}.")
    except Exception as e:
        print(f"❌ Error updating {path}: {e}")