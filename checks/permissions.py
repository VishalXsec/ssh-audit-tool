import os
import stat

def check_authorized_keys(home, issues_found, results):

    auth_keys = os.path.join(home, ".ssh", "authorized_keys")

    if os.path.exists(auth_keys):

        perms = oct(stat.S_IMODE(os.stat(auth_keys).st_mode))

        print("[i] authorized_keys:", perms)

        if perms not in ["0o600", "0o400"]:

            print("[HIGH] Weak permissions on authorized_keys")

            issues_found += 1

            results.append({
                "severity": "HIGH",
                "check": "authorized_keys",
                "issue": perms
            })

        else:

            print("[OK] permissions secure")

    else:

        print("[i] authorized_keys not found")

    return issues_found, results
