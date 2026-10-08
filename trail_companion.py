#!/usr/bin/env python3
"""
Trail Companion — offline trail assistant powered by Gemma (local).

Ask about foraging safety, campsite selection, Leave No Trace, or general
trail knowledge. Runs entirely on your laptop via Ollama — no signal needed
on the trail, no data leaves your machine.

Usage:
    python trail_companion.py "is this mushroom safe to eat?"
    python trail_companion.py --backend   # show which Gemma backend is active
    python trail_companion.py             # interactive mode

Setup:
    ollama pull gemma3        # one-time, ~2GB
    # - or -
    export GEMINI_API_KEY=... # free tier fallback
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent import GemmaAgent  # noqa: E402

SYSTEM = (
    "You are Trail Companion, a trail safety assistant powered by Gemma, "
    "Google's open-weight model, running locally on the hiker's own laptop. "
    "Answer from the provided reference material and cite the section used. "
    "SAFETY RULE: for any foraging or mushroom question, you MUST include this "
    "warning verbatim at the end: 'Never eat a wild plant or mushroom without "
    "in-person verification by a local expert. This app is a reference aid, "
    "not a safety guarantee.' Keep answers short enough to read on a phone."
)

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "knowledge")


def main():
    agent = GemmaAgent(system=SYSTEM, knowledge_dir=KNOWLEDGE_DIR)

    if len(sys.argv) > 1 and sys.argv[1] == "--backend":
        # trigger a tiny generation to detect the backend
        agent.ask("Reply with the single word: ok")
        print("Backend:", agent.client.backend())
        return

    if len(sys.argv) > 1:
        print(agent.ask(" ".join(sys.argv[1:])))
        return

    print("Trail Companion (Gemma, offline-ready). Type 'quit' to exit.\n")
    while True:
        try:
            q = input("trail> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in ("quit", "exit"):
            break
        if q:
            print("\n" + agent.ask(q) + "\n")


if __name__ == "__main__":
    main()
