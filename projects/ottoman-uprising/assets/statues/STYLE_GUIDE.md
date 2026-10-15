# High-Quality SVG Style Guide for Ottoman Uprising Statues

## Quality Standards

### 1. Anatomy & Proportions
- Human figure: Head = 1/7 of total height
- Proper muscle structure visible through armor
- Natural pose with weight distribution
- Hands and feet must be properly formed (5 fingers, anatomical)

### 2. Texture Requirements

#### Bronze (Tigranes, Merchant)
```svg
<!-- Multi-layer bronze texture -->
<filter id="bronzeTexture">
  <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="4" result="noise"/>
  <feDisplacementMap in="SourceGraphic" in2="noise" scale="2" result="displaced"/>
  <feGaussianBlur in="displaced" stdDeviation="0.3"/>
</filter>

<!-- Patina overlay -->
<filter id="patina">
  <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="3"/>
  <feColorMatrix type="matrix" values="0 0 0 0 0.18  0 0 0 0 0.55  0 0 0 0 0.34  0 0 0 0.4 0"/>
  <feComposite in2="SourceGraphic" operator="in"/>
</filter>
```

#### Marble (Gregory, Artashes)
```svg
<!-- Marble veining -->
<filter id="marbleVeins">
  <feTurbulence type="turbulence" baseFrequency="0.01 0.05" numOctaves="4" seed="2"/>
  <feColorMatrix type="matrix" values="0 0 0 0 0.9  0 0 0 0 0.88  0 0 0 0 0.85  0 0 0 0.15 0"/>
  <feComposite in2="SourceGraphic" operator="in"/>
</filter>
```

#### Stone (Anahit, Fallen Warrior)
```svg
<!-- Rough stone texture -->
<filter id="roughStone">
  <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="5" result="noise"/>
  <feDiffuseLighting in="noise" lighting-color="#8a8a8a" surfaceScale="3" result="diffLight">
    <feDistantLight azimuth="135" elevation="55"/>
  </feDiffuseLighting>
  <feComposite in="diffLight" in2="SourceGraphic" operator="in"/>
</filter>
```

### 3. Lighting System

#### Primary Light Sources
- **Key Light**: Main illumination (warm, from torch/sun)
- **Fill Light**: Secondary (cool, ambient)
- **Rim Light**: Edge highlighting (backlight)
- **Accent Light**: Details (sparks, magical glow)

#### Shadow System
```svg
<!-- Drop shadow with color -->
<filter id="coloredShadow">
  <feGaussianBlur in="SourceAlpha" stdDeviation="4" result="blur"/>
  <feOffset dx="3" dy="5" result="offsetBlur"/>
  <feFlood flood-color="#1a1a2e" flood-opacity="0.6" result="color"/>
  <feComposite in="color" in2="offsetBlur" operator="in" result="shadow"/>
  <feMerge>
    <feMergeNode in="shadow"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
```

### 4. Detail Elements

#### Armenian Khachkar Pattern
```svg
<g class="khachkar">
  <!-- Central cross -->
  <rect x="-2" y="-15" width="4" height="30" fill="currentColor"/>
  <rect x="-10" y="-2" width="20" height="4" fill="currentColor"/>
  <!-- Ornamental circles -->
  <circle cx="0" cy="-12" r="3" fill="none" stroke="currentColor"/>
  <circle cx="0" cy="12" r="3" fill="none" stroke="currentColor"/>
  <!-- Vine patterns -->
  <path d="M-8,-15 Q-12,-10 -8,-5 Q-4,0 -8,5 Q-12,10 -8,15" fill="none" stroke="currentColor"/>
  <path d="M8,-15 Q12,-10 8,-5 Q4,0 8,5 Q12,10 8,15" fill="none" stroke="currentColor"/>
</g>
```

#### Armenian Inscription Font
```svg
<style>
  .armenian-text {
    font-family: 'Noto Sans Armenian', 'Arial Unicode MS', sans-serif;
    font-size: 14px;
    fill: currentColor;
    letter-spacing: 2px;
  }
</style>
```

### 5. Atmospheric Effects

#### Fire/Torch Glow
```svg
<filter id="fireGlow">
  <feGaussianBlur stdDeviation="6" result="blur1"/>
  <feGaussianBlur stdDeviation="12" result="blur2"/>
  <feMerge>
    <feMergeNode in="blur2"/>
    <feMergeNode in="blur1"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
```

#### Dust Particles
```svg
<g class="dust-particles">
  <circle cx="100" cy="200" r="1" fill="#ffd700" opacity="0.6">
    <animate attributeName="cy" values="200;180;200" dur="4s" repeatCount="indefinite"/>
  </circle>
  <!-- More particles... -->
</g>
```

#### Mist/Fog
```svg
<filter id="mist">
  <feTurbulence type="fractalNoise" baseFrequency="0.01" numOctaves="3" result="noise"/>
  <feDisplacementMap in="SourceGraphic" in2="noise" scale="20"/>
  <feGaussianBlur stdDeviation="8"/>
</filter>
```

### 6. File Structure Template

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800">
  <defs>
    <!-- Gradients -->
    <!-- Filters -->
    <!-- Patterns -->
    <!-- Clip paths -->
  </defs>
  
  <!-- Background layer -->
  <g id="background">
    <!-- Environment details -->
  </g>
  
  <!-- Midground layer -->
  <g id="midground">
    <!-- Secondary elements -->
  </g>
  
  <!-- Statue layer -->
  <g id="statue">
    <!-- Statue base -->
    <!-- Statue body (bottom to top) -->
    <!-- Statue details -->
    <!-- Statue effects -->
  </g>
  
  <!-- Foreground layer -->
  <g id="foreground">
    <!-- Near elements -->
  </g>
  
  <!-- Effects layer -->
  <g id="effects">
    <!-- Lighting -->
    <!-- Particles -->
    <!-- Glow -->
  </g>
</svg>
```

### 7. Color Palettes

#### Bronze Statue
- Base: #8B6914, #CD853F, #8B7355
- Highlight: #DAA520, #FFD700
- Shadow: #6B4423, #4A3728
- Patina: #2E8B57, #3CB371

#### Marble Statue
- Base: #F5F5F5, #E8E8E8, #DCDCDC
- Veins: #C0C0C0, #A9A9A9
- Shadow: #808080, #696969
- Highlight: #FFFFFF

#### Stone Statue
- Base: #808080, #696969, #585858
- Highlight: #A9A9A9, #C0C0C0
- Shadow: #404040, #2F2F2F
- Moss: #228B22, #2E8B57

#### Dark Obsidian (Emperor)
- Base: #1a1a1a, #2d2d2d, #0d0d0d
- Highlight: #404040, #525252
- Reflection: #FF4500, #8B0000
- Glow: #FF0000, #DC143C
