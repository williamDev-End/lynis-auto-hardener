import os
import subprocess

def audit_ssh():
    """Checks SSH configuration and offers granular hardening and rollback options."""
    print("\n--- Granular SSH Hardening & Rollback Check ---")
    
    sshd_config_path = "/etc/ssh/sshd_config"
    if not os.path.exists(sshd_config_path):
        print("ℹ️ sshd_config not found. Skipping SSH checks.")
        return

    with open(sshd_config_path, "r") as f:
        content = f.read()

    root_login_secure = "PermitRootLogin no" in content or "PermitRootLogin prohibit-password" in content
    pass_auth_secure = "PasswordAuthentication no" in content

    print(f"   - PermitRootLogin Restricted: {'✅ Yes' if root_login_secure else '⚠️ No'}")
    print(f"   - PasswordAuthentication Disabled (Key-only): {'✅ Yes' if pass_auth_secure else '⚠️ No'}")

    changes_made = False

    # 1. PermitRootLogin restriction
    print(f"   - Root Login (Target: no/prohibit-password | Default/Restore: yes)")
    choice_root = input("     👉 Action: [y] Secure (no) | [r] Restore default (yes) | [N] Skip: ").strip().lower()
    if choice_root == 'y':
        update_sshd_config("PermitRootLogin", "no", sshd_config_path)
        changes_made = True
    elif choice_root == 'r':
        update_sshd_config("PermitRootLogin", "yes", sshd_config_path)
        changes_made = True

    # 2. PasswordAuthentication restriction
    print(f"   - Password Authentication (Target: no | Default/Restore: yes)")
    choice_pass = input("     👉 Action: [y] Secure (no) | [r] Restore default (yes) | [N] Skip: ").strip().lower()
    if choice_pass == 'y':
        update_sshd_config("PasswordAuthentication", "no", sshd_config_path)
        changes_made = True
    elif choice_pass == 'r':
        update_sshd_config("PasswordAuthentication", "yes", sshd_config_path)
        changes_made = True

    if changes_made:
        reload_ssh_service()
        print("✅ SSH hardening & rollback applied successfully.")
    else:
        print("ℹ️ No SSH changes selected.")

def update_sshd_config(key, value, config_path):
    """Updates or adds a configuration directive in sshd_config."""
    print(f"🔒 Setting {key} {value} in {config_path}...")
    try:
        with open(config_path, "r") as f:
            lines = f.readlines()

        updated = False
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(key) or stripped.startswith(f"#{key}"):
                new_lines.append(f"{key} {value}\n")
                updated = True
            else:
                new_lines.append(line)

        if not updated:
            new_lines.append(f"{key} {value}\n")

        with open(config_path, "w") as f:
            f.writelines(new_lines)
        print(f"✅ Success: {key} set to {value}.")
    except Exception as e:
        print(f"❌ Error updating {key}: {e}")

def reload_ssh_service():
    """Restarts SSH service to apply changes."""
    print("🔒 Restarting SSH service...")
    try:
        subprocess.run(["systemctl", "restart", "ssh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Success: SSH service reloaded.")
    except Exception as e:
        print(f"❌ Error reloading SSH service: {e}")