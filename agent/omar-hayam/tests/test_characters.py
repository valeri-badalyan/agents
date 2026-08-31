
from omar.characters import Character


def test_create_character():
    char = Character(name="Hero")
    assert char.name == "Hero"
    assert char.role == "supporting"


def test_create_character_full():
    char = Character(
        name="Hero",
        role="protagonist",
        backstory=" orphan",
        motivation="revenge",
        conflict="inner demons",
    )
    assert char.name == "Hero"
    assert char.role == "protagonist"
    assert char.backstory == " orphan"
    assert char.motivation == "revenge"


def test_add_trait():
    char = Character(name="Test")
    char.add_trait("brave")
    char.add_trait("loyal")
    assert "brave" in char.traits
    assert "loyal" in char.traits


def test_add_trait_no_duplicates():
    char = Character(name="Test")
    char.add_trait("brave")
    char.add_trait("brave")
    assert char.traits.count("brave") == 1


def test_add_relationship():
    char = Character(name="Hero")
    char.add_relationship("Villain", "enemy")
    assert "Villain" in char.relationships
    assert char.relationships["Villain"] == "enemy"


def test_describe():
    char = Character(name="Hero", role="protagonist", backstory=" orphan")
    desc = char.describe()
    assert "Hero" in desc
    assert "protagonist" in desc


def test_to_dict():
    char = Character(name="Hero", role="protagonist")
    d = char.to_dict()
    assert d["name"] == "Hero"
    assert d["role"] == "protagonist"