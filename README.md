# Trail Companion — offline trail assistant powered by Gemma

Built for the **Hacktoberfest 2026 Week 1 Challenge** ("Touch Grass") on DEV.
Prize categories entered: **Best Use of Gemma**.

## What it is

A command-line trail companion that answers foraging-safety, campsite, and
Leave No Trace questions — running **entirely offline** on your laptop via
[Gemma](https://deepmind.google/technologies/gemma/) (Google's open-weight
model) served locally through [Ollama](https://ollama.com).

The whole point: it works on the trail with **zero signal**. No cloud, no API
key, no subscription, no data leaving your machine. That is only possible
because Gemma's weights are open — you can carry the model in your backpack.

## Why Gemma (Best Use of Gemma)

- **Local inference:** `gemma3` via Ollama. The model file lives on disk;
  inference happens on-device. Try that with a closed API model.
- **Free fallback:** if Ollama isn't running, it uses Gemma through the
  Gemini API free tier (`gemma-3-27b-it`) — same code path, no changes.
- **Safety-critical local knowledge:** foraging answers are grounded in a
  bundled reference (poisonous lookalikes, mushroom rules) and every foraging
  answer ends with a mandatory expert-verification warning.

## Setup

```bash
ollama pull gemma3          # one-time download (~2GB)
pip install -r requirements.txt
```

Or without Ollama:

```bash
export GEMINI_API_KEY=your_free_key   # https://aistudio.google.com/apikey
pip install -r requirements.txt
```

## Usage

```bash
python trail_companion.py "is this white mushroom safe to eat?"
python trail_companion.py --backend     # show which Gemma backend is active
python trail_companion.py              # interactive mode
python demo.py                          # scripted demo (3 sample questions)
```

## Project layout

- `trail_companion.py` — CLI + safety-prompt wiring
- `agent.py` — minimal Gemma agent loop with local knowledge injection
- `gemma_client.py` — unified client: Ollama local first, Gemini API fallback
- `knowledge/` — bundled trail reference (foraging safety, camping, Leave No Trace)
- `demo.py` — scripted demo for the write-up

## Why open innovation matters here

A trail safety tool that phones home to a cloud API is useless exactly when
you need it most — no bars, no answers. Open weights flip that: the
intelligence lives on the device, in the woods, with you. Open also means
auditable: the safety prompts and knowledge base are plain files anyone can
inspect, correct, and improve. For safety-critical advice, that transparency
isn't a nice-to-have, it's the whole game.
