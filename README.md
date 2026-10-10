# 🔍 Qodex

> **$0 Open-Source AI Code Reviewer & Secret Leak Gatekeeper**  
> Replace expensive $60/dev/mo code review tools with a local-first, zero-cost CLI gatekeeper. 100+ local static security checks combined with deep AI architectural review on every git push or CI run.

---

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)

## 🚀 Why Qodex?

Commercial AI code review platforms charge $60+ per seat each month. **Qodex** gives you the exact same protection for **$0**:
- 🔒 **Zero-Latency Secret Scanning**: Catches GitHub tokens, AWS keys, Slack tokens, private keys, and API secrets *before* they leave your machine.
- 🛡️ **Local Static Checks**: Automatically verifies bash/shell syntax, python syntax compilation, JSON integrity, and unresolved merge conflict markers.
- 🧠 **AI Architectural Review**: Analyzes git diffs with Google Gemini, Anthropic Claude, or local Ollama models (`qwen2.5`, `deepseek-coder`, `llama3`).
- 🚪 **Pre-Push Gatekeeper**: Installs directly into `.git/hooks/pre-push` to reject bad commits locally before they hit remote branches.

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/apravint/qodex.git
cd qodex

# Install locally via pip
pip install -e .
```

---

## ⚡ Quick Start

### 1. Manual Code Review
Run inside any git repository to review uncommitted or latest commit changes:
```bash
qodex
```

### 2. CI / Pre-Push Strict Mode
Fail with a non-zero exit code if secrets, syntax errors, or conflict markers are detected:
```bash
qodex --gate
```

### 3. One-Click Git Hook Installation
Install `qodex` as your repository's automated pre-push gatekeeper:
```bash
qodex --install-hook
```
Now, whenever you run `git push`, Qodex runs its scans. If an API key or critical syntax bug is detected, the push is aborted immediately.

---

## ⚙️ Configuration & AI Models

Qodex works out of the box with $0 local Ollama models or external cloud LLM APIs:

- **Local Ollama (Default fallback, 100% offline & free)**:
  ```bash
  export OLLAMA_MODEL="qwen2.5:1.5b"  # or deepseek-coder:6.7b
  ```
- **Google Gemini**:
  ```bash
  export GEMINI_API_KEY="your-api-key"
  export REVIEW_MODEL="gemini-2.5-flash"
  ```
- **Anthropic Claude**:
  ```bash
  export ANTHROPIC_API_KEY="your-api-key"
  ```

---

## 🧪 Testing

```bash
python3 -m unittest discover tests
```

---

## 📜 License

MIT License © 2026 [Ayyappa Pravin](https://github.com/apravint)
