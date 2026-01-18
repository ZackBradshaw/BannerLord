# BannerLord Quick Start Guide

## Overview

BannerLord is an AI-powered banner generation tool that combines the Swarms framework for intelligent design recommendations with ControlNet for precise image generation. It creates fully editable banners that can be customized in any design program.

## Installation

### 1. Quick Setup (Automated)

```bash
# Clone the repository
git clone https://github.com/ZackBradshaw/BannerLord.git
cd BannerLord

# Run the setup script
./setup.sh
```

### 2. Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Basic Usage

### Command Line Interface

The simplest way to create a banner:

```bash
python bannerlord.py --prompt "modern tech startup" --text "INNOVATE"
```

### Full Options

```bash
python bannerlord.py \
  --prompt "gaming tournament poster" \
  --text "CHAMPION 2024" \
  --width 1920 \
  --height 1080 \
  --position center \
  --font-size 96 \
  --color "#FFD700" \
  --output my_banner
```

### Available Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--prompt` | Description of desired banner style (required) | - |
| `--text` | Text to display on banner (required) | - |
| `--width` | Banner width in pixels | 1024 |
| `--height` | Banner height in pixels | 512 |
| `--position` | Text position (left/center/right/top/bottom) | center |
| `--font-size` | Font size in pixels | 72 |
| `--color` | Text color as hex code | #FFFFFF |
| `--no-controlnet` | Skip ControlNet for faster generation | false |
| `--output` | Base name for output files | banner |

## Features in Detail

### 1. AI Design Agent (Swarms Framework)

The Swarms agent acts as your personal design consultant:

- **Analyzes** your prompt to understand your vision
- **Recommends** color schemes with specific hex codes
- **Suggests** typography and font styles
- **Provides** layout and composition guidance
- **Generates** optimized prompts for image generation

**Example:**
```python
from banner_agent import BannerDesignAgent

agent = BannerDesignAgent()
recommendations = agent.design_banner(
    "Create a banner for a music festival with vibrant colors"
)
print(recommendations)
```

### 2. ControlNet Integration

ControlNet ensures your AI-generated backgrounds respect text positioning and layout:

- **Creates control images** that define layout structure
- **Guides AI generation** to avoid text areas
- **Supports multiple modes** (canny, depth, pose, scribble)
- **Provides precision** while maintaining creative freedom

**Example:**
```python
from controlnet_generator import ControlNetBannerGenerator

generator = ControlNetBannerGenerator(controlnet_type="canny")
generator.load_model()

# Create control image
control = generator.create_control_image(
    width=1024, height=512,
    text_position="center",
    layout_type="minimal"
)

# Generate background
background = generator.generate_banner(
    prompt="futuristic tech background with neon lights",
    control_image=control
)
```

### 3. Text Composition

Add text with full customization:

- **Positioning:** Place text anywhere (or auto-center)
- **Fonts:** Use any system font
- **Colors:** Any hex color or named color
- **Effects:** Text stroke, shadow, transparency
- **Multiple layers:** Add as many text elements as needed

**Example:**
```python
from banner_compositor import BannerCompositor
from PIL import Image

compositor = BannerCompositor()
background = Image.open("background.png")

banner = compositor.add_text_to_banner(
    background=background,
    text="HELLO WORLD",
    position=(512, 256),
    font_size=80,
    color="#FFFFFF",
    stroke_width=3,
    stroke_color="#000000",
    shadow=True
)
```

### 4. Editable Export Formats

#### SVG Export (Best for Editing)
```python
compositor.export_as_svg(
    output_path="banner.svg",
    width=1024,
    height=512,
    background_image_path="background.png",
    text_layers=[{
        'text': 'EDITABLE',
        'x': 512, 'y': 256,
        'font_size': 72,
        'color': '#FFFFFF'
    }]
)
```

**Edit in:**
- Inkscape (free)
- Adobe Illustrator
- Figma
- Any SVG editor

#### Metadata Export (Best for Programmatic Editing)
```python
compositor.export_with_metadata(
    output_path="banner",
    background=background_image,
    text_layers=[...]
)

# Later, load and modify:
bg, layers = compositor.load_from_metadata("banner_metadata.json")
# Modify layers as needed
# Recreate banner with new settings
```

## Common Use Cases

### Use Case 1: Social Media Banner
```bash
python bannerlord.py \
  --prompt "vibrant social media banner for tech blog" \
  --text "TECH INSIGHTS" \
  --width 1200 \
  --height 628 \
  --position center \
  --color "#FF6B6B"
```

### Use Case 2: YouTube Thumbnail
```bash
python bannerlord.py \
  --prompt "dramatic gaming video thumbnail with dark theme" \
  --text "EPIC GAMEPLAY" \
  --width 1280 \
  --height 720 \
  --position left \
  --font-size 90 \
  --color "#FFD700"
```

### Use Case 3: Event Poster
```bash
python bannerlord.py \
  --prompt "professional conference poster with corporate blue" \
  --text "TECH SUMMIT 2024" \
  --width 1080 \
  --height 1920 \
  --position top \
  --font-size 80 \
  --color "#1E88E5"
```

### Use Case 4: Fast Prototype (No ControlNet)
```bash
python bannerlord.py \
  --prompt "minimalist design" \
  --text "PROTOTYPE" \
  --no-controlnet
```

## Python API Usage

### Complete Workflow
```python
from bannerlord import BannerLord

# Initialize
app = BannerLord(api_key="your-openai-key")

# Create banner
output = app.create_banner(
    user_prompt="cyberpunk aesthetic with neon lights",
    text="CYBER CITY",
    width=1920,
    height=1080,
    text_position="center",
    font_size=120,
    text_color="#00FFFF",
    use_controlnet=True,
    output_name="cyberpunk_banner"
)

print(f"Banner created: {output}")
```

### Using Individual Components

```python
# Just get design recommendations
from banner_agent import BannerDesignAgent
agent = BannerDesignAgent()
design = agent.design_banner("vintage music poster")

# Just add text to existing image
from banner_compositor import BannerCompositor
compositor = BannerCompositor()
result = compositor.add_text_to_banner(my_image, "TEXT")

# Just generate background with ControlNet
from controlnet_generator import ControlNetBannerGenerator
gen = ControlNetBannerGenerator()
gen.load_model()
bg = gen.generate_banner(prompt, control_image)
```

## Output Files

When you create a banner named "my_banner", you get:

| File | Description | Use For |
|------|-------------|---------|
| `my_banner.png` | Final composite | Direct use |
| `my_banner.svg` | Editable SVG | Vector editing |
| `my_banner_background.png` | Background only | Separate editing |
| `my_banner_metadata.json` | Full specification | Programmatic editing |
| `my_banner_control.png` | ControlNet control | Reference |

## Tips & Best Practices

### Getting Better Results

1. **Be specific in prompts:** "modern tech startup with blue gradient and geometric elements" is better than "tech banner"

2. **Match text position to design:** If your prompt mentions "left side imagery", use `--position right`

3. **Consider aspect ratios:**
   - Social media: 1200x628
   - YouTube: 1280x720
   - Twitter header: 1500x500
   - Instagram: 1080x1080

4. **Use appropriate font sizes:**
   - Large banners (1920px+): 96-120px
   - Medium banners (1024px): 72-96px
   - Small banners (800px): 48-72px

### Editing Generated Banners

**In Inkscape (Free & Open Source):**
1. Open the `.svg` file
2. Click on text to edit
3. Use text toolbar to change font, size, color
4. Export as PNG or PDF

**In Photoshop/GIMP:**
1. Open `_background.png`
2. Load `_metadata.json` to see text specifications
3. Add text layers manually with exact specifications
4. Edit as needed

**Programmatically:**
```python
compositor = BannerCompositor()
bg, layers = compositor.load_from_metadata("banner_metadata.json")

# Modify text
layers[0]['text'] = "NEW TEXT"
layers[0]['color'] = "#FF0000"

# Recreate
new_banner = compositor.create_composite_banner(bg, layers)
```

## Troubleshooting

### "No module named 'swarms'"
```bash
pip install swarms
```

### "OPENAI_API_KEY not found"
```bash
# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env
```

### Out of memory with ControlNet
```bash
# Use smaller dimensions
python bannerlord.py --width 800 --height 400 ...

# Or skip ControlNet
python bannerlord.py --no-controlnet ...
```

### Font not found warnings
System will use fallback fonts automatically. For better results:
```bash
# Ubuntu/Debian
sudo apt-get install fonts-dejavu

# macOS (usually pre-installed)
# Windows (usually pre-installed)
```

## Advanced Configuration

### Custom ControlNet Type
```python
app = BannerLord()
app.initialize_controlnet(controlnet_type="depth")  # or "pose", "scribble"
```

### Custom Color Schemes
```python
# Use design recommendations
design = agent.design_banner(prompt)
colors = design['colors']  # Get recommended colors

# Apply to banner
banner = compositor.add_text_to_banner(
    background, text,
    color=colors[0],
    stroke_color=colors[1]
)
```

### Batch Generation
```python
app = BannerLord()

variations = [
    ("INNOVATE", "#3498db"),
    ("CREATE", "#2ecc71"),
    ("SUCCEED", "#f39c12")
]

for text, color in variations:
    app.create_banner(
        user_prompt=base_prompt,
        text=text,
        text_color=color,
        output_name=f"banner_{text.lower()}"
    )
```

## Examples Gallery

See `examples.py` for complete working examples:

```bash
python examples.py
```

This includes:
- Simple banner creation
- Custom positioning
- Fast generation without ControlNet
- Multiple variations
- Design consultation only
- Compositor-only usage
- SVG export workflow

## Support & Contributing

- **Issues:** https://github.com/ZackBradshaw/BannerLord/issues
- **Discussions:** https://github.com/ZackBradshaw/BannerLord/discussions
- **Contributing:** Pull requests welcome!

## License

MIT License - see LICENSE file
