"""Tests for the statue spawn system."""

from __future__ import annotations

import pytest

from src.statues import (
    SpawnBonus,
    SpawnBonusType,
    SpawnEffect,
    Statue,
    StatueCategory,
    StatueRegistry,
)


def test_statue_creation() -> None:
    """Test creating a statue."""
    effect = SpawnEffect(
        visual="Golden light",
        sound="Chant",
        message="Test message",
    )
    bonus = SpawnBonus(SpawnBonusType.ATTACK, 0.10, 60)

    statue = Statue(
        id="test_statue",
        name="Test Statue",
        location="test_location",
        category=StatueCategory.HISTORICAL,
        description="A test statue",
        height=2.0,
        material="Stone",
        pose="Standing",
        activation_method="Touch",
        effect=effect,
        bonus=bonus,
        lore="Test lore",
    )

    assert statue.id == "test_statue"
    assert statue.name == "Test Statue"
    assert not statue.is_discovered
    assert not statue.is_activated


def test_statue_discovery() -> None:
    """Test discovering a statue."""
    effect = SpawnEffect(
        visual="Golden light",
        sound="Chant",
        message="Test message",
    )
    bonus = SpawnBonus(SpawnBonusType.ATTACK, 0.10, 60)

    statue = Statue(
        id="test_statue",
        name="Test Statue",
        location="test_location",
        category=StatueCategory.HISTORICAL,
        description="A test statue",
        height=2.0,
        material="Stone",
        pose="Standing",
        activation_method="Touch",
        effect=effect,
        bonus=bonus,
        lore="Test lore",
    )

    result = statue.discover()
    assert statue.is_discovered
    assert "Discovered" in result

    result2 = statue.discover()
    assert "already discovered" in result2


def test_statue_activation() -> None:
    """Test activating a statue."""
    effect = SpawnEffect(
        visual="Golden light",
        sound="Chant",
        message="Test message",
    )
    bonus = SpawnBonus(SpawnBonusType.ATTACK, 0.10, 60)

    statue = Statue(
        id="test_statue",
        name="Test Statue",
        location="test_location",
        category=StatueCategory.HISTORICAL,
        description="A test statue",
        height=2.0,
        material="Stone",
        pose="Standing",
        activation_method="Touch",
        effect=effect,
        bonus=bonus,
        lore="Test lore",
    )

    result = statue.activate()
    assert statue.is_activated
    assert result.visual == "Golden light"


def test_statue_respawn() -> None:
    """Test respawning at a statue."""
    effect = SpawnEffect(
        visual="Golden light",
        sound="Chant",
        message="Test message",
    )
    bonus = SpawnBonus(SpawnBonusType.ATTACK, 0.10, 60)

    statue = Statue(
        id="test_statue",
        name="Test Statue",
        location="test_location",
        category=StatueCategory.HISTORICAL,
        description="A test statue",
        height=2.0,
        material="Stone",
        pose="Standing",
        activation_method="Touch",
        effect=effect,
        bonus=bonus,
        lore="Test lore",
    )

    player = {"health": 50, "attack": 10}
    updated_player, message = statue.respawn(player)

    assert updated_player["attack_bonus"] == 0.10
    assert "Respawned" in message


def test_spawn_bonus_application() -> None:
    """Test applying different bonus types."""
    bonus_attack = SpawnBonus(SpawnBonusType.ATTACK, 0.25, 60)
    bonus_defense = SpawnBonus(SpawnBonusType.DEFENSE, 0.15, 60)
    bonus_full = SpawnBonus(SpawnBonusType.FULL_RESTORE, 1.0, 0)

    player = {"health": 50, "max_health": 100, "mana": 30, "max_mana": 100}

    updated = bonus_attack.apply(player)
    assert updated["attack_bonus"] == 0.25

    updated = bonus_defense.apply(player)
    assert updated["defense_bonus"] == 0.15

    updated = bonus_full.apply(player)
    assert updated["health"] == 100
    assert updated["mana"] == 100


def test_statue_registry() -> None:
    """Test the statue registry."""
    registry = StatueRegistry()

    assert len(registry._statues) == 15

    statue = registry.get_statue("statue_tigranes")
    assert statue is not None
    assert statue.name == "Tigranes the Great"


def test_statue_registry_by_location() -> None:
    """Test getting statues by location."""
    registry = StatueRegistry()

    statues = registry.get_statues_by_location("armens_hideout")
    assert len(statues) == 1
    assert statues[0].id == "statue_tigranes"


def test_statue_registry_by_category() -> None:
    """Test getting statues by category."""
    registry = StatueRegistry()

    historical = registry.get_statues_by_category(StatueCategory.HISTORICAL)
    assert len(historical) == 4

    deities = registry.get_statues_by_category(StatueCategory.DEITY)
    assert len(deities) == 3


def test_statue_registry_discover() -> None:
    """Test discovering a statue via registry."""
    registry = StatueRegistry()

    result = registry.discover_statue("statue_tigranes")
    assert "Discovered" in result

    discovered = registry.get_discovered_statues()
    assert len(discovered) == 1


def test_statue_registry_activate() -> None:
    """Test activating a statue via registry."""
    registry = StatueRegistry()

    effect = registry.activate_statue("statue_tigranes")
    assert effect is not None
    assert effect.visual == "Golden light emanates from the statue"

    activated = registry.get_activated_statues()
    assert len(activated) == 1


def test_statue_registry_respawn() -> None:
    """Test respawning via registry."""
    registry = StatueRegistry()
    registry.activate_statue("statue_tigranes")

    player = {"health": 50, "attack": 10}
    updated, message = registry.respawn_at("statue_tigranes", player)

    assert updated["attack_bonus"] == 0.10
    assert "Respawned" in message


def test_statue_registry_not_found() -> None:
    """Test handling of non-existent statue."""
    registry = StatueRegistry()

    result = registry.discover_statue("nonexistent")
    assert "not found" in result

    effect = registry.activate_statue("nonexistent")
    assert effect is None
