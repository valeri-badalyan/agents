# User Interface Design - Ottoman Uprising (Hero of Armenia)

## UI Philosophy
**Medieval Manuscript Meets Modern Clarity**
- Ornate historical aesthetics with functional modern UI
- Minimalist during gameplay, detailed during menus
- Cultural authenticity in all visual elements
- Responsive and intuitive interaction design

---

## Main Menu Layout

### Background
**Scene:** Armenian highlands at dawn with Chenani's fortress visible in distance
**Animation:** Subtle parallax scrolling, birds in flight, mist moving through valleys
**Lighting:** Golden hour light, long shadows, atmospheric depth

### Menu Structure
```
[Center Screen]
┌─────────────────────────────────────────────┐
│              OTTOMAN UPRISING                │
│            (Hero of Armenia)                 │
│                                             │
│         [Main Title with Armenian motifs]    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │         New Campaign                │    │
│  │         Continue                    │    │
│  │         Multiplayer                 │    │
│  │         Options                     │    │
│  │         Credits                     │    │
│  │         Exit                        │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  [Subtle animated Armenian cross symbol]    │
│                                             │
└─────────────────────────────────────────────┘
```

### Visual Elements
- **Title Font:** Armenian-inspired serif with metallic texture
- **Menu Buttons:** Stone-textured with gold trim
- **Selection Highlight:** Warm glow with subtle particle effects
- **Background Music:** Traditional Armenian instruments (duduk, tar)

---

## In-Game HUD

### Health & Status Panel (Top Left)
```
┌─────────────────────────────────┐
│ [Avatar] Hero Name              │
│ ████████████░░░░  Health        │
│ ██████████░░░░░░  Stamina       │
│ ▲▲▲▲▲▲▲▲▲▲  Reputation        │
│ ⚔️ Sword Skill  🛡️ Defense    │
│ 🔍 Stealth Level                │
└─────────────────────────────────┘
```

**Design Notes:**
- Avatar: Circular frame with Armenian knot border
- Health Bar: Red with stone texture background
- Stamina Bar: Blue with flowing water texture
- Reputation: Gold stars with cultural motifs
- Skills: Pictographic icons with level indicators

### Resources Panel (Top Right)
```
┌─────────────────────────────────┐
│  💰 Gold: 1,250                 │
│  🍖 Food: 850                   │
│  ⚒️ Materials: 420              │
│  📜 Scrolls: 12                 │
│  ⏱️ Time: Day 3, Hour 14       │
└─────────────────────────────────┘
```

**Design Notes:**
- Resources use medieval manuscript style icons
- Numbers in Armenian-inspired numerals
- Time shown with sundial/clock aesthetic
- Warning states with color changes (red for low resources)

### Minimap (Bottom Right)
```
┌─────────────────────────────────┐
│  ┌─────────────────────────┐    │
│  │                         │    │
│  │      Minimap View       │    │
│  │                         │    │
│  │   [Player] [Enemies]    │    │
│  │   [Allies] [Objectives] │    │
│  │                         │    │
│  └─────────────────────────┘    │
│  [Compass Rose] [Zoom Controls] │
└─────────────────────────────────┘
```

**Design Notes:**
- Circular minimap with parchment texture border
- Color-coded units: Green (player), Red (enemies), Blue (allies)
- Objective markers with pulsing animation
- Compass rose with Armenian cross at center
- Zoom controls with stone button aesthetic

### Action Bar (Bottom Center)
```
┌─────────────────────────────────────────────┐
│  [1]⚔️  [2]🛡️  [3]🔍  [4]🎭  [5]💀       │
│  Attack  Defend  Stealth  Ability  Special  │
│                                             │
│  [Hotbar Items: 🗡️ 🧪 📜 🔑 ⚔️]           │
└─────────────────────────────────────────────┘
```

**Design Notes:**
- Stone-textured action slots with gold numbering
- Icons: Hand-painted style with clear silhouettes
- Cooldown indicators with hourglass animation
- Active ability glow effects
- Hotbar with scroll-like texture

### Quick Inventory (Bottom Left)
```
┌─────────────────────────────────┐
│  🎒 Quick Access:               │
│  [Slot 1] [Slot 2] [Slot 3]    │
│  [Slot 4] [Slot 5] [Slot 6]    │
│                                 │
│  [Encumbrance: ████░░░░ 65%]   │
└─────────────────────────────────┘
```

---

## Inventory Screen

### Layout
```
┌─────────────────────────────────────────────────────┐
│  [Character Portrait]  │  [Inventory Grid]          │
│                        │  ┌──────────────────────┐  │
│  Name: [Hero Name]     │  │ 1  2  3  4  5  6  7  │  │
│  Class: [Class]        │  │ 8  9  10 11 12 13 14  │  │
│  Level: [Level]        │  │ 15 16 17 18 19 20 21  │  │
│                        │  │ 22 23 24 25 26 27 28  │  │
│  [Equipment Slots]     │  │ 29 30 31 32 33 34 35  │  │
│  🗡️ Weapon             │  └──────────────────────┘  │
│  🛡️ Shield             │                            │
│  🎭 Head               │  [Item Details Panel]      │
│  👕 Chest              │  ┌──────────────────────┐  │
│  🥾 Legs               │  │ Item Name            │  │
│  🧤 Hands              │  │ Description...       │  │
│  💍 Ring               │  │ Stats: +10 Attack    │  │
│  🔮 Amulet             │  │ [Use] [Equip] [Drop] │  │
│                        │  └──────────────────────┘  │
│  [Weight: 45/100]      │                            │
│  [Gold: 1,250]         │  [Sort] [Filter] [Search] │
└─────────────────────────────────────────────────────┘
```

### Visual Design
- **Background:** Parchment texture with ink borders
- **Item Grid:** Stone tiles with item icons
- **Equipment Slots:** Character-shaped outline
- **Item Rarity:** Color-coded borders (Common, Uncommon, Rare, Epic, Legendary)
- **Tooltips:** Ornate frame with historical manuscript styling

---

## Character Stats Panel

### Layout
```
┌─────────────────────────────────────────────────────┐
│  CHARACTER STATS                                     │
├─────────────────────────────────────────────────────┤
│  [Character Name] - [Class] - Level [X]             │
│                                                     │
│  ┌───────────────┐  ┌───────────────────────────┐   │
│  │  Attributes   │  │  Skills                   │   │
│  │  STR: [XX]    │  │  Swordsmanship: [XX/100]  │   │
│  │  DEX: [XX]    │  │  Stealth: [XX/100]        │   │
│  │  CON: [XX]    │  │  Archery: [XX/100]        │   │
│  │  INT: [XX]    │  │  Diplomacy: [XX/100]      │   │
│  │  WIS: [XX]    │  │  Herbalism: [XX/100]      │   │
│  │  CHA: [XX]    │  │  Leadership: [XX/100]     │   │
│  └───────────────┘  └───────────────────────────┘   │
│                                                     │
│  ┌───────────────┐  ┌───────────────────────────┐   │
│  │  Perks        │  │  Reputation               │   │
│  │  [Perk 1]     │  │  Armenians: [XX/100]      │   │
│  │  [Perk 2]     │  │  Turks: [XX/100]           │   │
│  │  [Perk 3]     │  │  Church: [XX/100]          │   │
│  │  [Perk 4]     │  │  Thieves: [XX/100]         │   │
│  └───────────────┘  └───────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### Visual Design
- **Attribute Bars:** Filled with gradient colors
- **Skill Icons:** Hand-drawn style with level indicators
- **Perk Tree:** Branching paths with unlock animations
- **Reputation Meters:** Faction-specific iconography

---

## Map Screen

### Layout
```
┌─────────────────────────────────────────────────────┐
│  WORLD MAP - Armenian Highlands & Turkish Territories│
├─────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────┐  │
│  │                                               │  │
│  │              [Main Map View]                  │  │
│  │                                               │  │
│  │   [Armenian Territories]                      │  │
│  │   [Border Zones]                              │  │
│  │   [Turkish Territories]                       │  │
│  │   [Key Locations]                             │  │
│  │   [Current Position]                          │  │
│  │   [Objective Markers]                         │  │
│  │                                               │  │
│  └───────────────────────────────────────────────┘  │
│                                                     │
│  [Map Legend]  │  [Location Details]  │  [Fast Travel]│
└─────────────────────────────────────────────────────┘
```

### Map Features
- **Terrain:** Topographic style with elevation lines
- **Political Boundaries:** Color-coded territories
- **Roads:** Detailed path networks
- **Settlements:** Icons based on size and type
- **Points of Interest:** Star markers for key locations
- **Fog of War:** Unexplored areas in shadow

### Interaction Elements
- **Hover Effects:** Location name and brief description
- **Click Actions:** Detailed information panel
- **Zoom Levels:** Strategic to tactical view
- **Filter Options:** Show/hide different map elements

---

## Dialogue Boxes

### Standard Dialogue
```
┌─────────────────────────────────────────────┐
│  [Speaker Portrait]                         │
│  ┌─────────────────────────────────────┐    │
│  │  " dialogue text with medieval      │    │
│  │    styling and authentic fonts"     │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  [Response Options]                         │
│  1. [Diplomatic Response]                   │
│  2. [Aggressive Response]                   │
│  3. [Stealth Response]                      │
│  4. [Ask for More Information]              │
└─────────────────────────────────────────────┘
```

### Visual Design
- **Frame:** Ornate stone frame with cultural motifs
- **Text:** Medieval-style font with drop caps
- **Speaker Name:** Highlighted with faction color
- **Response Options:** Stone buttons with hover effects
- **Portrait:** Animated character portrait with emotion states

---

## Notification System

### Alert Types
1. **Critical:** Red border, urgent sound
2. **Important:** Gold border, attention sound
3. **Informational:** Blue border, subtle sound
4. **Success:** Green border, positive sound

### Visual Design
- **Location:** Top center of screen
- **Duration:** 3-5 seconds or until dismissed
- **Animation:** Slide in/out with fade
- **Iconography:** Pictographic with text backup

---

## Tutorial System

### In-Game Tutorials
- **Highlight Effects:** Glowing borders on interactive elements
- **Step-by-Step Guides:** Numbered instructions with arrows
- **Practice Areas:** Safe zones for learning mechanics
- **Progress Tracking:** Completion indicators

### Visual Design
- **Tutorial Boxes:** Parchment style with clear instructions
- **Button Highlights:** Pulsing glow effects
- **Arrow Indicators:** Animated directional cues
- **Progress Bars:** Visual completion tracking

---

## Settings Menu

### Options Categories
1. **Graphics:** Resolution, quality, effects
2. **Audio:** Music, effects, voice volume
3. **Controls:** Keybindings, sensitivity
4. **Gameplay:** Difficulty, assistance options
5. **Accessibility:** Colorblind modes, text size

### Visual Design
- **Sliders:** Stone-textured with gold indicators
- **Dropdowns:** Medieval scroll style
- **Checkboxes:** Ornate box with checkmark
- **Save/Load:** Book-style interface

---

## Multiplayer Interface

### Lobby Design
- **Player List:** Character portraits with status
- **Chat System:** Medieval scroll style
- **Game Settings:** Host controls
- **Ready System:** Checkmark indicators

### In-Game Multiplayer
- **Alliance Indicators:** Team colors
- **Communication:** Quick chat wheel
- **Scoreboard:** Period-appropriate design
- **Spectator Mode:** Cinematic camera options

---

*This UI design creates an immersive historical experience while maintaining modern usability standards. All elements balance aesthetic authenticity with functional clarity.*