import os
import subprocess

def audit_kernel():
    """Checks and offers granular kernel and network hardening and rollback options (sysctl)."""
    print("\n--- Granular Kernel & Network Hardening & Rollback Check ---")
    
    sysctl_conf = "/etc/sysctl.conf"
    if not os.path.exists(sysctl_conf):
        print("ℹ️ sysctl.conf not found. Skipping kernel checks.")
        return

    with open(sysctl_conf, "r") as f:
        content = f.read()

    syncookies_active = "net.ipv4.tcp_syncookies = 1" in content
    source_route_active = "net.ipv4.conf.all.accept_source_route = 0" in content
    rp_filter_active = "net.ipv4.conf.all.rp_filter = 1" in content

    print(f"   - TCP SYN Cookies Enabled: {'✅ Yes' if syncookies_active else '⚠️ No'}")
    print(f"   - Source Route Disabled: {'✅ Yes' if source_route_active else '⚠️ No'}")
    print(f"   - Reverse Path Filtering Enabled: {'✅ Yes' if rp_filter_active else '⚠️ No'}")

    changes_made = False

    # 1. TCP SYN Cookies
    print(f"   - TCP SYN Cookies (Target: 1 | Default/Restore: 0)")
    choice_sync = input("     👉 Action: [y] Secure (1) | [r] Restore default (0) | [N] Skip: ").strip().lower()
    if choice_sync == 'y':
        update_sysctl("net.ipv4.tcp_syncookies", "1", sysctl_conf)
        changes_made = True
    elif choice_sync == 'r':
        update_sysctl("net.ipv4.tcp_syncookies", "0", sysctl_conf)
        changes_made = True

    # 2. IP Source Routing
    print(f"   - IP Source Routing (Target: 0 [Disabled] | Default/Restore: 1 [Enabled])")
    choice_src = input("     👉 Action: [y] Secure (0) | [r] Restore default (1) | [N] Skip: ").strip().lower()
    if choice_src == 'y':
        update_sysctl("net.ipv4.conf.all.accept_source_route", "0", sysctl_conf)
        update_sysctl("net.ipv4.conf.default.accept_source_route", "0", sysctl_conf)
        changes_made = True
    elif choice_src == 'r':
        update_sysctl("net.ipv4.conf.all.accept_source_route", "1", sysctl_conf)
        update_sysctl("net.ipv4.conf.default.accept_source_route", "1", sysctl_conf)
        changes_made = True

    # 3. Reverse Path Filtering
    print(f"   - Reverse Path Filtering (Target: 1 | Default/Restore: 0)")
    choice_rp = input("     👉 Action: [y] Secure (1) | [r] Restore default (0) | [N] Skip: ").strip().lower()
    if choice_rp == 'y':
        update_sysctl("net.ipv4.conf.all.rp_filter", "1", sysctl_conf)
        update_sysctl("net.ipv4.conf.default.rp_filter", "1", sysctl_conf)
        changes_made = True
    elif choice_rp == 'r':
        update_sysctl("net.ipv4.conf.all.rp_filter", "0", sysctl_conf)
        update_sysctl("net.ipv4.conf.default.rp_filter", "0", sysctl_conf)
        changes_made = True

    if changes_made:
        reload_sysctl()
        print("✅ Kernel hardening & rollback applied successfully.")
    else:
        print("ℹ️ No kernel changes selected.")

def update_sysctl(key, value, config_path):
    """Appends or updates a sysctl parameter in sysctl.conf."""
    try:
        with open(config_path, "r") as f:
            lines = f.readlines()

        updated = False
        new_lines = []
        for line in lines:
            if line.strip().startswith(key) and not line.strip().startswith("#"):
                new_lines.append(f"{key} = {value}\n")
                updated = True
            else:
                new_lines.append(line)

        if not updated:
            new_lines.append(f"{key} = {value}\n")

        with open(config_path, "w") as f:
            f.writelines(new_lines)
        print(f"✅ Success: Set {key} = {value}.")
    except Exception as e:
        print(f"❌ Error updating {key}: {e}")

def reload_sysctl():
    """Reloads sysctl active parameters."""
    print("🔒 Reloading kernel parameters...")
    try:
        subprocess.run(["sysctl", "-p"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Success: Kernel parameters reloaded.")
    except Exception as e:
        print(f"❌ Error reloading sysctl: {e}")