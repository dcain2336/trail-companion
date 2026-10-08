"""
Gemma unified client — reusable scaffold for Hacktoberfest 2026 entries.

Supports two free backends, tried in order:
  1. Ollama (local): http://localhost:11434, model "gemma3"
     - Fully offline, no API key, no cost. `ollama pull gemma3`
  2. Gemini API (free tier): https://generativelanguage.googleapis.com
     - Gemma models served via the Gemini API. Needs GEMINI_API_KEY env var.
     - Get a free key at https://aistudio.google.com/apikey

Only dependency: `requests`.
"""

import json
import os
import urllib.request
import urllib.error


def _ollama_generate(prompt, model="gemma3", timeout=120):
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(
            {"model": model, "prompt": prompt, "stream": False}
        ).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())["response"], "ollama:" + model
    except (urllib.error.URLError, OSError, KeyError):
        return None, None


def _gemini_api_generate(prompt, model="gemma-3-27b-it", timeout=120):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return None, None
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={key}"
    )
    body = json.dumps(
        {"contents": [{"parts": [{"text": prompt}]}]}
    ).encode()
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text, "gemini-api:" + model
    except (urllib.error.URLError, OSError, KeyError, IndexError):
        return None, None


class GemmaClient:
    """Try local Ollama first, fall back to Gemini API free tier."""

    def __init__(self, ollama_model="gemma3", api_model="gemma-3-27b-it"):
        self.ollama_model = ollama_model
        self.api_model = api_model
        self.last_backend = None

    def generate(self, prompt, system=None, timeout=120):
        full = f"{system}\n\n{prompt}" if system else prompt
        text, backend = _ollama_generate(full, self.ollama_model, timeout)
        if text is None:
            text, backend = _gemini_api_generate(full, self.api_model, timeout)
        if text is None:
            raise RuntimeError(
                "No Gemma backend available. Start Ollama (`ollama pull gemma3`) "
                "or set GEMINI_API_KEY."
            )
        self.last_backend = backend
        return text.strip()

    def backend(self):
        return self.last_backend or "none (call generate first)"
