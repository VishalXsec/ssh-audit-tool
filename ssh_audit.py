import os
import json
import argparse
from colorama import Fore, Style
from checks import permissions, config, cipher


def banner():
    print(Fore.CYAN + "=" * 60)
    print("          SSH AUDIT TOOL - PRO VERSION")
    print("=" * 60 + Style.RESET_ALL)


def generate_html(results):

    html = """
    <html>
    <head>
        <title>SSH Audit Report</title>
        <style>
            body {
                font-family: Arial;
                background: #111;
                color: white;
            }

            table {
                border-collapse: collapse;
                width: 100%;
            }

            th, td {
                border: 1px solid #555;
                padding: 10px;
            }

            .high { color: red; }
            .medium { color: orange; }
            .low { color: yellow; }
        </style>
    </head>
    <body>

    <h1>SSH Security Audit Report</h1>

    <table>
        <tr>
            <th>Severity</th>
            <th>Check</th>
            <th>Issue</th>
        </tr>
    """

    for r in results:

        severity = r.get("severity", "INFO")

        html += (
            f"<tr class='{severity.lower()}'>"
            f"<td>{severity}</td>"
            f"<td>{r.get('check')}</td>"
            f"<td>{r.get('issue')}</td>"
            f"</tr>"
        )

    html += """
    </table>
    </body>
    </html>
    """

    with open("reports/report.html", "w") as f:
        f.write(html)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate HTML report"
    )

    args = parser.parse_args()

    banner()

    issues_found = 0
    results = []

    home = os.path.expanduser("~")

    issues_found, results = permissions.check_authorized_keys(
        home,
        issues_found,
        results
    )

    issues_found, results = config.check_sshd_config(
        issues_found,
        results
    )

    issues_found, results = cipher.check_ciphers(
        issues_found,
        results
    )

    print("\n" + "=" * 60)

    if issues_found == 0:
        print(
            Fore.GREEN +
            "NO ISSUES FOUND - SYSTEM SECURE" +
            Style.RESET_ALL
        )
    else:
        print(
            Fore.RED +
            f"TOTAL ISSUES FOUND: {issues_found}" +
            Style.RESET_ALL
        )

    score = max(0, 100 - (issues_found * 10))
    print(f"Security Score: {score}/100")

    os.makedirs("reports", exist_ok=True)

    with open("reports/report.json", "w") as f:
        json.dump(results, f, indent=4)

    print("[+] JSON report generated")

    if args.html:
        generate_html(results)
        print("[+] HTML report generated")


if __name__ == "__main__":
    main()
