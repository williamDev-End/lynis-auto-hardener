import subprocess

def audit_firewall():
    """Checks UFW firewall status and offers granular hardening options."""
    print("\n--- Granular Firewall (UFW) Hardening Check ---")
    
    res = subprocess.run(["ufw", "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    is_installed = res.returncode == 0
    is_active = "active" in res.stdout.lower() if is_installed else False
    
    print(f"   - UFW Installed: {'✅ Yes' if is_installed else '❌ No'}")
    print(f"   - UFW Active: {'✅ Yes' if is_active else '⚠️ No'}")

    if not is_installed:
        print("⚠️ UFW is not installed on this system.")
        if input("👉 Do you want to install UFW? (y/N): ").strip().lower() == 'y':
            install_ufw()
            is_installed = True
        else:
            print("❌ Skipping firewall installation.")
            return

    changes_made = False

    if not is_active:
        if input("👉 Do you want to enable the UFW firewall? (y/N): ").strip().lower() == 'y':
            enable_ufw()
            changes_made = True

    if input("👉 Do you want to set default secure policies (Deny incoming, Allow outgoing)? (y/N): ").strip().lower() == 'y':
        set_default_policies()
        changes_made = True

    if input("👉 Do you want to explicitly allow SSH port to prevent lockouts? (y/N): ").strip().lower() == 'y':
        allow_ssh_port()
        changes_made = True

    if changes_made:
        print("✅ Firewall hardening applied successfully.")
    else:
        print("ℹ️ No firewall changes selected.")

def install_ufw():
    """Installs UFW package."""
    print("🔒 Installing UFW...")
    try:
        subprocess.run(["apt", "update"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["apt", "install", "-y", "ufw"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Success: UFW installed.")
    except Exception as e:
        print(f"❌ Error installing UFW: {e}")

def enable_ufw():
    """Enables UFW."""
    print("🔒 Enabling UFW...")
    try:
        subprocess.run(["ufw", "enable"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Success: UFW enabled.")
    except Exception as e:
        print(f"❌ Error enabling UFW: {e}")

def set_default_policies():
    """Sets default UFW policies."""
    print("🔒 Setting default firewall policies...")
    try:
        subprocess.run(["ufw", "default", "deny", "incoming"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["ufw", "default", "allow", "outgoing"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Success: Default policies set (Deny incoming / Allow outgoing).")
    except Exception as e:
        print(f"❌ Error setting default policies: {e}")

def allow_ssh_port():
    """Allows SSH port connections."""
    print("🔒 Allowing SSH connections...")
    try:
        subprocess.run(["ufw", "allow", "ssh"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Success: SSH port allowed.")
    except Exception as e:
        print(f"❌ Error allowing SSH: {e}")