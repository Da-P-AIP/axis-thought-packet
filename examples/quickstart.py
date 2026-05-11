"""
Axis Thought Packet — Quick Start Examples

Works with Claude, GPT, Gemini, or any LLM.
"""

from axis_thought_packet import ThoughtPacket, ThoughtLens
from axis_thought_packet.utils import merge_packets, diff_packets


# ------------------------------------------------------------------
# 1. Basic usage
# ------------------------------------------------------------------
print("=" * 60)
print("1. Basic ThoughtPacket")
print("=" * 60)

packet = ThoughtPacket(
    focus="Design axis-thought-packet as a pip package",
    intent="Make it model-agnostic and easy to adopt",
    confidence=0.85,
    subject="Axis Thought Packet",
    context="GitHub open source project, Zenodo archived",
    stance="early public specification",
    to_state="pip-installable v0.1.0 release",
)

print(packet)
print()
print("Position in thought-space:")
for k, v in packet.position.items():
    print(f"  {k}: {v}")


# ------------------------------------------------------------------
# 2. Generate a resumption prompt (paste into any AI)
# ------------------------------------------------------------------
print()
print("=" * 60)
print("2. Resumption Prompt (paste into Claude / GPT / Gemini)")
print("=" * 60)
print(packet.to_prompt())


# ------------------------------------------------------------------
# 3. Save and reload across sessions
# ------------------------------------------------------------------
print()
print("=" * 60)
print("3. Session Persistence")
print("=" * 60)

packet.save("/tmp/my_session.atp")
reloaded = ThoughtPacket.load("/tmp/my_session.atp")
print(f"Saved and reloaded: {reloaded.thought_state.focus[:50]}...")


# ------------------------------------------------------------------
# 4. ThoughtLens — view through different perspectives
# ------------------------------------------------------------------
print()
print("=" * 60)
print("4. ThoughtLens — Multiple Viewpoints")
print("=" * 60)

critic = ThoughtLens("critic")
engineer = ThoughtLens("implementer")

critical_view = critic.apply(packet)
engineer_view = engineer.apply(packet)

print(f"Original confidence:  {packet.thought_state.confidence}")
print(f"Critic confidence:    {critical_view.thought_state.confidence}")
print(f"Engineer stance:      {engineer_view.axes.stance}")


# ------------------------------------------------------------------
# 5. Multi-agent handoff
# ------------------------------------------------------------------
print()
print("=" * 60)
print("5. Multi-Agent Handoff (merge)")
print("=" * 60)

agent_1 = ThoughtPacket(
    focus="Defined the schema and JSON structure",
    intent="Establish core data format",
    confidence=0.9,
    tags=["agent:schema-designer"]
)
agent_2 = ThoughtPacket(
    focus="Implemented Python package with pip support",
    intent="Make it installable and testable",
    confidence=0.85,
    tags=["agent:engineer"]
)
agent_3 = ThoughtPacket(
    focus="Wrote tests and examples",
    intent="Ensure reliability and discoverability",
    confidence=0.8,
    tags=["agent:qa"]
)

final = merge_packets(agent_1, agent_2, agent_3)
print(f"Merged focus: {final.thought_state.focus}")
print(f"Merged confidence: {final.thought_state.confidence}")
print(f"Tags: {final.tags}")


# ------------------------------------------------------------------
# 6. Track evolution with diff
# ------------------------------------------------------------------
print()
print("=" * 60)
print("6. Thought Evolution Diff")
print("=" * 60)

before = ThoughtPacket(focus="Idea stage", intent="Explore concept", confidence=0.4)
after  = ThoughtPacket(focus="Implementation stage", intent="Ship v0.1.0", confidence=0.85)

changes = diff_packets(before, after)
for field, change in changes.items():
    print(f"  {field}: {change['before']!r} → {change['after']!r}")

print()
print("Done! ✓")
