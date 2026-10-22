import subprocess
import os

def audit_auditd():
    """Checks auditd status and offers granular hardening options."""
    print("\n--- Granular Auditd Hardening Check ---")
    
    res = subprocess.run(["dpkg", "-l", "auditd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    is_installed = "ii" in res.stdout
    
    print(f"   - Auditd Installed: {'✅ Yes' if is_installed else '❌ No'}")

    changes_made = False

    if not is_installed:
        if input("👉 Do you want to install auditd? (y/N): ").strip().lower() == 'y':
            install_auditd()
            is_installed = True
            changes_made = True
        else:
            print("❌ Skipping auditd installation.")
            return

    if is_installed:
        active_res = subprocess.run(["systemctl", "is-active", "auditd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        is_active = active_res.returncode == 0
        print(f"   - Auditd Service Active: {'✅ Yes' if is_active else '⚠️ No'}")

        if not is_active:
            if input("👉 Do you want to enable and start the auditd service? (y/N): ").strip().lower() == 'y':
                start_auditd()
                changes_made = True

    if changes_made:
        print("✅ Auditd hardening applied successfully.")
    else:
        print("ℹ️ No auditd changes selected.")

def install_auditd():
    """Installs auditd package."""
    print("🔒 Installing auditd...")
    try:
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"
        subprocess.run(["apt", "update"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        subprocess.run(["apt", "install", "-y", "auditd"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        print("✅ Success: Auditd installed.")
    except Exception as e:
        print(f"❌ Error installing auditd: {e}")

def start_auditd():
    """Enables and starts auditd service with container fallback."""
    print("🔒 Enabling and starting auditd...")
    try:
        subprocess.run(["systemctl", "enable", "auditd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = subprocess.run(["systemctl", "start", "auditd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            subprocess.run(["service", "auditd", "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Success: Auditd service enabled and started.")
    except Exception as e:
        print(f"❌ Error starting auditd: {e}")