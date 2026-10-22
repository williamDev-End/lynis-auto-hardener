import os

def audit_banners():
    """Checks and offers granular hardening and rollback for OS and issue banners."""
    print("\n--- Granular OS Banners Hardening & Rollback Check ---")
    
    banner_files = ["/etc/issue", "/etc/issue.net", "/etc/motd"]
    changes_made = False

    for filepath in banner_files:
        if os.path.exists(filepath):
            # Check if file is empty
            is_empty = os.path.getsize(filepath) == 0
            print(f"   - {filepath}: {'Empty (Secured)' if is_empty else 'Contains content (Default)'}")
            
            choice = input(f"     👉 Action: [y] Clear/Secure (empty) | [r] Restore default (generic text) | [N] Skip: ").strip().lower()
            if choice == 'y':
                clear_banner_file(filepath)
                changes_made = True
            elif choice == 'r':
                restore_banner_file(filepath)
                changes_made = True
        else:
            print(f"   - {filepath}: not found")

    if changes_made:
        print("✅ Banners hardening & rollback applied successfully.")
    else:
        print("ℹ️ No banner changes selected.")

def clear_banner_file(filepath):
    """Empties a banner file to prevent OS version leaking."""
    print(f"🔒 Clearing {filepath}...")
    try:
        with open(filepath, "w") as f:
            f.write("")
        print(f"✅ Success: {filepath} cleared.")
    except Exception as e:
        print(f"❌ Error clearing {filepath}: {e}")

def restore_banner_file(filepath):
    """Restores a generic default banner text."""
    print(f"🔒 Restoring default text for {filepath}...")
    try:
        default_text = "Authorized access only.\n" if "issue" in filepath else "Welcome.\n"
        with open(filepath, "w") as f:
            f.write(default_text)
        print(f"✅ Success: Default banner restored for {filepath}.")
    except Exception as e:
        print(f"❌ Error restoring {filepath}: {e}")