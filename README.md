# 🛡️ Lynis Auto Hardener

**Lynis Auto Hardener** is a modular, interactive Python-based security hardening and auditing assistant for Linux systems. Designed with a "human-in-the-loop" approach, it allows administrators to audit security parameters, apply granular hardening rules, or roll back to default states module by module.

---

## 📂 Project Structure

```text
lynis-auto-hardener/
│
├── auditor.py             # Main execution script
└── modules/
    ├── __init__.py
    ├── auditd.py          # Auditd configuration checks
    ├── banners.py         # OS and login banners cleanup & restoration
    ├── compilers.py       # Restrict compiler execution permissions
    ├── cron.py            # Cron files & directories permissions hardening
    ├── fail2ban.py        # Fail2ban installation & local jail setup
    ├── firewall.py        # Firewall configurations
    ├── kernel.py          # Kernel & network sysctl hardening
    ├── password_rounds.py # Secure password hashing rounds (SHA-512)
    ├── permissions.py     # Sensitive system files permissions (/etc/shadow, etc.)
    ├── security_limits.py # Password aging and core dumps restrictions
    ├── ssh.py             # SSH daemon hardening (Root login, auth methods)
    ├── system_utils.py    # Recommended system utils (libpam-tmpdir, etc.)
    └── updates.py         # Unattended upgrades configuration
```

---

## ✨ Key Features

* **Granular Control:** Inspects system states individually and prompts for action rather than applying blind, sweeping changes.
* **Rollback / Restore Support:** For critical configuration modules, you can choose to apply security hardening (`y`), restore system default values (`r`), or skip (`N`).
* **Modular Architecture:** Clean separation of concerns with dedicated Python modules for each security domain.
* **Interactive CLI:** Clear visual feedback (`✅ Secured`, `⚠️ Insecure`, status indicators) to guide the administrator.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.x
* Root privileges (required to audit system files, modify configurations, and manage services).

### Installation

Clone the repository to your target Linux machine:

```bash
git clone [https://github.com/YOUR_USERNAME/lynis-auto-hardener.git](https://github.com/YOUR_USERNAME/lynis-auto-hardener.git)
cd lynis-auto-hardener
```

### Usage

Run the main auditor script with `sudo` permissions:

```bash
sudo python3 auditor.py
```

For each module, you will be presented with interactive choices:
* **`y`** : Apply the recommended security hardening.
* **`r`** : Restore the system default state (Rollback).
* **`N`** : Skip the current item.

---

## 🛠️ Modules Overview

1. **SSH Hardening (`ssh.py`)**: Restricts root login and enforces key-based authentication with rollback options.
2. **Sensitive Permissions (`permissions.py`)**: Secures critical files like `/etc/shadow`, `/etc/passwd`, and `/etc/group`.
3. **Kernel & Network (`kernel.py`)**: Configures sysctl parameters (SYN cookies, source routing, reverse path filtering).
4. **Security Limits (`security_limits.py`)**: Manages password maximum aging (`PASS_MAX_DAYS`) and core dumps restriction.
5. **Banners (`banners.py`)**: Clears OS version info from issue and MOTD files to prevent information disclosure.
6. **Cron Permissions (`cron.py`)**: Locks down cron directories and files permissions.
7. **Fail2ban (`fail2ban.py`)**: Installs and configures brute-force protection.
8. **System Utilities (`system_utils.py`)**: Ensures privacy in `/tmp` and installs safety tools like `needrestart`.

---

## ⚠️ Disclaimer

This tool is designed for educational and administrative hardening purposes. Always test hardening scripts in a staging or non-production environment before deploying them to production servers. The authors assume no responsibility for locked-out access or service disruptions.

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).