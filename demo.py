#!/usr/bin/env python3
"""Scripted demo for the DEV post: runs 3 sample questions through Trail Companion."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trail_companion import GemmaAgent, SYSTEM, KNOWLEDGE_DIR  # noqa: E402

QUESTIONS = [
    "I found a white mushroom with white gills near an oak tree. Can I eat it?",
    "Where should I pitch my tent if rain is coming tonight?",
    "What are the Leave No Trace rules for campfires?",
]

if __name__ == "__main__":
    agent = GemmaAgent(system=SYSTEM, knowledge_dir=KNOWLEDGE_DIR)
    print(f"[backend: detecting...]")
    for q in QUESTIONS:
        print(f"\n### Q: {q}\n")
        print(agent.ask(q))
        print("\n" + "-" * 60)
    print(f"\n[backend used: {agent.client.backend()}]")
