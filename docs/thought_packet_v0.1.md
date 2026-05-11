# Thought Packet v0.1

An Axis Thought Packet is a lightweight record for preserving a thought state across humans, AI agents, and multi-agent workflows.

It is designed to be:

- portable
- inspectable
- extensible
- suitable for public or private contexts
- usable as a handoff object between agents

## Minimal Fields

- `packet_id` - stable identifier for the packet
- `version` - packet format version
- `title` - human-readable packet title
- `thought_state` - core focus, intent, and confidence
- `axes` - contextual coordinates of the thought
- `transition` - how the state was produced or should move forward

## Optional Fields

- `lineage` - source packet, parent state, or previous handoff
- `constraints` - public/private boundary, license, safety, or task limits
- `evidence` - references, files, links, or observations
- `next_actions` - suggested next steps

## Design Boundary

The packet should capture enough context to continue thought, without requiring raw private logs.

For public repositories, avoid including:

- raw private conversations
- account identifiers
- credentials or tokens
- unpublished personal data
- private URLs or browser captures

