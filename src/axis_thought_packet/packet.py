"""
ThoughtPacket — Core class for Axis Thought Packet
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


@dataclass
class ThoughtState:
    """Represents the current thought state."""
    focus: str
    intent: str
    confidence: float = 0.5

    def __post_init__(self):
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")


@dataclass
class Axes:
    """Multi-dimensional context axes."""
    subject: str = ""
    context: str = ""
    stance: str = ""
    time: str = field(default_factory=lambda: datetime.now(timezone.utc).date().isoformat())


@dataclass
class Transition:
    """State transition description."""
    from_state: str = ""
    to_state: str = ""
    method: str = ""


class ThoughtPacket:
    """
    A portable representation of a thought state and its context.

    Designed to be model-agnostic — works with Claude, GPT, Gemini,
    or any LLM. Enables thought-state continuity across sessions
    and multi-agent handoffs.

    Example
    -------
    >>> packet = ThoughtPacket(
    ...     focus="Designing a new API",
    ...     intent="Make it model-agnostic",
    ...     confidence=0.85
    ... )
    >>> print(packet.position)
    {'clarity': 0.85, 'confidence': 0.85, 'novelty': 0.5}
    >>> prompt = packet.to_prompt()
    >>> print(prompt)  # paste into any AI session
    """

    def __init__(
        self,
        focus: str,
        intent: str,
        confidence: float = 0.5,
        subject: str = "",
        context: str = "",
        stance: str = "",
        title: str = "",
        packet_id: Optional[str] = None,
        version: str = "0.1.0",
        from_state: str = "",
        to_state: str = "",
        method: str = "",
        tags: Optional[list] = None,
        model: Optional[str] = None,
    ):
        self.packet_id = packet_id or f"packet.{uuid.uuid4().hex[:8]}"
        self.version = version
        self.title = title or focus[:60]
        self.model = model

        self.thought_state = ThoughtState(
            focus=focus,
            intent=intent,
            confidence=confidence,
        )
        self.axes = Axes(
            subject=subject,
            context=context,
            stance=stance,
        )
        self.transition = Transition(
            from_state=from_state,
            to_state=to_state,
            method=method,
        )
        self.tags = tags or []
        self._created_at = datetime.now(timezone.utc).isoformat()

    # ------------------------------------------------------------------
    # Core: position in thought-space
    # ------------------------------------------------------------------

    @property
    def position(self) -> dict:
        """
        Returns coordinates in thought-space.
        Useful for AI self-awareness: 'where am I right now?'

        Returns
        -------
        dict with keys: clarity, confidence, novelty, completeness
        """
        clarity = min(1.0, (
            (0.4 if self.thought_state.focus else 0.0) +
            (0.3 if self.thought_state.intent else 0.0) +
            (0.3 if self.axes.context else 0.0)
        ))
        completeness = min(1.0, (
            (0.25 if self.thought_state.focus else 0.0) +
            (0.25 if self.thought_state.intent else 0.0) +
            (0.25 if self.axes.subject else 0.0) +
            (0.25 if self.transition.to_state else 0.0)
        ))
        novelty = 0.5  # default; override via ThoughtLens
        return {
            "clarity": round(clarity, 3),
            "confidence": round(self.thought_state.confidence, 3),
            "novelty": round(novelty, 3),
            "completeness": round(completeness, 3),
        }

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Convert to plain dictionary (JSON-serializable)."""
        return {
            "packet_id": self.packet_id,
            "version": self.version,
            "title": self.title,
            "model": self.model,
            "created_at": self._created_at,
            "tags": self.tags,
            "thought_state": asdict(self.thought_state),
            "axes": asdict(self.axes),
            "transition": {
                "from": self.transition.from_state,
                "to": self.transition.to_state,
                "method": self.transition.method,
            },
            "position": self.position,
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def to_prompt(self) -> str:
        """
        Generate a resumption prompt for any AI model.
        Paste this at the start of a new session to inherit the thought state.
        """
        lines = [
            "## Axis Thought Packet — Context Handoff",
            f"**Focus**: {self.thought_state.focus}",
            f"**Intent**: {self.thought_state.intent}",
            f"**Confidence**: {self.thought_state.confidence}",
        ]
        if self.axes.subject:
            lines.append(f"**Subject**: {self.axes.subject}")
        if self.axes.context:
            lines.append(f"**Context**: {self.axes.context}")
        if self.axes.stance:
            lines.append(f"**Stance**: {self.axes.stance}")
        if self.transition.to_state:
            lines.append(f"**Next step**: {self.transition.to_state}")
        lines.append(
            "\nPlease continue from this thought state without requiring re-explanation."
        )
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: str) -> None:
        """Save packet to a .atp (JSON) file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json())

    @classmethod
    def load(cls, path: str) -> "ThoughtPacket":
        """Load packet from a .atp (JSON) file."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> "ThoughtPacket":
        """Reconstruct a ThoughtPacket from a dictionary."""
        ts = data.get("thought_state", {})
        ax = data.get("axes", {})
        tr = data.get("transition", {})
        return cls(
            focus=ts.get("focus", ""),
            intent=ts.get("intent", ""),
            confidence=ts.get("confidence", 0.5),
            subject=ax.get("subject", ""),
            context=ax.get("context", ""),
            stance=ax.get("stance", ""),
            title=data.get("title", ""),
            packet_id=data.get("packet_id"),
            version=data.get("version", "0.1.0"),
            from_state=tr.get("from", ""),
            to_state=tr.get("to", ""),
            method=tr.get("method", ""),
            tags=data.get("tags", []),
            model=data.get("model"),
        )

    @classmethod
    def from_text(cls, ai_response: str, model: Optional[str] = None, **kwargs) -> "ThoughtPacket":
        """
        Create a packet from raw AI response text.
        Useful for wrapping any LLM output into a thought packet.
        """
        focus = ai_response[:120].replace("\n", " ").strip()
        return cls(
            focus=focus,
            intent=kwargs.get("intent", "Captured from AI response"),
            confidence=kwargs.get("confidence", 0.6),
            model=model,
            context=kwargs.get("context", ""),
            subject=kwargs.get("subject", ""),
            **{k: v for k, v in kwargs.items()
               if k not in ("intent", "confidence", "context", "subject")},
        )

    # ------------------------------------------------------------------
    # Dunder
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"ThoughtPacket(id={self.packet_id!r}, "
            f"focus={self.thought_state.focus[:40]!r}, "
            f"confidence={self.thought_state.confidence})"
        )
