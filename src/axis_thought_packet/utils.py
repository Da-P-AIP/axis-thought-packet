"""
Utils — Helper functions for Axis Thought Packet
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Union
from .packet import ThoughtPacket


def save_packet(packet: ThoughtPacket, path: Union[str, Path]) -> None:
    """Save a ThoughtPacket to a file."""
    packet.save(str(path))


def load_packet(path: Union[str, Path]) -> ThoughtPacket:
    """Load a ThoughtPacket from a file."""
    return ThoughtPacket.load(str(path))


def merge_packets(*packets: ThoughtPacket, method: str = "merge") -> ThoughtPacket:
    """
    Merge multiple ThoughtPackets into one.
    Useful for multi-agent handoffs where several agents contributed.

    The resulting packet takes:
    - focus from the last packet
    - intent synthesized from all packets
    - confidence as weighted average
    """
    if not packets:
        raise ValueError("At least one packet is required")
    if len(packets) == 1:
        return packets[0]

    last = packets[-1]
    avg_confidence = sum(p.thought_state.confidence for p in packets) / len(packets)
    combined_intent = " → ".join(
        p.thought_state.intent for p in packets if p.thought_state.intent
    )
    all_tags = list({tag for p in packets for tag in p.tags})

    return ThoughtPacket(
        focus=last.thought_state.focus,
        intent=combined_intent,
        confidence=round(avg_confidence, 3),
        subject=last.axes.subject,
        context=last.axes.context,
        stance=f"merged from {len(packets)} packets",
        from_state=packets[0].thought_state.focus,
        to_state=last.thought_state.focus,
        method=method,
        tags=all_tags,
    )


def diff_packets(a: ThoughtPacket, b: ThoughtPacket) -> dict:
    """
    Compare two packets and return a diff of changed fields.
    Useful for tracking how thought state evolved.
    """
    da = a.to_dict()
    db = b.to_dict()
    result = {}
    for key in ("thought_state", "axes", "transition"):
        fa, fb = da.get(key, {}), db.get(key, {})
        for field in set(list(fa.keys()) + list(fb.keys())):
            va, vb = fa.get(field), fb.get(field)
            if va != vb:
                result[f"{key}.{field}"] = {"before": va, "after": vb}
    return result
