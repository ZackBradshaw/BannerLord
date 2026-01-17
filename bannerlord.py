"""
BannerLord - Main CLI Application
AI-powered banner generation tool with ControlNet and editable output
"""

import argparse
import os
import sys
from typing import Optional, Dict, List
import json
from pathlib import Path

from banner_agent import BannerDesignAgent
from controlnet_generator import ControlNetBannerGenerator
from banner_compositor import BannerCompositor


class BannerLord:
    """Main application class for BannerLord banner generation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize BannerLord application.
        
        Args:
            api_key: OpenAI API key for the swarms agent
        """
        self.agent = None
        self.controlnet = None
        self.compositor = BannerCompositor()
        self.api_key = api_key
        
        # Create output directory
        self.output_dir = Path("outputs")
        self.output_dir.mkdir(exist_ok=True)
    
    def initialize_agent(self):
        """Initialize the Swarms design agent."""
        if self.agent is None:
            print("Initializing Banner Design Agent...")
            self.agent = BannerDesignAgent(api_key=self.api_key)
            print("Agent ready!")
    
    def initialize_controlnet(self, controlnet_type: str = "canny"):
        """
        Initialize ControlNet generator.
        
        Args:
            controlnet_type: Type of ControlNet to use
        """
        if self.controlnet is None:
            print(f"Initializing ControlNet ({controlnet_type})...")
            self.controlnet = ControlNetBannerGenerator(controlnet_type=controlnet_type)
            print("ControlNet ready!")
    
    def parse_design_response(self, response: str) -> Dict:
        """
        Parse the agent's design response.
        
        Args:
            response: Agent response text
            
        Returns:
            Parsed design dictionary
        """
        # Try to extract JSON if present
        try:
            # Look for JSON in the response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Return raw response if JSON parsing fails
        return {
            "raw_response": response,
            "concept": "See raw response",
            "colors": ["#3498db", "#2ecc71", "#f39c12", "#e74c3c", "#ffffff"],
            "typography": "Sans-serif, bold",
            "layout": "center",
            "image_prompt": "professional modern abstract background"
        }
    
    def create_banner(
        self,
        user_prompt: str,
        text: str,
        width: int = 1024,
        height: int = 512,
        text_position: str = "center",
        font_size: int = 72,
        text_color: str = "#FFFFFF",
        use_controlnet: bool = True,
        output_name: str = "banner"
    ) -> str:
        """
        Create a complete banner based on user prompt.
        
        Args:
            user_prompt: Description of desired banner
            text: Text to display on banner
            width: Banner width
            height: Banner height
            text_position: Where to position text
            font_size: Font size for text
            text_color: Color for text
            use_controlnet: Whether to use ControlNet for generation
            output_name: Base name for output files
            
        Returns:
            Path to created banner
        """
        print("\n" + "="*60)
        print("BANNERLORD - AI BANNER GENERATION")
        print("="*60 + "\n")
        
        # Step 1: Get design recommendations from agent
        print("📋 Step 1: Consulting AI Design Agent...")
        self.initialize_agent()
        design_response = self.agent.design_banner(user_prompt)
        print("\n🎨 Design Recommendations:")
        print("-" * 60)
        print(design_response)
        print("-" * 60 + "\n")
        
        # Parse design
        design = self.parse_design_response(design_response)
        
        # Step 2: Generate background with ControlNet
        if use_controlnet:
            print("🖼️  Step 2: Generating background with ControlNet...")
            self.initialize_controlnet()
            
            # Create control image
            control_image = self.controlnet.create_control_image(
                width=width,
                height=height,
                text_position=text_position,
                layout_type="minimal"
            )
            
            # Save control image for reference
            control_path = self.output_dir / f"{output_name}_control.png"
            control_image.save(control_path)
            print(f"   Control image saved: {control_path}")
            
            # Generate background
            image_prompt = design.get('image_prompt', user_prompt)
            background = self.controlnet.generate_banner(
                prompt=image_prompt,
                control_image=control_image,
                num_inference_steps=30,
                guidance_scale=7.5
            )
            
            bg_path = self.output_dir / f"{output_name}_background.png"
            background.save(bg_path)
            print(f"   Background generated: {bg_path}")
        else:
            print("🖼️  Step 2: Creating simple background...")
            from PIL import Image, ImageDraw
            background = Image.new('RGB', (width, height), color='#2c3e50')
            draw = ImageDraw.Draw(background)
            # Add gradient effect
            for i in range(height):
                shade = int(44 + (i / height) * 30)
                color = f'#{shade:02x}{62 + i//20:02x}{80:02x}'
                draw.line([(0, i), (width, i)], fill=color)
            
            bg_path = self.output_dir / f"{output_name}_background.png"
            background.save(bg_path)
            print(f"   Background created: {bg_path}")
        
        # Step 3: Compose banner with text
        print("\n✍️  Step 3: Adding text to banner...")
        
        # Use colors from design if available
        if 'colors' in design and isinstance(design['colors'], list) and design['colors']:
            text_color = design['colors'][0] if isinstance(design['colors'][0], str) else text_color
        
        text_layers = [{
            'text': text,
            'position': None,  # Auto-center
            'font_size': font_size,
            'font_family': 'Sans',
            'color': text_color,
            'alignment': text_position,
            'stroke_width': 3,
            'stroke_color': '#000000',
            'shadow': True
        }]
        
        # Create composite
        final_banner = self.compositor.create_composite_banner(
            background=background,
            text_elements=text_layers
        )
        
        # Step 4: Export in multiple formats
        print("\n💾 Step 4: Exporting banner...")
        
        # Export as PNG
        png_path = self.output_dir / f"{output_name}.png"
        final_banner.save(png_path, "PNG")
        print(f"   PNG: {png_path}")
        
        # Export with metadata for editing
        metadata_base = self.output_dir / output_name
        bg_path, metadata_path = self.compositor.export_with_metadata(
            output_path=str(metadata_base),
            background=background,
            text_layers=text_layers
        )
        print(f"   Metadata: {metadata_path}")
        
        # Export as SVG
        svg_path = self.output_dir / f"{output_name}.svg"
        self.compositor.export_as_svg(
            output_path=str(svg_path),
            width=width,
            height=height,
            background_image_path=str(bg_path),
            text_layers=[{
                **layer,
                'x': width // 2,
                'y': height // 2
            } for layer in text_layers]
        )
        print(f"   SVG: {svg_path}")
        
        print("\n✅ Banner creation complete!")
        print(f"\n📁 All files saved to: {self.output_dir}/")
        print("\n💡 You can edit:")
        print(f"   - SVG file ({svg_path.name}) in Inkscape, Adobe Illustrator, etc.")
        print(f"   - PNG with metadata ({metadata_path.name}) for programmatic editing")
        print(f"   - Background image ({bg_path.name}) separately in any image editor")
        
        return str(png_path)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="BannerLord - AI-powered banner generation with ControlNet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a banner with default settings
  python bannerlord.py --prompt "modern tech startup" --text "INNOVATE"
  
  # Create a banner with custom positioning and colors
  python bannerlord.py --prompt "gaming tournament" --text "CHAMPION" \\
    --position left --color "#FFD700" --width 1920 --height 1080
  
  # Skip ControlNet for faster generation
  python bannerlord.py --prompt "minimalist design" --text "SIMPLE" --no-controlnet
        """
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        required=True,
        help='Description of the banner you want to create'
    )
    
    parser.add_argument(
        '--text',
        type=str,
        required=True,
        help='Text to display on the banner'
    )
    
    parser.add_argument(
        '--width',
        type=int,
        default=1024,
        help='Banner width in pixels (default: 1024)'
    )
    
    parser.add_argument(
        '--height',
        type=int,
        default=512,
        help='Banner height in pixels (default: 512)'
    )
    
    parser.add_argument(
        '--position',
        type=str,
        choices=['left', 'center', 'right', 'top', 'bottom'],
        default='center',
        help='Text position on banner (default: center)'
    )
    
    parser.add_argument(
        '--font-size',
        type=int,
        default=72,
        help='Font size in pixels (default: 72)'
    )
    
    parser.add_argument(
        '--color',
        type=str,
        default='#FFFFFF',
        help='Text color as hex code (default: #FFFFFF)'
    )
    
    parser.add_argument(
        '--no-controlnet',
        action='store_true',
        help='Skip ControlNet generation (faster but less precise)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='banner',
        help='Base name for output files (default: banner)'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='OpenAI API key (or set OPENAI_API_KEY env var)'
    )
    
    args = parser.parse_args()
    
    # Create BannerLord instance
    try:
        app = BannerLord(api_key=args.api_key)
        
        # Create banner
        output_path = app.create_banner(
            user_prompt=args.prompt,
            text=args.text,
            width=args.width,
            height=args.height,
            text_position=args.position,
            font_size=args.font_size,
            text_color=args.color,
            use_controlnet=not args.no_controlnet,
            output_name=args.output
        )
        
        print(f"\n🎉 Success! Banner saved to: {output_path}")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
