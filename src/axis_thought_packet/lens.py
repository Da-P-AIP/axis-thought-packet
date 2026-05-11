"""
ThoughtLens — Interpretive lens for Axis Thought Packets.

Maps a packet into another viewpoint, agent, or task context.
Think of it as a coordinate transformation in thought-space.
"""

from __future__ import annotations

from typing import Optional, Callable
from .packet import ThoughtPacket


class ThoughtLens:
    """
    A lens that re-interprets a ThoughtPacket through a different viewpoint.

    Example
    -------
    >>> packet = ThoughtPacket(focus="Build an API", intent="Ship fast", confidence=0.7)
    >>> lens = ThoughtLens(viewpoint="security_reviewer")
    >>> transformed = lens.apply(packet)
    >>> print(transformed.axes.stance)
    'viewed through security_reviewer lens'
    """

    def __init__(
        self,
        viewpoint: str,
        transform_fn: Optional[Callable[[ThoughtPacket], dict]] = None,
    ):
        """
        Parameters
        ----------
        viewpoint : str
            Name of the interpretive lens (e.g. "critic", "implementer", "user")
        transform_fn : callable, optional
            Custom function that takes a ThoughtPacket and returns
            a dict of field overrides. If None, applies default lens logic.
        """
        self.viewpoint = viewpoint
        self.transform_fn = transform_fn

    def apply(self, packet: ThoughtPacket) -> ThoughtPacket:
        """
        Apply the lens to a packet, returning a new transformed packet.
        The original packet is not mutated.
        """
        overrides = {}

        if self.transform_fn:
            overrides = self.transform_fn(packet)
        else:
            overrides = self._default_transform(packet)

        base = packet.to_dict()
        ts = base["thought_state"]
        ax = base["axes"]
        tr = base["transition"]

        return ThoughtPacket(
            focus=overrides.get("focus", ts["focus"]),
            intent=overrides.get("intent", ts["intent"]),
            confidence=overrides.get("confidence", ts["confidence"]),
            subject=overrides.get("subject", ax["subject"]),
            context=overrides.get("context", ax["context"]),
            stance=overrides.get("stance", f"viewed through {self.viewpoint} lens"),
            title=overrides.get("title", f"[{self.viewpoint}] {base['title']}"),
            from_state=overrides.get("from_state", tr.get("from", "")),
            to_state=overrides.get("to_state", tr.get("to", "")),
            method=overrides.get("method", tr.get("method", "")),
            tags=base["tags"] + [self.viewpoint],
            model=base.get("model"),
        )

    def _default_transform(self, packet: ThoughtPacket) -> dict:
        """
        Built-in lens behaviors for common viewpoints.
        """
        vp = self.viewpoint.lower()

        if vp in ("critic", "reviewer"):
            return {
                "intent": f"Critically evaluate: {packet.thought_state.intent}",
                "confidence": max(0.1, packet.thought_state.confidence - 0.2),
            }
        elif vp in ("implementer", "engineer"):
            return {
                "intent": f"Implement concretely: {packet.thought_state.intent}",
                "stance": "practical implementation focus",
            }
        elif vp in ("user", "customer"):
            return {
                "focus": f"From user perspective: {packet.thought_state.focus}",
                "intent": "Understand value and usability",
            }
        elif vp in ("summarizer", "summary"):
            return {
                "focus": packet.thought_state.focus[:60],
                "intent": "Distill to essential points",
                "confidence": 1.0,
            }
        else:
            return {}

    def __repr__(self) -> str:
        return f"ThoughtLens(viewpoint={self.viewpoint!r})"


# ------------------------------------------------------------------
# Preset lenses
# ------------------------------------------------------------------

CriticLens = ThoughtLens("critic")
ImplementerLens = ThoughtLens("implementer")
UserLens = ThoughtLens("user")
SummaryLens = ThoughtLens("summarizer")
