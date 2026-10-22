import subprocess
import os

def audit_fail2ban():
    """Checks fail2ban status and offers granular hardening options."""
    print("\n--- Granular Fail2ban Hardening Check ---")
    
    res = subprocess.run(["dpkg", "-l", "fail2ban"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    is_installed = "ii" in res.stdout
    
    print(f"   - Fail2ban Installed: {'✅ Yes' if is_installed else '❌ No'}")

    changes_made = False

    if not is_installed:
        if input("👉 Do you want to install fail2ban? (y/N): ").strip().lower() == 'y':
            install_fail2ban()
            is_installed = True
            changes_made = True
        else:
            print("❌ Skipping fail2ban installation.")
            return

    if is_installed:
        local_exists = os.path.exists("/etc/fail2ban/jail.local")
        print(f"   - Local Configuration (jail.local) Exists: {'✅ Yes' if local_exists else '⚠️ No'}")

        if not local_exists:
            if input("👉 Do you want to create jail.local from jail.conf to protect your custom settings? (y/N): ").strip().lower() == 'y':
                create_jail_local()
                changes_made = True

        if input("👉 Do you want to enable and start the fail2ban service? (y/N): ").strip().lower() == 'y':
            start_fail2ban()
            changes_made = True

    if changes_made:
        print("✅ Fail2ban hardening applied successfully.")
    else:
        print("ℹ️ No fail2ban changes selected.")

def install_fail2ban():
    """Installs fail2ban package."""
    print("🔒 Installing fail2ban...")
    try:
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"
        subprocess.run(["apt", "update"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        subprocess.run(["apt", "install", "-y", "fail2ban"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        print("✅ Success: Fail2ban installed.")
    except Exception as e:
        print(f"❌ Error installing fail2ban: {e}")

def create_jail_local():
    """Copies jail.conf to jail.local."""
    print("🔒 Creating jail.local configuration...")
    try:
        conf_path = "/etc/fail2ban/jail.conf"
        local_path = "/etc/fail2ban/jail.local"
        if os.path.exists(conf_path) and not os.path.exists(local_path):
            with open(conf_path, "r") as f_src, open(local_path, "w") as f_dst:
                f_dst.write(f_src.read())
            print("✅ Success: Created /etc/fail2ban/jail.local.")
        else:
            print("ℹ️ jail.local already exists or jail.conf not found.")
    except Exception as e:
        print(f"❌ Error creating jail.local: {e}")

def start_fail2ban():
    """Enables and starts fail2ban service."""
    print("🔒 Enabling and starting fail2ban service...")
    try:
        subprocess.run(["systemctl", "enable", "fail2ban"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = subprocess.run(["systemctl", "start", "fail2ban"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            subprocess.run(["service", "fail2ban", "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Success: Fail2ban service enabled and started.")
    except Exception as e:
        print(f"❌ Error starting fail2ban: {e}")