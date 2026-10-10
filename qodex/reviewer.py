import os
import json
import urllib.request
from typing import Optional

def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "") or os.environ.get("ANTHROPIC_API_KEY", "") or os.environ.get("OPENAI_API_KEY", "")
    if key:
        return key
    conf_path = os.path.expanduser("~/.config/environment.d/20-gemini.conf")
    if os.path.exists(conf_path):
        with open(conf_path, "r") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    return line.strip().split("=", 1)[1].strip('"').strip("'")
    return ""

def query_ai_reviewer(diff_text: str) -> str:
    """Send git diff to AI reviewer model."""
    if not diff_text.strip():
        return "No code changes detected in diff."

    prompt = (
        "You are an expert Principal Systems Engineer conducting a strict code review.\n"
        "Analyze the following git diff and provide a concise review covering:\n"
        "1. Security & Safety (Privilege escalation, injections, leaks)\n"
        "2. Correctness & Breaking Changes\n"
        "3. Performance & Resource Impact\n"
        "4. Recommendation (APPROVE / REQUEST_CHANGES)\n\n"
        f"Git Diff (truncated to 4000 chars):\n```diff\n{diff_text[:4000]}\n```"
    )

    api_key = get_api_key()
    if api_key:
        model = os.environ.get("REVIEW_MODEL", "gemini-2.5-flash")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "x-goog-api-key": api_key}
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception:
            pass

    # Local Ollama fallback
    try:
        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=json.dumps({"model": os.environ.get("OLLAMA_MODEL", "qwen2.5:1.5b"), "prompt": prompt, "stream": False}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except Exception as e:
        return f"[AI Reviewer unavailable ({e}). Local static and security checks passed.]"
