"""RailBlock — coordinated maintenance block planning for Indian Railways."""

from .model import (
    DAY, Block, Request, Scenario, Section, Solution, Window,
    solve, verify,
)
from . import scenarios

__all__ = [
    "DAY", "Block", "Request", "Scenario", "Section", "Solution", "Window",
    "solve", "verify", "scenarios",
]
