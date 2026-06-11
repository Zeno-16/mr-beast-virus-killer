import os
import re
import sys
import ctypes

sys.stdout.reconfigure(encoding='utf-8')



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("[*] Requesting Administrator privileges...")
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        '"' + os.path.abspath(__file__) + '"',
        None,
        1
    )
    sys.exit()



SUSPICIOUS_KEYWORDS = [
    b"powershell",
    b"cscript",
    b"wscript",
    b"CreateObject(\"WScript.Shell\")",
    b"FromBase64String",
    b"ExecutionPolicy Bypass"
]

PROJECT_EXTENSIONS = ['.vcxproj', '.csproj']



def sanitize_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()

        original_content = content
        findings = []

        is_project = any(filepath.endswith(ext) for ext in PROJECT_EXTENSIONS)

        if is_project:
            pattern = re.compile(
                b'(?i)<PreBuildEvent>.*?</PreBuildEvent>|'
                b'<PostBuildEvent>.*?</PostBuildEvent>|'
                b'<Target\\s+[^>]*>.*?</Target>',
                re.DOTALL
            )

            def replacer(match):
                block = match.group(0)
                is_malicious = False

                for kw in SUSPICIOUS_KEYWORDS:
                    if kw.lower() in block.lower():
                        is_malicious = True
                        break

                if re.search(b'[A-Za-z0-9+/=]{300,}', block):
                    is_malicious = True

                if is_malicious:
                    findings.append(
                        "Deleted: Build Event/Target containing suspicious PowerShell or Base64 payload"
                    )
                    return b""

                return block

            content = pattern.sub(replacer, content)

        if content != original_content:
            with open(filepath, 'wb') as f:
                f.write(content)

            print(f"\n[+] Cleaned: {filepath}")

            for find in findings:
                print(f"    -> {find}")

            return 1

        return 0

    except Exception:
        return 0


def main():
    print("=" * 60)
    print(" vcxproj and csproj rats cleaner")
    print(" Made by Nam and Trong")
    print(" Reminder: After you cleaned the rats use this or it will comeback!")
    print("=" * 60)

    drives_to_scan = [
        'D:\\',
        'C:\\',
        'E:\\'
    ]

    total_infected = 0
    total_scanned = 0

    print("\n[*] Starting scan...")

    for target_dir in drives_to_scan:
        if not os.path.exists(target_dir):
            continue

        print(f"\n[>>>] Scanning drive {target_dir}")

        for root, dirs, files in os.walk(target_dir):
            for file in files:
                ext = os.path.splitext(file)[1].lower()

                if ext in PROJECT_EXTENSIONS:
                    filepath = os.path.join(root, file)

                    total_scanned += 1
                    total_infected += sanitize_file(filepath)

    print("\n" + "=" * 60)
    print(f"[*] Scan Complete")
    print(f"[*] Project files scanned: {total_scanned}")
    print(f"[*] Files cleaned: {total_infected}")
    print("=" * 60)

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()