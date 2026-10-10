import os
import sys

def install_git_hook():
    """Install qodex into .git/hooks/pre-push"""
    hook_path = ".git/hooks/pre-push"
    if not os.path.exists(".git"):
        print("Error: Must be run inside the root of a git repository.")
        sys.exit(1)

    hook_content = (
        "#!/usr/bin/env bash\n"
        "# Qodex Pre-Push AI Code Review Hook\n"
        "echo -e '\\033[1;34m==> Running Qodex AI Code Review Gatekeeper...\\033[0m'\n"
        "qodex --gate || {\n"
        "    echo -e '\\033[1;31m[PUSH REJECTED] Qodex review gate failed. Fix errors above before pushing.\\033[0m'\n"
        "    exit 1\n"
        "}\n"
    )
    with open(hook_path, "w") as f:
        f.write(hook_content)
    os.chmod(hook_path, 0o755)
    print(f"✓ Successfully installed pre-push gatekeeper hook at {hook_path}")
