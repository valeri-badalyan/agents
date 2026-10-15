# Leo Da Vinci

Design agent for 3D artwork, illustrations, and rendering.

## Features

- **3D Scene Design** — compose scenes with lighting, materials, and camera setup
- **Illustration Planning** — define composition, style, color palette, and mood
- **Rendering Pipeline** — configure render settings, quality, and output formats
- **Style Guide Creation** — establish visual identity and artistic direction
- **Asset Specification** — define 3D models, textures, and shader requirements

## Usage

```python
from leo_davinci import LeoDaVinci

agent = LeoDaVinci()

# Design a 3D scene
agent.create_scene("Medieval Village", lighting="golden_hour", mood="serene")

# Add assets to the scene
agent.add_asset("Cottage", type="model", style="low_poly", texture="wood_stone")
agent.add_asset("Tree", type="model", style="realistic", count=12)

# Configure rendering
agent.configure_render(quality="high", resolution="4K", samples=1024)

# Generate illustration brief
print(agent.generate_brief())

# Get render settings
print(agent.get_render_config())
```

## CLI

```bash
python session_loader.py leo-davinci
```
