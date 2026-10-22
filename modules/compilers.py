import os

def audit_compilers():
    """Checks and offers granular restrictions on system compilers permissions."""
    print("\n--- Granular Compilers Access Hardening Check ---")
    
    compilers = ["/usr/bin/gcc", "/usr/bin/g++", "/usr/bin/make"]
    changes_made = False

    for comp in compilers:
        if os.path.exists(comp):
            stat = os.stat(comp)
            is_world_executable = (stat.st_mode & 0o001) != 0
            current_perm = oct(stat.st_mode)[-4:]
            
            print(f"   - {comp}: current permissions {current_perm} (world-executable: {'⚠️ Yes' if is_world_executable else '✅ No'})")
            
            if is_world_executable:
                choice = input(f"     👉 Do you want to restrict execution permissions for {comp}? (y/N): ").strip().lower()
                if choice == 'y':
                    apply_compiler_hardening(comp)
                    changes_made = True
        else:
            print(f"   - {comp}: not found")

    if changes_made:
        print("✅ Compilers hardening applied successfully.")
    else:
        print("ℹ️ No compiler permission changes selected.")

def apply_compiler_hardening(comp):
    """Removes execution rights for others on a compiler binary."""
    print(f"🔒 Restricting execution permissions on {comp}...")
    try:
        current_mode = os.stat(comp).st_mode
        new_mode = current_mode & ~0o001
        os.chmod(comp, new_mode)
        print(f"✅ Success: Permissions restricted for {comp}.")
    except Exception as e:
        print(f"❌ Error restricting {comp}: {e}")