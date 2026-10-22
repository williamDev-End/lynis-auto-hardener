import subprocess
import os

def audit_updates():
    """Checks unattended-upgrades status and offers granular hardening options."""
    print("\n--- Granular Automatic Updates Hardening Check ---")
    
    res = subprocess.run(["dpkg", "-l", "unattended-upgrades"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    is_installed = "ii" in res.stdout
    
    print(f"   - Unattended-Upgrades Installed: {'✅ Yes' if is_installed else '❌ No'}")

    changes_made = False

    if not is_installed:
        if input("👉 Do you want to install unattended-upgrades? (y/N): ").strip().lower() == 'y':
            install_updates()
            is_installed = True
            changes_made = True
        else:
            print("❌ Skipping unattended-upgrades installation.")
            return

    if is_installed:
        if input("👉 Do you want to configure and enable automatic security updates? (y/N): ").strip().lower() == 'y':
            configure_updates()
            changes_made = True

    if changes_made:
        print("✅ Automatic updates hardening applied successfully.")
    else:
        print("ℹ️ No automatic updates changes selected.")

def install_updates():
    """Installs unattended-upgrades package."""
    print("🔒 Installing unattended-upgrades...")
    try:
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"
        subprocess.run(["apt", "update"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        subprocess.run(["apt", "install", "-y", "unattended-upgrades"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        print("✅ Success: Unattended-upgrades installed.")
    except Exception as e:
        print(f"❌ Error installing unattended-upgrades: {e}")

def configure_updates():
    """Configures and enables unattended-upgrades non-interactively."""
    print("🔒 Configuring automatic security updates...")
    try:
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"
        subprocess.run(["dpkg-reconfigure", "-f", "noninteractive", "unattended-upgrades"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        print("✅ Success: Automatic updates configured and enabled.")
    except Exception as e:
        print(f"❌ Error configuring automatic updates: {e}")