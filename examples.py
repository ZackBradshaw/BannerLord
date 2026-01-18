"""
Example Usage of BannerLord
Demonstrates various ways to use the banner generation tool
"""

from bannerlord import BannerLord
from pathlib import Path


def example_1_simple_banner():
    """Create a simple banner with default settings."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Simple Banner")
    print("="*70)
    
    app = BannerLord()
    
    output = app.create_banner(
        user_prompt="modern tech startup with clean design",
        text="INNOVATE",
        output_name="example1_simple"
    )
    
    print(f"\n✅ Created: {output}")


def example_2_custom_position():
    """Create a banner with custom text positioning."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Custom Text Position")
    print("="*70)
    
    app = BannerLord()
    
    output = app.create_banner(
        user_prompt="gaming tournament poster with dramatic lighting",
        text="CHAMPION 2024",
        text_position="left",
        font_size=96,
        text_color="#FFD700",
        width=1920,
        height=1080,
        output_name="example2_gaming"
    )
    
    print(f"\n✅ Created: {output}")


def example_3_no_controlnet():
    """Create a banner without ControlNet for faster generation."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Fast Generation (No ControlNet)")
    print("="*70)
    
    app = BannerLord()
    
    output = app.create_banner(
        user_prompt="minimalist corporate design",
        text="ENTERPRISE",
        use_controlnet=False,
        output_name="example3_fast"
    )
    
    print(f"\n✅ Created: {output}")


def example_4_multiple_variations():
    """Create multiple banner variations."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Multiple Variations")
    print("="*70)
    
    app = BannerLord()
    
    base_prompt = "professional technology conference"
    texts = ["INNOVATE", "CONNECT", "CREATE"]
    colors = ["#3498db", "#2ecc71", "#f39c12"]
    
    for i, (text, color) in enumerate(zip(texts, colors)):
        output = app.create_banner(
            user_prompt=base_prompt,
            text=text,
            text_color=color,
            output_name=f"example4_variation_{i+1}"
        )
        print(f"\n✅ Created variation {i+1}: {output}")


def example_5_agent_only():
    """Use just the AI agent to get design recommendations."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Design Consultation Only")
    print("="*70)
    
    from banner_agent import BannerDesignAgent
    
    agent = BannerDesignAgent()
    
    prompt = """
    I need a banner for a summer music festival. It should feel energetic and fun.
    The text should say "SUMMER BEATS 2024" and I want it to appeal to young adults.
    Colors should be vibrant and the style should be modern.
    """
    
    recommendations = agent.design_banner(prompt)
    
    print("\n🎨 Design Recommendations:")
    print("-" * 70)
    print(recommendations)
    print("-" * 70)


def example_6_compositor_only():
    """Use compositor to add text to an existing image."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Add Text to Existing Image")
    print("="*70)
    
    from banner_compositor import BannerCompositor
    from PIL import Image
    
    # Create a sample background
    background = Image.new('RGB', (1024, 512), color='#2c3e50')
    
    compositor = BannerCompositor()
    
    # Add multiple text elements
    text_elements = [
        {
            'text': 'BannerLord',
            'position': (512, 200),
            'font_size': 80,
            'color': '#ffffff',
            'shadow': True
        },
        {
            'text': 'AI-Powered Design',
            'position': (512, 320),
            'font_size': 40,
            'color': '#3498db',
            'shadow': True
        }
    ]
    
    result = compositor.create_composite_banner(
        background=background,
        text_elements=text_elements,
        output_path="outputs/example6_composite.png"
    )
    
    print("\n✅ Created composite banner")


def example_7_svg_export():
    """Create an SVG banner for maximum editability."""
    print("\n" + "="*70)
    print("EXAMPLE 7: SVG Export")
    print("="*70)
    
    from banner_compositor import BannerCompositor
    from PIL import Image
    
    background = Image.new('RGB', (1200, 400), color='#34495e')
    bg_path = "outputs/example7_bg.png"
    background.save(bg_path)
    
    compositor = BannerCompositor()
    
    text_layers = [
        {
            'text': 'EDITABLE BANNER',
            'x': 600,
            'y': 200,
            'font_size': 72,
            'font_family': 'Arial',
            'color': '#ecf0f1',
            'stroke_color': '#2c3e50',
            'stroke_width': 3
        }
    ]
    
    compositor.export_as_svg(
        output_path="outputs/example7_editable.svg",
        width=1200,
        height=400,
        background_image_path=bg_path,
        text_layers=text_layers
    )
    
    print("\n✅ Created editable SVG banner")
    print("💡 Open outputs/example7_editable.svg in Inkscape or Illustrator to edit!")


def main():
    """Run all examples."""
    print("\n" + "🎨"*35)
    print("BANNERLORD EXAMPLES")
    print("🎨"*35)
    
    examples = [
        ("Simple Banner", example_1_simple_banner),
        ("Custom Position", example_2_custom_position),
        ("Fast Generation", example_3_no_controlnet),
        ("Multiple Variations", example_4_multiple_variations),
        ("Design Consultation", example_5_agent_only),
        ("Compositor Only", example_6_compositor_only),
        ("SVG Export", example_7_svg_export),
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nNote: Examples 1-4 require OpenAI API key and may take time.")
    print("Examples 5-7 are faster and demonstrate individual components.\n")
    
    choice = input("Enter example number to run (or 'all' to run 5-7): ").strip()
    
    if choice.lower() == 'all':
        # Run only lightweight examples
        for i in [4, 5, 6]:
            try:
                examples[i][1]()
            except Exception as e:
                print(f"\n❌ Error in example {i+1}: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        idx = int(choice) - 1
        try:
            examples[idx][1]()
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        print("Invalid choice. Please run again and select a valid example.")


if __name__ == "__main__":
    main()
