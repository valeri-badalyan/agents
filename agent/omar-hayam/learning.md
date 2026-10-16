# Learning — Omar Hayam

## Index

| Section | Description |
|---------|-------------|
| [Distillation Process](#distillation-process) | How Omar learns |
| [What Omar Learns](#what-omar-learns) | Types of learnings |
| [Learning Methods](#learning-methods) | How learnings are captured |
| [Storage](#storage) | Data structure |
| [Triggers](#triggers) | When learnings are applied |
| [Actual Learnings](#actual-learnings-distilled) | Distilled learnings log |

---

## Distillation Process

Omar learns through distillation — extracting creative patterns, user preferences, and storytelling techniques to improve scenario writing.

## What Omar Learns

### 1. Style Preferences
- Genre preferences (sci-fi, drama, comedy, etc.)
- Tone preferences (dark, hopeful, satirical)
- Pacing preferences (fast, slow, episodic)

### 2. Character Patterns
- Which character archetypes resonate
- What makes characters memorable
- How users prefer character development

### 3. Story Structure
- Which structures work best for genres
- How users prefer act breaks
- Pacing patterns that engage

### 4. Dialogue Style
- Natural speech patterns per character type
- Subtext techniques that work
- Dialogue pacing preferences

## Learning Methods

### Feedback Loop
- User approves/rejects scenarios → Store preferences
- User requests revisions → Learn what to change
- User selects favorites → Reinforce successful patterns

### Pattern Recognition
- Identify which scenarios get positive feedback
- Track which characters users love
- Learn which structures engage users

### Genre Mastery
- Build genre-specific templates
- Learn genre conventions and tropes
- Adapt to sub-genre preferences

## Storage

```json
{
  "style_preferences": {
    "genre": "sci-fi",
    "tone": "hopeful",
    "pacing": "medium",
    "dialogue": "natural"
  },
  "favorite_characters": [],
  "scenario_archive": [],
  "feedback_history": [],
  "genre_templates": {
    "sci-fi": {"structure": "three-act", "themes": ["technology", "humanity"]},
    "drama": {"structure": "hero-journey", "themes": ["growth", "loss"]}
  }
}
```

---

## Triggers

> Learnings are pulled when these triggers fire.

| Trigger | Action | Learning Applied |
|---------|--------|------------------|
| `on_scenario_requested` | Load style preferences | Genre, tone, pacing |
| `on_genre_specified` | Load genre template | Genre-specific rules |
| `on_character_created` | Store character pattern | Character library |
| `on_revision_requested` | Analyze changes | Feedback patterns |
| `on_scenario_approved` | Reinforce successful patterns | Positive feedback |
| `on_scenario_rejected` | Learn what to avoid | Negative feedback |
| `on_dialogue_written` | Track dialogue style | Dialogue patterns |
| `on_act_structure_used` | Store structure preference | Structure patterns |
| `daily_review` | Analyze feedback trends | Pattern analysis |
| `weekly_optimization` | Update genre templates | Template refinement |

### Trigger Example

```python
def on_scenario_requested(genre: str, tone: str):
    """Trigger: pulls style learnings."""
    # Pull from learning store
    style_prefs = pull_learning("style_preferences")
    genre_templates = pull_learning("genre_templates")
    
    # Apply learnings
    template = genre_templates.get(genre, default_template)
    style = {**style_prefs, "genre": genre, "tone": tone}
    
    return template, style
```

---

## Actual Learnings (Distilled)

> New learnings are appended below after each distillation cycle.

| Date | Learning | Source | Trigger | Action Taken |
|------|----------|--------|---------|--------------|
| | | | | |