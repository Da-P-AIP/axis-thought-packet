"""
Tests for Axis Thought Packet
"""

import json
import tempfile
import os
import pytest

from axis_thought_packet import ThoughtPacket, ThoughtLens
from axis_thought_packet.utils import merge_packets, diff_packets


class TestThoughtPacket:
    def test_basic_creation(self):
        p = ThoughtPacket(
            focus="Build an API",
            intent="Make it model-agnostic",
            confidence=0.85
        )
        assert p.thought_state.focus == "Build an API"
        assert p.thought_state.intent == "Make it model-agnostic"
        assert p.thought_state.confidence == 0.85

    def test_confidence_validation(self):
        with pytest.raises(ValueError):
            ThoughtPacket(focus="test", intent="test", confidence=1.5)
        with pytest.raises(ValueError):
            ThoughtPacket(focus="test", intent="test", confidence=-0.1)

    def test_position(self):
        p = ThoughtPacket(
            focus="Axis Thought Packet design",
            intent="Create pip-installable package",
            confidence=0.9,
            context="GitHub open source project"
        )
        pos = p.position
        assert "clarity" in pos
        assert "confidence" in pos
        assert "novelty" in pos
        assert "completeness" in pos
        assert pos["confidence"] == 0.9

    def test_to_json(self):
        p = ThoughtPacket(focus="test", intent="test intent", confidence=0.7)
        j = json.loads(p.to_json())
        assert j["thought_state"]["focus"] == "test"
        assert j["thought_state"]["confidence"] == 0.7

    def test_save_and_load(self):
        p = ThoughtPacket(
            focus="Saved packet",
            intent="Persist across sessions",
            confidence=0.75,
            subject="persistence",
            tags=["test", "persistence"]
        )
        with tempfile.NamedTemporaryFile(suffix=".atp", delete=False) as f:
            path = f.name
        try:
            p.save(path)
            loaded = ThoughtPacket.load(path)
            assert loaded.thought_state.focus == p.thought_state.focus
            assert loaded.thought_state.confidence == p.thought_state.confidence
            assert loaded.tags == p.tags
        finally:
            os.unlink(path)

    def test_to_prompt(self):
        p = ThoughtPacket(
            focus="Design the Universal Formula",
            intent="Bridge human and AI cognition",
            confidence=0.9,
            context="Axis Thought Packet project"
        )
        prompt = p.to_prompt()
        assert "Design the Universal Formula" in prompt
        assert "Bridge human and AI cognition" in prompt
        assert "Axis Thought Packet" in prompt

    def test_from_text(self):
        p = ThoughtPacket.from_text(
            "The EML function can represent all elementary functions.",
            model="claude-sonnet-4-6",
            intent="Analyze EML theory"
        )
        assert p.model == "claude-sonnet-4-6"
        assert "EML" in p.thought_state.focus

    def test_from_dict_roundtrip(self):
        original = ThoughtPacket(
            focus="Roundtrip test",
            intent="Verify serialization",
            confidence=0.6,
            subject="testing",
            context="unit test",
            to_state="verified"
        )
        restored = ThoughtPacket.from_dict(original.to_dict())
        assert restored.thought_state.focus == original.thought_state.focus
        assert restored.thought_state.confidence == original.thought_state.confidence


class TestThoughtLens:
    def test_critic_lens(self):
        p = ThoughtPacket(focus="Big idea", intent="Change the world", confidence=0.9)
        lens = ThoughtLens("critic")
        result = lens.apply(p)
        assert result.thought_state.confidence < p.thought_state.confidence
        assert "critic" in result.tags

    def test_custom_lens(self):
        def my_transform(packet):
            return {"confidence": 1.0, "stance": "fully committed"}

        p = ThoughtPacket(focus="test", intent="test", confidence=0.5)
        lens = ThoughtLens("optimist", transform_fn=my_transform)
        result = lens.apply(p)
        assert result.thought_state.confidence == 1.0
        assert result.axes.stance == "fully committed"

    def test_lens_does_not_mutate_original(self):
        p = ThoughtPacket(focus="original", intent="stay same", confidence=0.5)
        lens = ThoughtLens("critic")
        lens.apply(p)
        assert p.thought_state.confidence == 0.5


class TestUtils:
    def test_merge_packets(self):
        p1 = ThoughtPacket(focus="Step 1", intent="Start", confidence=0.6)
        p2 = ThoughtPacket(focus="Step 2", intent="Middle", confidence=0.8)
        p3 = ThoughtPacket(focus="Step 3", intent="End", confidence=0.7)
        merged = merge_packets(p1, p2, p3)
        assert merged.thought_state.focus == "Step 3"
        assert abs(merged.thought_state.confidence - 0.7) < 0.01
        assert "Start" in merged.thought_state.intent

    def test_diff_packets(self):
        p1 = ThoughtPacket(focus="Before", intent="old intent", confidence=0.5)
        p2 = ThoughtPacket(focus="After", intent="new intent", confidence=0.9)
        diff = diff_packets(p1, p2)
        assert "thought_state.focus" in diff
        assert diff["thought_state.focus"]["before"] == "Before"
        assert diff["thought_state.focus"]["after"] == "After"
