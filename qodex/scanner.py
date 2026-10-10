import os
import re
import json
import subprocess
from typing import List, Tuple

SECRET_PATTERNS = [
    (r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_-]{20,}['\"]", "Potential API Key"),
    (r"(?i)secret[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_-]{20,}['\"]", "Potential Secret Key"),
    (r"AIza[0-9A-Za-z-_]{35}", "Google API Key"),
    (r"ghp_[0-9a-zA-Z]{36}", "GitHub Personal Access Token"),
    (r"xox[baprs]-[0-9a-zA-Z]{10,48}", "Slack Token"),
    (r"-----BEGIN\s+(RSA|OPENSSH|PRIVATE)\s+KEY-----", "Private Cryptographic Key"),
    (r"sk-[a-zA-Z0-9]{20,}", "OpenAI / Cloud Secret Key"),
]

def run_local_scans() -> Tuple[List[str], List[str]]:
    """
    Run $0 local security and syntax checks across modified files.
    Returns (errors, warnings).
    """
    errors = []
    warnings = []

    # Get changed files
    res = subprocess.run(["git", "diff", "--name-only", "HEAD~1"], capture_output=True, text=True)
    if res.returncode != 0:
        res = subprocess.run(["git", "diff", "--name-only", "--cached"], capture_output=True, text=True)
    files = [f.strip() for f in res.stdout.splitlines() if f.strip() and os.path.exists(f.strip())]

    # Get diff text for secret scanning
    diff_res = subprocess.run(["git", "diff", "HEAD~1"], capture_output=True, text=True)
    if diff_res.returncode != 0:
        diff_res = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    diff_text = diff_res.stdout

    # 1. Secret Scanning on diff
    for pattern, desc in SECRET_PATTERNS:
        matches = re.findall(pattern, diff_text)
        if matches:
            errors.append(f"🔒 Secret Leak Detected: {desc} (Match: {matches[0][:15]}...)")

    # 2. Merge Conflict Markers
    for line in diff_text.splitlines():
        if line.startswith("+<<<<<<< ") or line.startswith("+=======") or line.startswith("+>>>>>>> "):
            errors.append("⚔️ Unresolved Git Merge Conflict Markers found in added lines")
            break

    # 3. File Syntax Checks
    for f in files:
        # Bash / Shell scripts
        if f.endswith(".sh") or f.startswith("bin/"):
            try:
                with open(f, "rb") as fh:
                    first_line = fh.readline()
                if b"bash" in first_line or b"sh" in first_line:
                    chk = subprocess.run(["bash", "-n", f], capture_output=True, text=True)
                    if chk.returncode != 0:
                        errors.append(f"🐚 Shell syntax error in {f}: {chk.stderr.strip()}")
            except Exception:
                pass

        # Python scripts
        if f.endswith(".py"):
            try:
                chk = subprocess.run(["python3", "-m", "py_compile", f], capture_output=True, text=True)
                if chk.returncode != 0:
                    errors.append(f"🐍 Python syntax compilation error in {f}: {chk.stderr.strip()}")
            except Exception:
                pass

        # JSON files
        if f.endswith(".json"):
            try:
                with open(f, "r") as fh:
                    json.load(fh)
            except Exception as e:
                errors.append(f"📄 JSON parse error in {f}: {e}")

        # Check binary file sizes (> 15MB)
        try:
            if os.path.getsize(f) > 15 * 1024 * 1024 and not f.endswith(".iso"):
                warnings.append(f"📦 Large file detected (>15MB): {f}")
        except Exception:
            pass

    return errors, warnings
