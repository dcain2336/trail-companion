"""
Minimal agent loop on top of GemmaClient — reusable scaffold.

The agent gets: a system prompt, a question, and optional local knowledge
files injected as context. No frameworks, no API costs, runs anywhere.
"""

import os
from gemma_client import GemmaClient

DEFAULT_SYSTEM = (
    "You are a helpful assistant powered by Gemma, Google's open-weight model. "
    "Answer concisely and accurately. If the provided reference material does not "
    "contain the answer, say so rather than guessing."
)


def load_knowledge(knowledge_dir):
    """Concatenate all .md files in knowledge_dir as reference context."""
    chunks = []
    if not os.path.isdir(knowledge_dir):
        return ""
    for name in sorted(os.listdir(knowledge_dir)):
        if name.endswith(".md"):
            with open(os.path.join(knowledge_dir, name)) as f:
                chunks.append(f"--- {name} ---\n" + f.read())
    return "\n\n".join(chunks)


class GemmaAgent:
    def __init__(self, system=DEFAULT_SYSTEM, knowledge_dir=None,
                 ollama_model="gemma3"):
        self.client = GemmaClient(ollama_model=ollama_model)
        self.system = system
        self.knowledge = load_knowledge(knowledge_dir) if knowledge_dir else ""

    def ask(self, question):
        prompt = question
        if self.knowledge:
            prompt = (
                "Use the following reference material to answer. "
                "Cite which section you used.\n\n"
                f"REFERENCE MATERIAL:\n{self.knowledge}\n\n"
                f"QUESTION: {question}"
            )
        return self.client.generate(prompt, system=self.system)
