# Omar Hayam

Narrative agent for creating storylines, characters, and world-building.

## Features

- **Character Creation** — design protagonists, antagonists, and supporting cast
- **World-Building** — define locations, cultures, and settings
- **Story Outlining** — structure three-act narratives with themes and tone
- **Dialogue Writing** — generate sample conversations between characters
- **Pitch Generation** — create one-paragraph story summaries

## Usage

```python
from omar_hayam import OmarHayam

agent = OmarHayam()

# Create characters
agent.create_character("Aria", role="protagonist", traits=["brave", "curious"])
agent.create_character("Malakar", role="antagonist", traits=["cunning", "patient"])

# Build world
agent.add_world_element("The Obsidian Spire", kind="location", description="A tower of black glass")

# Outline story
agent.outline_story("Aria must stop Malakar from awakening the Old Ones", theme="sacrifice vs power")

# Generate dialogue
print(agent.write_dialogue("Aria", "Malakar", "the nature of power"))

# Get pitch
print(agent.generate_pitch())
```

## CLI

```bash
python session_loader.py omar-hayam
```
