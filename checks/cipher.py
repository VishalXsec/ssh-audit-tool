import subprocess

def check_ciphers(issues_found, results):

    try:

        output = subprocess.check_output(
            ["ssh", "-Q", "cipher"],
            text=True
        )

        weak = {
            "3des-cbc": "HIGH",
            "arcfour": "HIGH"
        }

        for w, sev in weak.items():

            if w in output:

                print(f"[{sev}] Weak cipher: {w}")

                issues_found += 1

                results.append({
                    "severity": sev,
                    "check": "cipher",
                    "issue": w
                })

    except Exception as e:

        print("[!] Cipher check failed:", e)

    return issues_found, results
