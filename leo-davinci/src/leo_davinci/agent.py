"""Core design agent — creates 3D scenes, illustrations, and render configurations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Asset:
    """A 3D asset in a scene."""

    name: str
    asset_type: str = "model"
    style: str = "realistic"
    texture: str = ""
    scale: float = 1.0
    position: tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class Light:
    """A light source in a scene."""

    name: str
    light_type: str = "point"
    intensity: float = 1.0
    color: str = "#FFFFFF"
    position: tuple[float, float, float] = (0.0, 5.0, 0.0)
    cast_shadows: bool = True


@dataclass
class Camera:
    """Camera configuration for rendering."""

    name: str = "MainCamera"
    fov: float = 50.0
    position: tuple[float, float, float] = (0.0, 2.0, -5.0)
    target: tuple[float, float, float] = (0.0, 0.0, 0.0)
    depth_of_field: bool = False
    aperture: float = 1.8


@dataclass
class Material:
    """A material definition for assets."""

    name: str
    base_color: str = "#CCCCCC"
    metallic: float = 0.0
    roughness: float = 0.5
    normal_map: str = ""
    emissive: str = ""
    opacity: float = 1.0


@dataclass
class RenderConfig:
    """Render output configuration."""

    quality: str = "medium"
    resolution: str = "1920x1080"
    samples: int = 256
    engine: str = "cycles"
    format: str = "PNG"
    denoise: bool = True
    output_path: str = "./renders/"


@dataclass
class StyleGuide:
    """Visual style guide for a project."""

    name: str
    art_style: str = "realistic"
    color_palette: list[str] = field(default_factory=list)
    mood: str = ""
    references: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)


class LeoDaVinci:
    """Design agent for 3D artwork, illustrations, and rendering."""

    def __init__(self) -> None:
        self.scenes: dict[str, dict[str, Any]] = {}
        self.assets: list[Asset] = []
        self.lights: list[Light] = []
        self.camera: Camera = Camera()
        self.materials: list[Material] = []
        self.render_config: RenderConfig = RenderConfig()
        self.style_guide: StyleGuide | None = None
        self._current_scene: str | None = None

    def create_scene(
        self,
        name: str,
        lighting: str = "neutral",
        mood: str = "",
        background: str = "#1a1a2e",
    ) -> str:
        """Create a new 3D scene with preset lighting."""
        lighting_presets: dict[str, list[Light]] = {
            "neutral": [
                Light("Key", "area", 1.0, "#FFFFFF", (3, 5, 3)),
                Light("Fill", "area", 0.4, "#B0C4DE", (-3, 3, 1)),
            ],
            "golden_hour": [
                Light("Sun", "sun", 1.2, "#FFA500", (10, 3, 5)),
                Light("Ambient", "hemisphere", 0.3, "#87CEEB", (0, 10, 0)),
            ],
            "dramatic": [
                Light("Spot", "spot", 2.0, "#FFFFFF", (0, 8, 0)),
                Light("Rim", "point", 0.8, "#4169E1", (-5, 2, 5)),
            ],
            "studio": [
                Light("Key", "area", 1.5, "#FFFFFF", (4, 4, 4)),
                Light("Fill", "area", 0.6, "#FFF8DC", (-3, 3, 2)),
                Light("Back", "area", 0.8, "#FFFFFF", (0, 3, -4)),
            ],
            "night": [
                Light("Moon", "directional", 0.3, "#C0C0FF", (5, 10, 5)),
                Light("Lamp", "point", 0.6, "#FFD700", (0, 2, 0)),
            ],
        }

        self._current_scene = name
        self.scenes[name] = {
            "mood": mood,
            "background": background,
            "lighting_preset": lighting,
        }
        self.lights = lighting_presets.get(lighting, lighting_presets["neutral"])
        self.assets = []
        self.materials = []

        return f"Scene '{name}' created with '{lighting}' lighting"

    def add_asset(
        self,
        name: str,
        asset_type: str = "model",
        style: str = "realistic",
        texture: str = "",
        scale: float = 1.0,
        position: tuple[float, float, float] | None = None,
    ) -> Asset:
        """Add a 3D asset to the current scene."""
        pos = position or (0.0, 0.0, 0.0)
        asset = Asset(
            name=name,
            asset_type=asset_type,
            style=style,
            texture=texture,
            scale=scale,
            position=pos,
        )
        self.assets.append(asset)
        return asset

    def add_light(
        self,
        name: str,
        light_type: str = "point",
        intensity: float = 1.0,
        color: str = "#FFFFFF",
        position: tuple[float, float, float] | None = None,
    ) -> Light:
        """Add a custom light to the scene."""
        pos = position or (0.0, 5.0, 0.0)
        light = Light(name=name, light_type=light_type, intensity=intensity, color=color, position=pos)
        self.lights.append(light)
        return light

    def set_camera(
        self,
        fov: float = 50.0,
        position: tuple[float, float, float] | None = None,
        target: tuple[float, float, float] | None = None,
        depth_of_field: bool = False,
    ) -> Camera:
        """Configure the scene camera."""
        self.camera = Camera(
            fov=fov,
            position=position or (0.0, 2.0, -5.0),
            target=target or (0.0, 0.0, 0.0),
            depth_of_field=depth_of_field,
        )
        return self.camera

    def add_material(
        self,
        name: str,
        base_color: str = "#CCCCCC",
        metallic: float = 0.0,
        roughness: float = 0.5,
    ) -> Material:
        """Create and attach a material."""
        mat = Material(name=name, base_color=base_color, metallic=metallic, roughness=roughness)
        self.materials.append(mat)
        return mat

    def configure_render(
        self,
        quality: str = "medium",
        resolution: str = "1920x1080",
        samples: int = 256,
        engine: str = "cycles",
        format: str = "PNG",
    ) -> RenderConfig:
        """Configure render output settings."""
        quality_presets: dict[str, int] = {
            "preview": 64,
            "low": 128,
            "medium": 256,
            "high": 1024,
            "ultra": 4096,
        }
        self.render_config = RenderConfig(
            quality=quality,
            resolution=resolution,
            samples=quality_presets.get(samples, samples) if isinstance(samples, int) else samples,
            engine=engine,
            format=format,
        )
        return self.render_config

    def create_style_guide(
        self,
        name: str,
        art_style: str = "realistic",
        color_palette: list[str] | None = None,
        mood: str = "",
    ) -> StyleGuide:
        """Define a visual style guide for the project."""
        self.style_guide = StyleGuide(
            name=name,
            art_style=art_style,
            color_palette=color_palette or [],
            mood=mood,
        )
        return self.style_guide

    def generate_brief(self) -> str:
        """Generate a design brief summarizing the current scene."""
        parts = []
        if self._current_scene:
            parts.append(f"Scene: {self._current_scene}")
        if self.assets:
            asset_names = ", ".join(a.name for a in self.assets)
            parts.append(f"Assets: {asset_names} ({len(self.assets)} total)")
        if self.lights:
            parts.append(f"Lighting: {len(self.lights)} sources")
        if self.style_guide:
            parts.append(f"Style: {self.style_guide.art_style}")
        if self.render_config:
            parts.append(f"Render: {self.render_config.quality} @ {self.render_config.resolution}")
        return " | ".join(parts) if parts else "No scene defined yet."

    def get_render_config(self) -> dict[str, Any]:
        """Return render settings as a dictionary."""
        return {
            "quality": self.render_config.quality,
            "resolution": self.render_config.resolution,
            "samples": self.render_config.samples,
            "engine": self.render_config.engine,
            "format": self.render_config.format,
            "denoise": self.render_config.denoise,
            "output_path": self.render_config.output_path,
        }

    def get_scene_stats(self) -> dict[str, Any]:
        """Return statistics about the current scene."""
        return {
            "scene": self._current_scene,
            "assets": len(self.assets),
            "lights": len(self.lights),
            "materials": len(self.materials),
            "camera_fov": self.camera.fov,
            "has_style_guide": self.style_guide is not None,
        }

    def execute(self, task: str, **kwargs: Any) -> str:
        """Main entry point — route design tasks."""
        task_lower = task.lower()
        if "scene" in task_lower and ("create" in task_lower or "new" in task_lower):
            name = kwargs.get("name", "Untitled Scene")
            return self.create_scene(
                name,
                kwargs.get("lighting", "neutral"),
                kwargs.get("mood", ""),
            )
        elif "asset" in task_lower or "add" in task_lower:
            name = kwargs.get("name", "Untitled Asset")
            asset = self.add_asset(
                name,
                kwargs.get("type", "model"),
                kwargs.get("style", "realistic"),
                kwargs.get("texture", ""),
            )
            return f"Added asset: {asset.name} ({asset.asset_type})"
        elif "render" in task_lower:
            self.configure_render(
                kwargs.get("quality", "medium"),
                kwargs.get("resolution", "1920x1080"),
                kwargs.get("samples", 256),
            )
            return f"Render configured: {self.render_config.quality} @ {self.render_config.resolution}"
        elif "brief" in task_lower:
            return self.generate_brief()
        elif "style" in task_lower:
            self.create_style_guide(
                kwargs.get("name", "Default Style"),
                kwargs.get("art_style", "realistic"),
                kwargs.get("color_palette", []),
                kwargs.get("mood", ""),
            )
            return f"Style guide created: {kwargs.get('name', 'Default Style')}"
        elif "stats" in task_lower:
            stats = self.get_scene_stats()
            return f"Scene stats: {stats['assets']} assets, {stats['lights']} lights, {stats['materials']} materials"
        else:
            return self.generate_brief()

    def __repr__(self) -> str:
        return (
            f"LeoDaVinci(scene={self._current_scene}, "
            f"assets={len(self.assets)}, lights={len(self.lights)})"
        )
