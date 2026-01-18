# BannerLord 🎨

AI-powered banner generation tool using the Swarms framework and ControlNet for precise, editable banner creation.

## Features

✨ **AI Design Intelligence** - Uses Swarms framework agent to provide expert design recommendations
🎯 **ControlNet Integration** - Precise image generation with layout control
🎨 **Fully Editable Output** - Export to SVG and layered formats for editing in any design program
⚙️ **Customizable Everything** - Control text positioning, fonts, colors, and sizes
🚀 **Easy to Use** - Simple CLI interface with sensible defaults

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ZackBradshaw/BannerLord.git
cd BannerLord
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Quick Start

### Basic Usage

Create a banner with default settings:
```bash
python bannerlord.py --prompt "modern tech startup" --text "INNOVATE"
```

### Advanced Usage

Create a banner with custom positioning and colors:
```bash
python bannerlord.py \
  --prompt "gaming tournament poster" \
  --text "CHAMPION 2024" \
  --position left \
  --color "#FFD700" \
  --width 1920 \
  --height 1080 \
  --font-size 96
```

### Skip ControlNet for Faster Generation

If you don't need precise layout control:
```bash
python bannerlord.py \
  --prompt "minimalist design" \
  --text "SIMPLE" \
  --no-controlnet
```

## Output Formats

BannerLord creates multiple output files for maximum flexibility:

- **`banner.png`** - Final composite banner (ready to use)
- **`banner.svg`** - Editable SVG with text layers (for Inkscape, Illustrator, etc.)
- **`banner_background.png`** - Background image only
- **`banner_metadata.json`** - Complete banner specification for programmatic editing
- **`banner_control.png`** - ControlNet control image (for reference)

## How It Works

### 1. AI Design Agent (Swarms Framework)

The Swarms agent analyzes your prompt and provides:
- Design concept and visual direction
- Harmonious color schemes with hex codes
- Typography recommendations
- Layout and composition suggestions
- Optimized image generation prompts

### 2. ControlNet Image Generation

Uses Stable Diffusion with ControlNet to generate backgrounds with precise layout control:
- Creates control images based on your text positioning
- Guides the AI to respect text areas and layout structure
- Supports multiple ControlNet types (canny, depth, pose, scribble)

### 3. Banner Composition

Composites text onto the generated background with:
- Custom fonts, sizes, and colors
- Text stroke and shadow effects
- Precise positioning control
- Multiple text layers support

### 4. Multi-Format Export

Exports to editable formats:
- **SVG** - Edit text, colors, fonts in vector programs
- **PNG + Metadata** - Programmatically edit layers
- **Separated layers** - Edit background and text independently

## API Usage

You can also use BannerLord as a Python library:

```python
from bannerlord import BannerLord

# Initialize
app = BannerLord(api_key="your-openai-key")

# Create banner
output_path = app.create_banner(
    user_prompt="futuristic sci-fi theme",
    text="THE FUTURE",
    width=1920,
    height=1080,
    text_position="center",
    font_size=96,
    text_color="#00FFFF",
    use_controlnet=True,
    output_name="scifi_banner"
)

print(f"Banner created: {output_path}")
```

## Architecture

### Components

1. **`banner_agent.py`** - Swarms AI agent for design intelligence
2. **`controlnet_generator.py`** - ControlNet integration for image generation
3. **`banner_compositor.py`** - Text overlay and multi-format export
4. **`bannerlord.py`** - Main CLI application

### Technology Stack

- **Swarms** - AI agent framework for intelligent design recommendations
- **Stable Diffusion + ControlNet** - Precise image generation
- **PIL/Pillow** - Image manipulation
- **svgwrite** - SVG export for editability
- **PyTorch** - Deep learning backend

## Configuration

### Environment Variables

```bash
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_TOKEN=your_huggingface_token_here  # Optional
```

### CLI Arguments

```
--prompt          Description of the banner (required)
--text            Text to display (required)
--width           Banner width in pixels (default: 1024)
--height          Banner height in pixels (default: 512)
--position        Text position: left/center/right/top/bottom (default: center)
--font-size       Font size in pixels (default: 72)
--color           Text color as hex (default: #FFFFFF)
--no-controlnet   Skip ControlNet for faster generation
--output          Base name for output files (default: banner)
--api-key         OpenAI API key (overrides env var)
```

## Examples

### Example 1: Corporate Banner
```bash
python bannerlord.py \
  --prompt "professional corporate blue theme for technology company" \
  --text "ENTERPRISE SOLUTIONS" \
  --position center \
  --color "#1E88E5" \
  --width 1200 \
  --height 400
```

### Example 2: Event Poster
```bash
python bannerlord.py \
  --prompt "vibrant music festival with colorful abstract background" \
  --text "SUMMER FEST 2024" \
  --position top \
  --color "#FF6B6B" \
  --width 1080 \
  --height 1920
```

### Example 3: Gaming Banner
```bash
python bannerlord.py \
  --prompt "dark cyberpunk aesthetic with neon lights" \
  --text "GAME ON" \
  --position center \
  --color "#00FFFF" \
  --font-size 120
```

## Editing Generated Banners

### In Inkscape (Free)
1. Open the `.svg` file
2. Select text elements to edit text, font, color
3. Edit background as needed
4. Export as PNG or PDF

### In Adobe Illustrator
1. Open the `.svg` file
2. Text layers are fully editable
3. Modify positioning, styling, effects
4. Export to any format

### Programmatically
1. Load the `_metadata.json` file
2. Modify text layer properties
3. Use `BannerCompositor.load_from_metadata()` to recreate
4. Re-export with new settings

## Requirements

- Python 3.8+
- CUDA-capable GPU recommended (for ControlNet)
- 8GB+ RAM
- OpenAI API key

## Troubleshooting

### Out of Memory Error
- Reduce image size with `--width` and `--height`
- Use `--no-controlnet` to skip ControlNet generation
- Enable CPU offloading (automatic on CUDA)

### API Key Not Found
- Set `OPENAI_API_KEY` environment variable
- Or use `--api-key` argument
- Or create `.env` file from `.env.example`

### Font Not Found
- System uses fallback fonts automatically
- Install DejaVu or Liberation fonts for better results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Credits

Built with:
- [Swarms](https://github.com/kyegomez/swarms) - AI agent framework
- [Diffusers](https://github.com/huggingface/diffusers) - Stable Diffusion + ControlNet
- [Pillow](https://python-pillow.org/) - Image processing

## Support

For issues, questions, or feature requests, please open an issue on GitHub.
