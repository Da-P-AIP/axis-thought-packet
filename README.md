# Axis Thought Packet

[![PyPI version](https://img.shields.io/pypi/v/axis-thought-packet.svg)](https://pypi.org/project/axis-thought-packet/)
[![Python](https://img.shields.io/pypi/pyversions/axis-thought-packet.svg)](https://pypi.org/project/axis-thought-packet/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20116884.svg)](https://doi.org/10.5281/zenodo.20116884)

**A coordinate system for AI self-awareness — knowing where you are in thought space.**

Axis Thought Packet is a structured thought-state representation format for human-AI and multi-agent collaboration. Model-agnostic: works with Claude, GPT, Gemini, or any LLM.

---

## Install

```bash
pip install axis-thought-packet
```

---

## The Problem

Every AI session starts from zero.  
You re-explain context. The AI re-builds understanding. Thought state is lost.

Axis Thought Packet solves this by treating **thought as a portable, structured object** — with coordinates, history, and intent — that can be passed between sessions, agents, and models.

---

## Quick Start

```python
from axis_thought_packet import ThoughtPacket

# Create a thought packet
packet = ThoughtPacket(
    focus="Build a model-agnostic thought protocol",
    intent="Enable AI self-positioning across sessions",
    confidence=0.85,
    subject="Axis Thought Packet",
    context="Multi-agent AI collaboration"
)

# Where am I in thought-space?
print(packet.position)
# → {'clarity': 1.0, 'confidence': 0.85, 'novelty': 0.5, 'completeness': 0.75}

# Generate a resumption prompt — paste into ANY AI
print(packet.to_prompt())
# → ## Axis Thought Packet — Context Handoff
#   **Focus**: Build a model-agnostic thought protocol
#   **Intent**: Enable AI self-positioning across sessions
#   ...

# Save and reload across sessions
packet.save("my_session.atp")
reloaded = ThoughtPacket.load("my_session.atp")
```

---

## Core Concepts

### Universal Formula

Axis Thought Packet is based on the **Universal Formula** framework, which treats thinking as three operations:

```
Thought = State × Transition × Translation
```

| Component | Description | In code |
|-----------|-------------|---------|
| **State** | What the AI knows and intends right now | `thought_state` |
| **Transition** | How the state is evolving | `transition` |
| **Translation** | How to hand off to another agent or session | `to_prompt()` |

### Thought Position

Every packet has a **position** in thought-space — a coordinate vector that answers:
*"Where am I right now as a thinking agent?"*

```python
packet.position
# {
#   "clarity":      0.85,  # how well-defined is the focus?
#   "confidence":   0.90,  # how confident is the intent?
#   "novelty":      0.50,  # how unexplored is the territory?
#   "completeness": 0.75   # how much context is filled in?
# }
```

This is the key insight: **AI can know where it is in thought-space**, not just what it's saying.

---

## Features

### ThoughtPacket — Core object

```python
from axis_thought_packet import ThoughtPacket

packet = ThoughtPacket(
    focus="...",          # what are we thinking about?
    intent="...",         # why are we thinking about it?
    confidence=0.8,       # how sure are we?
    subject="...",        # topic domain
    context="...",        # situational context
    stance="...",         # current stance or angle
    to_state="...",       # where are we headed?
    tags=["research"]     # free-form labels
)
```

### ThoughtLens — Perspective transformer

View the same thought through different lenses:

```python
from axis_thought_packet import ThoughtLens

critic   = ThoughtLens("critic")       # reduces confidence, adds scrutiny
engineer = ThoughtLens("implementer")  # shifts toward practical execution
user     = ThoughtLens("user")         # reframes around usability

critical_view = critic.apply(packet)
print(critical_view.thought_state.confidence)  # lower than original
```

Built-in lenses: `critic`, `implementer`, `user`, `summarizer`

### Multi-agent handoff

```python
from axis_thought_packet.utils import merge_packets

agent_1 = ThoughtPacket(focus="Defined schema", intent="Establish format", confidence=0.9)
agent_2 = ThoughtPacket(focus="Wrote tests",   intent="Verify behavior",  confidence=0.85)
agent_3 = ThoughtPacket(focus="Shipped v0.1",  intent="Public release",   confidence=0.95)

final = merge_packets(agent_1, agent_2, agent_3)
# → merged focus, averaged confidence, combined tags
```

### Thought evolution diff

```python
from axis_thought_packet.utils import diff_packets

before = ThoughtPacket(focus="Idea stage",          confidence=0.4)
after  = ThoughtPacket(focus="Implementation stage", confidence=0.85)

changes = diff_packets(before, after)
# → {'thought_state.focus': {'before': 'Idea stage', 'after': 'Implementation stage'}, ...}
```

---

## Why This Matters

Most AI frameworks focus on **pipelines** (what the AI does).  
Axis Thought Packet focuses on **state** (where the AI is).

| Framework | Focus |
|-----------|-------|
| LangChain / LlamaIndex | Task pipelines |
| AutoGen / CrewAI | Agent orchestration |
| **Axis Thought Packet** | **Thought state representation** |

These are complementary, not competing. ATP is the **cognitive layer** that sits beneath any pipeline.

Inspired by:
- EML functions — any elementary function from a single binary operator
- Fourier analysis — any waveform from simple basis functions  
- HFE (Hypothesis Field Engine) — reasoning as geometric navigation in meaning space
- The Universal Formula — thought as state, transition, translation

---

## Repository Structure

```
axis-thought-packet/
├── src/axis_thought_packet/   # Python package
│   ├── packet.py              # ThoughtPacket core
│   ├── lens.py                # ThoughtLens transformer
│   └── utils.py               # merge, diff, load, save
├── tests/                     # 13 tests, all passing
├── examples/                  # quickstart.py
├── schema/                    # JSON Schema spec
├── docs/                      # specification notes
└── paper/                     # manuscript drafts
```

---

## Citation

If you use Axis Thought Packet in research, please cite:

```bibtex
@software{axis_thought_packet_2026,
  author    = {Da-P-AIP},
  title     = {Axis Thought Packet: A structured thought-state representation
               format for human-AI and multi-agent collaboration},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20116884},
  url       = {https://github.com/Da-P-AIP/axis-thought-packet}
}
```

Citation metadata: `CITATION.cff` · Zenodo metadata: `.zenodo.json`

---

## License

CC BY 4.0 — use freely, cite the source.
