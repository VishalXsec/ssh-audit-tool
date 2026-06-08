import os

def check_sshd_config(issues_found, results):

    config_file = "/etc/ssh/sshd_config"

    dangerous = {
        "PermitRootLogin yes": "HIGH",
        "PasswordAuthentication yes": "MEDIUM",
        "PermitEmptyPasswords yes": "HIGH",
        "X11Forwarding yes": "LOW"
    }

    if os.path.exists(config_file):

        with open(config_file, "r") as f:

            for line in f:

                if line.strip().startswith("#"):
                    continue

                for key, severity in dangerous.items():

                    if key.lower() in line.lower():

                        print(f"[{severity}] {key}")

                        issues_found += 1

                        results.append({
                            "severity": severity,
                            "check": "sshd_config",
                            "issue": key
                        })

    else:

        print("[i] sshd_config not found")

    return issues_found, results
