import subprocess
import sys
import os

# Import all hardening modules
from modules import ssh
from modules import firewall
from modules import kernel
from modules import auditd
from modules import updates
from modules import security_limits
from modules import permissions
from modules import banners
from modules import fail2ban
from modules import system_utils
from modules import password_rounds
from modules import cron       # <--- Nouveau
from modules import compilers  # <--- Nouveau

def check_root():
    """Ensure the script is executed with root privileges."""
    if os.geteuid() != 0:
        print("❌ Error: This script must be run as root (sudo).")
        sys.exit(1)

def check_lynis():
    """Check if Lynis is installed on the system."""
    try:
        subprocess.run(["lynis", "show", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except FileNotFoundError:
        print("❌ Error: Lynis is not installed.")
        sys.exit(1)

def run_audit(phase_name="INITIAL"):
    """Execute a silent audit with Lynis, extract score, and display top suggestions."""
    print(f"🔍 Starting {phase_name} Lynis system audit...")
    command = ["lynis", "audit", "system", "--quick"]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    score = "Unknown"
    warnings_count = 0
    suggestions_count = 0
    suggestions_list = []
    
    report_path = "/var/log/lynis-report.dat"
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            for line in f:
                if line.startswith("hardening_index="):
                    score = line.split("=")[1].strip()
                elif line.startswith("warning"):
                    warnings_count += 1
                elif line.startswith("suggestion[]="):
                    suggestions_list.append(line.split("=")[1].strip())
                    suggestions_count += 1
    
    print(f"✅ {phase_name} Audit completed!")
    print(f"📊 Hardening Index Score: {score}/100")
    print(f"⚠️ Warnings found: {warnings_count}")
    print(f"💡 Suggestions found: {suggestions_count}\n")

    if suggestions_list and phase_name == "POST-REMEDIATION":
        print("🔍 --- Top Lynis Suggestions for Improvement ---")
        for s in suggestions_list[:5]:
            print(f"   💡 {s}")
        print("------------------------------------------------\n")

def prompt_remediation():
    """Prompts the user independently for each hardening module."""
    print("\n========================================")
    print("       HARDENING & REMEDIATION PHASE    ")
    print("========================================")
    
    if input("👉 Run SSH hardening module? (y/N): ").strip().lower() == 'y':
        ssh.audit_ssh()
    else:
        print("⏭️ Skipping SSH hardening.")

    if input("\n👉 Run Firewall (UFW) hardening module? (y/N): ").strip().lower() == 'y':
        firewall.audit_firewall()
    else:
        print("⏭️ Skipping Firewall hardening.")

    if input("\n👉 Run Kernel hardening module? (y/N): ").strip().lower() == 'y':
        kernel.audit_kernel()
    else:
        print("⏭️ Skipping Kernel hardening.")

    if input("\n👉 Run Auditd hardening module? (y/N): ").strip().lower() == 'y':
        auditd.audit_auditd()
    else:
        print("⏭️ Skipping Auditd hardening.")

    if input("\n👉 Run Automatic Updates hardening module? (y/N): ").strip().lower() == 'y':
        updates.audit_updates()
    else:
        print("⏭️ Skipping Automatic Updates hardening.")

    if input("\n👉 Run Login Policy & Core Dumps hardening module? (y/N): ").strip().lower() == 'y':
        security_limits.audit_security_limits()
    else:
        print("⏭️ Skipping Login Policy hardening.")

    if input("\n👉 Run Sensitive Files Permissions hardening module? (y/N): ").strip().lower() == 'y':
        permissions.audit_permissions()
    else:
        print("⏭️ Skipping Permissions hardening.")

    if input("\n👉 Run OS Banners hardening module? (y/N): ").strip().lower() == 'y':
        banners.audit_banners()
    else:
        print("⏭️ Skipping Banners hardening.")

    if input("\n👉 Run Fail2ban hardening module? (y/N): ").strip().lower() == 'y':
        fail2ban.audit_fail2ban()
    else:
        print("⏭️ Skipping Fail2ban hardening.")

    if input("\n👉 Run Recommended System Utilities module? (y/N): ").strip().lower() == 'y':
        system_utils.audit_system_utils()
    else:
        print("⏭️ Skipping System Utilities hardening.")

    if input("\n👉 Run Password Hashing Rounds hardening module? (y/N): ").strip().lower() == 'y':
        password_rounds.audit_password_rounds()
    else:
        print("⏭️ Skipping Password Rounds hardening.")

    # Nouveaux modules intégrés
    if input("\n👉 Run Cron Permissions hardening module? (y/N): ").strip().lower() == 'y':
        cron.audit_cron()
    else:
        print("⏭️ Skipping Cron hardening.")

    if input("\n👉 Run Compilers Access hardening module? (y/N): ").strip().lower() == 'y':
        compilers.audit_compilers()
    else:
        print("⏭️ Skipping Compilers hardening.")

    print("\n========================================")
    print("          REMEDIATION FINISHED          ")
    print("========================================")
    
    run_audit(phase_name="POST-REMEDIATION")
    
    print("📁 Detailed audit reports can be found here:")
    print("   - Raw report: /var/log/lynis-report.dat")
    print("   - Execution log: /var/log/lynis.log")

if __name__ == "__main__":
    check_root()
    check_lynis()
    run_audit(phase_name="INITIAL")
    prompt_remediation()