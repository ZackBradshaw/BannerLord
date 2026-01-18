# BannerLord - Visual Showcase

This document showcases the capabilities of BannerLord with example outputs.

## Demo 1: Professional Tech Banner

![Professional Banner](https://github.com/user-attachments/assets/5b40327a-2a94-4e8e-b2ac-bf47205d6bb6)

**Features:**
- Gradient blue background (professional theme)
- Large "INNOVATE" text with white color
- Text stroke and shadow effects for depth
- Geometric border elements for visual interest
- Dimensions: 1200x400px

**Generated with:**
```bash
python bannerlord.py \
  --prompt "professional tech startup with clean design" \
  --text "INNOVATE" \
  --width 1200 \
  --height 400
```

---

## Demo 2: Multi-Layer Sale Banner

![Multi-Layer Banner](https://github.com/user-attachments/assets/e38bb277-9a95-4b77-b02a-34f663cacff4)

**Features:**
- Split-color design (red/blue contrast)
- Two text layers with different sizes and colors
- "SUMMER" in white with black stroke
- "SALE 2024" in gold (#FFD700)
- Perfect for promotional content
- Dimensions: 1024x512px

**Code example:**
```python
text_elements = [
    {
        'text': 'SUMMER',
        'font_size': 80,
        'color': '#FFFFFF',
        'stroke_width': 4
    },
    {
        'text': 'SALE 2024',
        'font_size': 60,
        'color': '#FFD700',
        'stroke_width': 3
    }
]
```

---

## Key Features Demonstrated

### ✅ Text Customization
- **Font sizes:** From 48px to 120px+
- **Colors:** Any hex color (#FFFFFF, #FFD700, etc.)
- **Positioning:** Left, center, right, top, bottom
- **Effects:** Stroke, shadow, custom fonts

### ✅ Editable Formats
- **PNG:** Ready-to-use final output
- **SVG:** Edit in Inkscape, Illustrator, Figma
- **Metadata JSON:** Programmatic editing
- **Separated layers:** Background + text independent

### ✅ AI-Powered Design
- **Swarms Agent:** Intelligent design recommendations
- **ControlNet:** Precise layout control
- **Color schemes:** Harmonious palettes
- **Typography:** Professional font suggestions

### ✅ Use Cases
- Social media banners
- YouTube thumbnails
- Event posters
- Website headers
- Promotional graphics
- Conference materials

---

## Export Format Examples

### SVG Export (Editable)
```xml
<svg width="1000" height="300">
  <image href="background.png" width="1000" height="300"/>
  <text x="500" y="150" 
        font-size="64" 
        fill="#ecf0f1" 
        stroke="#2c3e50" 
        stroke-width="2">
    EDITABLE BANNER
  </text>
</svg>
```

### Metadata JSON (Programmatic)
```json
{
  "width": 800,
  "height": 400,
  "background": "outputs/banner_background.png",
  "text_layers": [
    {
      "text": "METADATA",
      "position": [400, 200],
      "font_size": 72,
      "color": "#FFFFFF",
      "font_family": "Sans",
      "stroke_width": 3,
      "stroke_color": "#27ae60"
    }
  ]
}
```

---

## Technical Capabilities

### Image Generation
- **Stable Diffusion + ControlNet** for precise backgrounds
- **Multiple ControlNet types:** canny, depth, pose, scribble
- **GPU acceleration** with CUDA/MPS support
- **CPU fallback** for systems without GPU

### Text Rendering
- **PIL/Pillow** for high-quality text rendering
- **TrueType font support** with system font fallback
- **Advanced effects:** stroke, shadow, anti-aliasing
- **Multi-line text** with alignment control

### Design Intelligence
- **Swarms Framework** for AI agent orchestration
- **GPT-4 integration** for design expertise
- **Contextual recommendations** based on user intent
- **Iterative refinement** with feedback support

---

## Performance Notes

### With ControlNet (High Quality)
- **Time:** 30-60 seconds per banner
- **Requirements:** GPU with 4GB+ VRAM recommended
- **Output:** AI-generated backgrounds with precise layout

### Without ControlNet (Fast)
- **Time:** 3-5 seconds per banner
- **Requirements:** Any system with Python
- **Output:** Gradient/solid backgrounds with text

### Agent Only (Consultation)
- **Time:** 5-10 seconds
- **Requirements:** OpenAI API key
- **Output:** Design recommendations and guidance

---

## Real-World Applications

### Marketing & Advertising
- Product launch banners
- Sale promotions
- Brand campaigns
- Social media ads

### Events & Conferences
- Event posters
- Speaker introductions
- Schedule headers
- Venue signage

### Content Creation
- YouTube thumbnails
- Podcast covers
- Blog headers
- Newsletter graphics

### Corporate Communications
- Internal announcements
- Team celebrations
- Milestone markers
- Training materials

---

## Get Started

1. **Install:** `./setup.sh` or `pip install -r requirements.txt`
2. **Configure:** Add OpenAI API key to `.env`
3. **Create:** `python bannerlord.py --prompt "your idea" --text "YOUR TEXT"`
4. **Edit:** Open SVG in your favorite editor
5. **Use:** Deploy banner wherever needed

## Learn More

- **Full Documentation:** [README.md](README.md)
- **Usage Guide:** [GUIDE.md](GUIDE.md)
- **Examples:** Run `python examples.py`
- **Tests:** Run `python test_bannerlord.py`

---

**BannerLord** - AI-Powered Banner Generation with Swarms & ControlNet

*Create professional, editable banners in seconds with intelligent design assistance.*
