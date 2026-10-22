import subprocess
import os

def audit_system_utils():
    """Checks and offers granular installation of recommended system utilities."""
    print("\n--- Granular Recommended System Utilities Check ---")
    
    utilities = [
        ("libpam-tmpdir", "Ensures sessions have a private /tmp directory."),
        ("needrestart", "Checks which daemons need to be restarted after library upgrades."),
        ("apt-listchanges", "Displays history of changes prior to installation/upgrade.")
    ]
    
    changes_made = False

    for pkg, desc in utilities:
        res = subprocess.run(["dpkg", "-l", pkg], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        is_installed = "ii" in res.stdout
        
        print(f"   - {pkg}: {'✅ Installed' if is_installed else '⚠️ Missing'} ({desc})")
        if not is_installed:
            choice = input(f"     👉 Do you want to install {pkg}? (y/N): ").strip().lower()
            if choice == 'y':
                install_utility(pkg)
                changes_made = True

    if changes_made:
        print("✅ System utilities hardening applied successfully.")
    else:
        print("ℹ️ No system utilities changes selected.")

def install_utility(pkg):
    """Installs a specific utility package."""
    print(f"🔒 Installing {pkg}...")
    try:
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"
        subprocess.run(["apt", "update"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        subprocess.run(["apt", "install", "-y", pkg], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        print(f"✅ Success: {pkg} installed.")
    except Exception as e:
        print(f"❌ Error installing {pkg}: {e}")