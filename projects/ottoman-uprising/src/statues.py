"""Statue Spawn System - Spawn points in cities and key locations."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class StatueCategory(Enum):
    """Categories of statues."""

    HISTORICAL = "historical"
    DEITY = "deity"
    ANCESTOR = "ancestor"
    UNKNOWN = "unknown"


class SpawnBonusType(Enum):
    """Types of spawn bonuses."""

    ATTACK = "attack"
    DEFENSE = "defense"
    HEALTH_REGEN = "health_regen"
    CRITICAL_HIT = "critical_hit"
    STEALTH = "stealth"
    MOVEMENT_SPEED = "movement_speed"
    GOLD = "gold"
    ALL_STATS = "all_stats"
    ESCAPE_CHANCE = "escape_chance"
    SUMMON_ALLIES = "summon_allies"
    INVISIBILITY = "invisibility"
    REVEAL_HIDDEN = "reveal_hidden"
    FULL_RESTORE = "full_restore"


@dataclass
class SpawnBonus:
    """Bonus granted upon respawn at a statue."""

    bonus_type: SpawnBonusType
    value: float
    duration: float

    def apply(self, player: dict[str, Any]) -> dict[str, Any]:
        """Apply the bonus to a player."""
        updated = player.copy()
        if self.bonus_type == SpawnBonusType.ATTACK:
            updated["attack_bonus"] = updated.get("attack_bonus", 0) + self.value
        elif self.bonus_type == SpawnBonusType.DEFENSE:
            updated["defense_bonus"] = updated.get("defense_bonus", 0) + self.value
        elif self.bonus_type == SpawnBonusType.HEALTH_REGEN:
            updated["health_regen_bonus"] = updated.get("health_regen_bonus", 0) + self.value
        elif self.bonus_type == SpawnBonusType.CRITICAL_HIT:
            updated["crit_chance_bonus"] = updated.get("crit_chance_bonus", 0) + self.value
        elif self.bonus_type == SpawnBonusType.STEALTH:
            updated["stealth_bonus"] = updated.get("stealth_bonus", 0) + self.value
        elif self.bonus_type == SpawnBonusType.MOVEMENT_SPEED:
            updated["speed_bonus"] = updated.get("speed_bonus", 0) + self.value
        elif self.bonus_type == SpawnBonusType.FULL_RESTORE:
            updated["health"] = updated.get("max_health", 100)
            updated["mana"] = updated.get("max_mana", 100)
        return updated


@dataclass
class SpawnEffect:
    """Visual and audio effect for statue activation."""

    visual: str
    sound: str
    message: str


@dataclass
class Statue:
    """A statue spawn point in the game world."""

    id: str
    name: str
    location: str
    category: StatueCategory
    description: str
    height: float
    material: str
    pose: str
    activation_method: str
    effect: SpawnEffect
    bonus: SpawnBonus
    lore: str
    is_discovered: bool = False
    is_activated: bool = False

    def discover(self) -> str:
        """Discover the statue."""
        if not self.is_discovered:
            self.is_discovered = True
            return f"Discovered statue: {self.name}"
        return f"Statue already discovered: {self.name}"

    def activate(self) -> SpawnEffect:
        """Activate the statue as a spawn point."""
        if not self.is_activated:
            self.is_activated = True
        return self.effect

    def respawn(self, player: dict[str, Any]) -> tuple[dict[str, Any], str]:
        """Respawn player at this statue with bonus."""
        updated_player = self.bonus.apply(player)
        message = f"Respawned at {self.name}. Bonus: {self.bonus.bonus_type.value}"
        return updated_player, message


class StatueRegistry:
    """Registry of all statues in the game."""

    def __init__(self) -> None:
        self._statues: dict[str, Statue] = {}
        self._register_default_statues()

    def _register_default_statues(self) -> None:
        """Register all default statues."""
        statues = [
            # Armenian Highlands
            Statue(
                id="statue_tigranes",
                name="Tigranes the Great",
                location="armens_hideout",
                category=StatueCategory.HISTORICAL,
                description="A majestic bronze statue of Tigranes the Great, the greatest Armenian king.",
                height=3.0,
                material="Bronze",
                pose="Standing, sword raised",
                activation_method="Touch the statue's base",
                effect=SpawnEffect(
                    visual="Golden light emanates from the statue",
                    sound="Ancient Armenian chant",
                    message="The spirit of Tigranes guides you",
                ),
                bonus=SpawnBonus(SpawnBonusType.ATTACK, 0.10, 60),
                lore="Tigranes the Great ruled the Armenian Empire at its zenith.",
            ),
            Statue(
                id="statue_gregory",
                name="Saint Gregory the Illuminator",
                location="haghpat_monastery",
                category=StatueCategory.HISTORICAL,
                description="A stone statue of Saint Gregory, the founder of Armenian Christianity.",
                height=2.5,
                material="White marble",
                pose="Standing, cross raised",
                activation_method="Pray at the statue",
                effect=SpawnEffect(
                    visual="Soft white glow surrounds the statue",
                    sound="Church bells",
                    message="Saint Gregory watches over you",
                ),
                bonus=SpawnBonus(SpawnBonusType.HEALTH_REGEN, 0.15, 60),
                lore="Saint Gregory converted Armenia to Christianity in 301 AD.",
            ),
            Statue(
                id="statue_ara",
                name="Ara the Beautiful",
                location="tumanyan_village",
                category=StatueCategory.DEITY,
                description="A wooden statue of Ara the Beautiful, an ancient Armenian god of war.",
                height=2.0,
                material="Carved wood",
                pose="Standing, holding spear",
                activation_method="Leave an offering",
                effect=SpawnEffect(
                    visual="Red glow emanates from the statue",
                    sound="War drums",
                    message="Ara blesses your courage",
                ),
                bonus=SpawnBonus(SpawnBonusType.ATTACK, 0.20, 30),
                lore="Ara the Beautiful was worshipped as a god of war and beauty.",
            ),
            Statue(
                id="statue_anahit",
                name="Anahit, Goddess of War",
                location="battle_pass",
                category=StatueCategory.DEITY,
                description="A stone statue of Anahit, the Armenian goddess of war.",
                height=2.5,
                material="Gray stone",
                pose="Standing, holding bow",
                activation_method="Perform a combat pose",
                effect=SpawnEffect(
                    visual="Silver light surrounds the statue",
                    sound="Eagle screech",
                    message="Anahit sharpens your senses",
                ),
                bonus=SpawnBonus(SpawnBonusType.CRITICAL_HIT, 0.25, 45),
                lore="Anahit was the goddess of war and wisdom in Armenian mythology.",
            ),
            Statue(
                id="statue_fallen",
                name="The Fallen Warrior",
                location="resistance_camp",
                category=StatueCategory.ANCESTOR,
                description="A simple stone statue of an anonymous Armenian warrior.",
                height=1.8,
                material="Rough-hewn stone",
                pose="Kneeling, sword planted",
                activation_method="Salute the statue",
                effect=SpawnEffect(
                    visual="Soft golden glow",
                    sound="Wind through trees",
                    message="Remember the fallen",
                ),
                bonus=SpawnBonus(SpawnBonusType.DEFENSE, 0.10, 60),
                lore="In memory of all who fell fighting for freedom.",
            ),
            # Turkish Borderlands
            Statue(
                id="statue_unknown",
                name="The Unknown Armenian",
                location="voskan_village",
                category=StatueCategory.UNKNOWN,
                description="A mysterious stone statue, face worn away by time.",
                height=2.0,
                material="Weathered stone",
                pose="Standing, arms outstretched",
                activation_method="Touch the statue's hand",
                effect=SpawnEffect(
                    visual="Blue light emanates from the statue",
                    sound="Whispering voices",
                    message="The unknown guides you",
                ),
                bonus=SpawnBonus(SpawnBonusType.STEALTH, 0.15, 60),
                lore="Who was this figure? Their identity is lost to time.",
            ),
            Statue(
                id="statue_mithra",
                name="Mithra, God of Covenants",
                location="geghard_caves",
                category=StatueCategory.DEITY,
                description="A carved stone statue of Mithra, the ancient god of covenants.",
                height=2.0,
                material="Red stone",
                pose="Seated, holding torch",
                activation_method="Light a torch at the statue",
                effect=SpawnEffect(
                    visual="Fire emanates from the statue",
                    sound="Crackling flames",
                    message="Mithra illuminates your path",
                ),
                bonus=SpawnBonus(SpawnBonusType.REVEAL_HIDDEN, 1.0, 120),
                lore="Mithra was worshipped as the god of covenants and light.",
            ),
            Statue(
                id="statue_merchant",
                name="The Merchant's Guardian",
                location="maku_market",
                category=StatueCategory.ANCESTOR,
                description="A bronze statue of a merchant holding scales.",
                height=1.5,
                material="Bronze",
                pose="Standing, scales in hand",
                activation_method="Place a coin at the feet",
                effect=SpawnEffect(
                    visual="Green light surrounds the statue",
                    sound="Clinking coins",
                    message="The merchant smiles upon you",
                ),
                bonus=SpawnBonus(SpawnBonusType.GOLD, 0.20, 300),
                lore="Guardian of trade and commerce.",
            ),
            Statue(
                id="statue_border",
                name="The Border Guardian",
                location="araxes_crossing",
                category=StatueCategory.ANCESTOR,
                description="A stone statue watching over the border crossing.",
                height=2.5,
                material="Gray stone",
                pose="Standing, shield raised",
                activation_method="Cross the river facing the statue",
                effect=SpawnEffect(
                    visual="Water glows around the statue",
                    sound="Rushing water",
                    message="The guardian protects your crossing",
                ),
                bonus=SpawnBonus(SpawnBonusType.MOVEMENT_SPEED, 0.30, 30),
                lore="Protectors of the ancient borders.",
            ),
            # Turkish Heartland
            Statue(
                id="statue_artashes",
                name="King Artashes",
                location="city_of_ani",
                category=StatueCategory.HISTORICAL,
                description="A grand marble statue of King Artashes.",
                height=4.0,
                material="White marble",
                pose="Standing, crown on head",
                activation_method="Kneel before the statue",
                effect=SpawnEffect(
                    visual="Golden crown of light appears",
                    sound="Royal fanfare",
                    message="King Artashes recognizes his heir",
                ),
                bonus=SpawnBonus(SpawnBonusType.ALL_STATS, 0.20, 60),
                lore="Artashes founded the Artaxiad dynasty.",
            ),
            Statue(
                id="statue_prisoner",
                name="The Prisoner's Hope",
                location="kars_fortress",
                category=StatueCategory.ANCESTOR,
                description="A chained statue with broken chains.",
                height=1.8,
                material="Iron and stone",
                pose="Kneeling, chains broken",
                activation_method="Break a chain near the statue",
                effect=SpawnEffect(
                    visual="Chains shatter with golden light",
                    sound="Breaking metal",
                    message="Freedom awaits",
                ),
                bonus=SpawnBonus(SpawnBonusType.ESCAPE_CHANCE, 0.25, 300),
                lore="Hope never dies.",
            ),
            Statue(
                id="statue_ancient",
                name="The Ancient King",
                location="valley_of_statues",
                category=StatueCategory.HISTORICAL,
                description="An ancient statue of a forgotten Armenian king.",
                height=3.0,
                material="Cracked marble",
                pose="Standing, head missing",
                activation_method="Place flowers at the feet",
                effect=SpawnEffect(
                    visual="Petals swirl around the statue",
                    sound="Gentle wind",
                    message="Even broken, kings endure",
                ),
                bonus=SpawnBonus(SpawnBonusType.HEALTH_REGEN, 0.15, 120),
                lore="Some kings are forgotten but never truly lost.",
            ),
            Statue(
                id="statue_soldier",
                name="The Soldier's Memorial",
                location="yerevan_camp",
                category=StatueCategory.ANCESTOR,
                description="A row of small statues honoring fallen soldiers.",
                height=1.0,
                material="Simple stone",
                pose="Various combat poses",
                activation_method="Salute all statues",
                effect=SpawnEffect(
                    visual="Soft glow surrounds all statues",
                    sound="Distant war drums",
                    message="The fallen remember",
                ),
                bonus=SpawnBonus(SpawnBonusType.SUMMON_ALLIES, 3.0, 60),
                lore="12 statues, 12 heroes.",
            ),
            Statue(
                id="statue_underground",
                name="The Underground's Secret",
                location="armenian_underground",
                category=StatueCategory.UNKNOWN,
                description="A hidden statue glowing with strange light.",
                height=2.0,
                material="Unknown",
                pose="Standing, finger to lips",
                activation_method="Whisper a secret",
                effect=SpawnEffect(
                    visual="Shadows dance around the statue",
                    sound="Whispering",
                    message="Secrets protect you",
                ),
                bonus=SpawnBonus(SpawnBonusType.INVISIBILITY, 1.0, 15),
                lore="The underground holds many secrets.",
            ),
            # Final Boss
            Statue(
                id="statue_chenani",
                name="The Emperor's Shadow",
                location="throne_room",
                category=StatueCategory.UNKNOWN,
                description="A dark statue of Malikhor Chenani.",
                height=5.0,
                material="Black obsidian",
                pose="Seated on throne",
                activation_method="Defeat Chenani",
                effect=SpawnEffect(
                    visual="Statue crumbles, light emerges",
                    sound="Empire falling",
                    message="Tyranny ends",
                ),
                bonus=SpawnBonus(SpawnBonusType.FULL_RESTORE, 1.0, 0),
                lore="Even empires fall.",
            ),
        ]

        for statue in statues:
            self._statues[statue.id] = statue

    def get_statue(self, statue_id: str) -> Statue | None:
        """Get a statue by ID."""
        return self._statues.get(statue_id)

    def get_statues_by_location(self, location: str) -> list[Statue]:
        """Get all statues at a location."""
        return [s for s in self._statues.values() if s.location == location]

    def get_statues_by_category(self, category: StatueCategory) -> list[Statue]:
        """Get all statues of a category."""
        return [s for s in self._statues.values() if s.category == category]

    def get_discovered_statues(self) -> list[Statue]:
        """Get all discovered statues."""
        return [s for s in self._statues.values() if s.is_discovered]

    def get_activated_statues(self) -> list[Statue]:
        """Get all activated statues."""
        return [s for s in self._statues.values() if s.is_activated]

    def discover_statue(self, statue_id: str) -> str:
        """Discover a statue."""
        statue = self.get_statue(statue_id)
        if statue:
            return statue.discover()
        return f"Statue not found: {statue_id}"

    def activate_statue(self, statue_id: str) -> SpawnEffect | None:
        """Activate a statue."""
        statue = self.get_statue(statue_id)
        if statue:
            return statue.activate()
        return None

    def respawn_at(self, statue_id: str, player: dict[str, Any]) -> tuple[dict[str, Any], str]:
        """Respawn player at a statue."""
        statue = self.get_statue(statue_id)
        if statue and statue.is_activated:
            return statue.respawn(player)
        return player, f"Cannot respawn at {statue_id}: not activated"


# Global statue registry
registry = StatueRegistry()
