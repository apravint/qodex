#!/usr/bin/env python3
import sys
import subprocess
import argparse
from qodex.scanner import run_local_scans
from qodex.reviewer import query_ai_reviewer
from qodex.hook import install_git_hook

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
BOLD = "\033[1m"
NC = "\033[0m"

def main():
    parser = argparse.ArgumentParser(description="Qodex: $0 Open-Source AI Code Reviewer & Secret Leak Gatekeeper")
    parser.add_argument("--gate", action="store_true", help="Fail with non-zero exit code on critical findings (for CI / pre-push)")
    parser.add_argument("--install-hook", action="store_true", help="Install as .git/hooks/pre-push gatekeeper")
    args = parser.parse_args()

    if args.install_hook:
        install_git_hook()
        return

    print(f"{BOLD}{CYAN}🔍 Qodex AI Code Reviewer ($0 Open-Source Gatekeeper){NC}")
    print(f"   Scanning staged changes and commit diff...")

    errors, warnings = run_local_scans()

    print(f"\n{BOLD}1. Local Static & Security Scanners:{NC}")
    if not errors and not warnings:
        print(f"   {GREEN}✓ All local security and syntax checks passed clean (0 leaks, 0 errors).{NC}")
    else:
        for err in errors:
            print(f"   {RED}✗ {err}{NC}")
        for warn in warnings:
            print(f"   {YELLOW}⚠ {warn}{NC}")

    diff_res = subprocess.run(["git", "diff", "HEAD~1"], capture_output=True, text=True)
    if diff_res.returncode != 0:
        diff_res = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    diff_text = diff_res.stdout

    print(f"\n{BOLD}2. AI Deep Logic & Architecture Review:{NC}")
    ai_feedback = query_ai_reviewer(diff_text)
    print(ai_feedback)

    if errors and args.gate:
        print(f"\n{RED}{BOLD}🚨 GATE BLOCKED: Critical issues detected. Resolve errors before pushing.{NC}")
        sys.exit(1)
    else:
        print(f"\n{GREEN}{BOLD}✨ Review complete.{NC}")

if __name__ == "__main__":
    main()
