# Axis Thought Packet

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20116884.svg)](https://doi.org/10.5281/zenodo.20116884)

**Axis Thought Packet** is a structured thought-state representation format for human-AI and multi-agent collaboration.

It is based on the **Universal Formula** framework, which treats thinking as:

1. a thought state,
2. a state transition,
3. and a state translation between humans, AI agents, and multi-agent systems.

The goal of this project is to provide a lightweight, extensible format for representing, sharing, inheriting, and inspecting thought states across collaborative intelligence systems.

## Status

This repository is an early public specification package prepared for GitHub release and Zenodo archiving.

Current version target: `v0.1.0`

## Core Ideas

- **Universal Formula** - a minimal framework for describing thought as state, transition, and translation.
- **Axis Thought Packet** - a portable representation of a thought state and its context.
- **Thought Lens** - an interpretive lens that maps a packet into another viewpoint, agent, or task.
- **Three Theorems** - early working principles for continuity, translation, and inheritance of thought states.

## Repository Contents

- `docs/` - public specification notes and Zenodo submission checklist
- `schema/` - JSON Schema for Axis Thought Packet records
- `examples/` - example packets and use cases
- `paper/` - manuscript drafts and publication materials
- `src/` - implementation files, if code is added later

## Quick Example

```json
{
  "packet_id": "example.ai-agent-handoff.v0.1",
  "version": "0.1.0",
  "title": "AI Agent Handoff",
  "thought_state": {
    "focus": "Continue a repository preparation task for Zenodo release.",
    "intent": "Preserve continuity across agents without exposing private notes.",
    "confidence": 0.78
  },
  "axes": {
    "subject": "Axis Thought Packet",
    "context": "GitHub and Zenodo publication workflow",
    "stance": "public specification draft",
    "time": "2026-05-11"
  },
  "transition": {
    "from": "initial repository scaffold",
    "to": "v0.1 public specification package",
    "method": "schema, examples, docs, and metadata refinement"
  }
}
```

## Publication Plan

The recommended path is:

1. Prepare the public manuscript and supporting files in this repository.
2. Confirm that no private notes, personal data, API keys, or unpublished sensitive materials are included.
3. Push the repository to GitHub.
4. Create a GitHub release such as `v0.1.0`.
5. Archive the release on Zenodo to mint a DOI.

## Citation

Citation metadata is provided in `CITATION.cff`. Zenodo metadata is provided in `.zenodo.json`.

When both files are present, Zenodo's GitHub integration uses `.zenodo.json` for the archived record metadata, while GitHub uses `CITATION.cff` for repository citation display.

## License

This repository is licensed under Creative Commons Attribution 4.0 International (`CC-BY-4.0`) unless otherwise noted.
