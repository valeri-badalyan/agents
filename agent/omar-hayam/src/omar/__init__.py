"""Omar Hayam — Scenario Writer Agent."""

from omar.characters import Character
from omar.dialogue import DialogueGenerator
from omar.format import ScenarioFormatter
from omar.templates import StoryTemplate
from omar.writer import OmarWriter

__version__ = "0.1.0"
__all__ = [
    "Character",
    "DialogueGenerator",
    "OmarWriter",
    "ScenarioFormatter",
    "StoryTemplate",
]