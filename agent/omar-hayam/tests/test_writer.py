
from omar.writer import OmarWriter


def test_create_scenario():
    writer = OmarWriter()
    scenario = writer.create_scenario(
        title="Test Story",
        genre="sci-fi",
        characters=["Hero", "Villain"],
        setting="Space station",
    )
    assert scenario.title == "Test Story"
    assert scenario.genre == "sci-fi"
    assert len(scenario.characters) == 2


def test_create_scenario_defaults():
    writer = OmarWriter()
    scenario = writer.create_scenario(title="Default Test")
    assert scenario.title == "Default Test"
    assert scenario.genre == "drama"
    assert len(scenario.characters) == 0


def test_add_character():
    writer = OmarWriter()
    scenario = writer.create_scenario(title="Test")
    char = writer.add_character(scenario, "New Character", role="protagonist")
    assert char.name == "New Character"
    assert char.role == "protagonist"
    assert len(scenario.characters) == 1


def test_add_scene():
    writer = OmarWriter()
    scenario = writer.create_scenario(title="Test")
    writer.add_scene(scenario, act=1, title="Opening", description="The beginning")
    assert len(scenario.acts[0]["scenes"]) == 1
    assert len(scenario.scenes) == 1


def test_add_dialogue():
    writer = OmarWriter()
    scenario = writer.create_scenario(title="Test")
    writer.add_dialogue(scenario, "Hero", "I will save the world!")
    assert len(scenario.dialogue_samples) == 1


def test_list_templates():
    writer = OmarWriter()
    templates = writer.list_templates()
    assert "three-act" in templates
    assert "hero-journey" in templates


def test_format_markdown():
    writer = OmarWriter()
    scenario = writer.create_scenario(title="Format Test", genre="comedy")
    output = writer.format_scenario(scenario, fmt="markdown")
    assert "# Format Test" in output
    assert "comedy" in output