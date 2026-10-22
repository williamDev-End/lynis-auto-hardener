import os

def audit_security_limits():
    """Checks password expiration policies and core dumps restriction with granular choices and rollback."""
    print("\n--- Granular Login Policy & Core Dumps Hardening & Rollback Check ---")
    
    login_defs_path = "/etc/login.defs"
    limits_conf_path = "/etc/security/limits.conf"
    
    password_policy_secured = False
    if os.path.exists(login_defs_path):
        with open(login_defs_path, "r") as f:
            content = f.read()
        for line in content.splitlines():
            if line.strip().startswith("PASS_MAX_DAYS"):
                try:
                    days = int(line.split()[1])
                    if days <= 90:
                        password_policy_secured = True
                except ValueError:
                    pass

    coredump_secured = False
    if os.path.exists(limits_conf_path):
        with open(limits_conf_path, "r") as f:
            limits_content = f.read()
        if "* hard core 0" in limits_content:
            coredump_secured = True

    print(f"   - Password Aging Configured (<= 90 days max): {'✅ Yes' if password_policy_secured else '⚠️ No'}")
    print(f"   - Core Dumps Disabled: {'✅ Yes' if coredump_secured else '⚠️ No'}")

    changes_made = False

    # 1. Password Aging Policy
    print(f"   - Password Expiration (Target: 90 days max | Default/Restore: 99999 days)")
    choice_pass = input("     👉 Action: [y] Secure (90 days) | [r] Restore default (99999 days) | [N] Skip: ").strip().lower()
    if choice_pass == 'y':
        apply_password_policy(90)
        changes_made = True
    elif choice_pass == 'r':
        apply_password_policy(99999)
        changes_made = True

    # 2. Core Dumps Restriction
    print(f"   - Core Dumps Restriction (Target: disabled [0] | Default/Restore: enabled/unlimited)")
    choice_core = input("     👉 Action: [y] Secure (Disable) | [r] Restore default (Enable) | [N] Skip: ").strip().lower()
    if choice_core == 'y':
        apply_coredump_restriction(disable=True)
        changes_made = True
    elif choice_core == 'r':
        apply_coredump_restriction(disable=False)
        changes_made = True

    if changes_made:
        print("✅ Security limits hardening & rollback applied successfully.")
    else:
        print("ℹ️ No security limits changes selected.")

def apply_password_policy(max_days):
    """Updates password aging parameters in login.defs."""
    print(f"🔒 Setting password maximum age to {max_days} days...")
    login_defs_path = "/etc/login.defs"
    min_days = 7 if max_days != 99999 else 0
    warn_age = 14 if max_days != 99999 else 7
    try:
        with open(login_defs_path, "r") as f:
            lines = f.readlines()
        
        new_lines = []
        found_max = found_min = found_warn = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("PASS_MAX_DAYS"):
                new_lines.append(f"PASS_MAX_DAYS   {max_days}\n")
                found_max = True
            elif stripped.startswith("PASS_MIN_DAYS"):
                new_lines.append(f"PASS_MIN_DAYS   {min_days}\n")
                found_min = True
            elif stripped.startswith("PASS_WARN_AGE"):
                new_lines.append(f"PASS_WARN_AGE   {warn_age}\n")
                found_warn = True
            else:
                new_lines.append(line)
        
        if not found_max:
            new_lines.append(f"PASS_MAX_DAYS   {max_days}\n")
        if not found_min:
            new_lines.append(f"PASS_MIN_DAYS   {min_days}\n")
        if not found_warn:
            new_lines.append(f"PASS_WARN_AGE   {warn_age}\n")
        
        with open(login_defs_path, "w") as f:
            f.writelines(new_lines)
        print("✅ Success: Password policy updated.")
    except Exception as e:
        print(f"❌ Error updating password policy: {e}")

def apply_coredump_restriction(disable=True):
    """Disables or re-enables core dumps in limits.conf."""
    limits_conf_path = "/etc/security/limits.conf"
    try:
        if os.path.exists(limits_conf_path):
            with open(limits_conf_path, "r") as f:
                lines = f.readlines()
            
            new_lines = [l for l in lines if "hard core" not in l and "Added by Lynis-Auto-Hardener" not in l]
            
            if disable:
                print("🔒 Restricting core dumps...")
                new_lines.append("\n# Added by Lynis-Auto-Hardener\n* hard core 0\n")
            else:
                print("🔒 Restoring default core dumps...")
                new_lines.append("\n# Restored default by Lynis-Auto-Hardener\n* hard core unlimited\n")
            
            with open(limits_conf_path, "w") as f:
                f.writelines(new_lines)
            print("✅ Success: Core dumps settings updated.")
    except Exception as e:
        print(f"❌ Error configuring core dumps: {e}")