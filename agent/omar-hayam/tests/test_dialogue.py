
from omar.dialogue import DialogueGenerator


def test_create_scene():
    gen = DialogueGenerator()
    scene = gen.create_scene("Test Scene")
    assert scene.title == "Test Scene"
    assert len(scene.lines) == 0


def test_add_line():
    gen = DialogueGenerator()
    scene = gen.create_scene("Test")
    scene.add_line("Hero", "Hello there!")
    assert len(scene.lines) == 1
    assert scene.lines[0].character == "Hero"


def test_add_line_with_direction():
    gen = DialogueGenerator()
    scene = gen.create_scene("Test")
    scene.add_line("Hero", "Hello!", direction="angrily")
    assert scene.lines[0].direction == "angrily"


def test_get_character_lines():
    gen = DialogueGenerator()
    scene = gen.create_scene("Test")
    scene.add_line("Hero", "Line 1")
    scene.add_line("Villain", "Line 2")
    scene.add_line("Hero", "Line 3")
    hero_lines = scene.get_character_lines("Hero")
    assert len(hero_lines) == 2


def test_to_script():
    gen = DialogueGenerator()
    scene = gen.create_scene("Test")
    scene.add_line("Hero", "Hello!")
    script = scene.to_script()
    assert "HERO: Hello!" in script


def test_generate_template():
    gen = DialogueGenerator()
    lines = gen.generate_template("argument")
    assert len(lines) > 0
    assert all(isinstance(l, str) for l in lines)


def test_list_templates():
    gen = DialogueGenerator()
    templates = gen.list_templates()
    assert "argument" in templates
    assert "negotiation" in templates