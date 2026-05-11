"""
Axis Thought Packet
===================
A structured thought-state representation format for human-AI
and multi-agent collaboration.

Based on the Universal Formula framework:
  Thought = State × Transition × Translation
"""

from .packet import ThoughtPacket
from .lens import ThoughtLens
from .utils import load_packet, save_packet

__version__ = "0.1.1"
__author__ = "Da-P-AIP"
__all__ = ["ThoughtPacket", "ThoughtLens", "load_packet", "save_packet"]
