"""
Banner Compositor - Creates final banners with editable text layers
Exports to multiple formats including SVG and layered formats
"""

from PIL import Image, ImageDraw, ImageFont, ImageColor
import svgwrite
from typing import Tuple, Optional, List, Dict
import json
import os


class BannerCompositor:
    """
    Composes final banners by overlaying text on generated backgrounds.
    Supports multiple export formats for editability.
    """
    
    def __init__(self):
        """Initialize the Banner Compositor."""
        self.default_font_size = 72
        self.default_font = None
        
    def _get_font(self, font_size: int, font_family: str = "arial") -> ImageFont.FreeTypeFont:
        """
        Get a font object, falling back to defaults if specified font not available.
        
        Args:
            font_size: Size of the font
            font_family: Font family name
            
        Returns:
            Font object
        """
        # Try to load specified font
        font_paths = [
            f"/usr/share/fonts/truetype/dejavu/DejaVu{font_family.title()}.ttf",
            f"/usr/share/fonts/truetype/liberation/Liberation{font_family.title()}.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, font_size)
                except:
                    continue
        
        # Fallback to default
        return ImageFont.load_default()
    
    def add_text_to_banner(
        self,
        background: Image.Image,
        text: str,
        position: Tuple[int, int] = None,
        font_size: int = 72,
        font_family: str = "Sans",
        color: str = "#FFFFFF",
        alignment: str = "center",
        stroke_width: int = 2,
        stroke_color: str = "#000000",
        shadow: bool = True
    ) -> Image.Image:
        """
        Add text overlay to banner background.
        
        Args:
            background: Background image
            text: Text to add
            position: (x, y) position. If None, centers text
            font_size: Font size in pixels
            font_family: Font family name
            color: Text color (hex or name)
            alignment: Text alignment ('left', 'center', 'right')
            stroke_width: Width of text outline
            stroke_color: Color of text outline
            shadow: Whether to add shadow effect
            
        Returns:
            Image with text overlay
        """
        # Create a copy to avoid modifying original
        img = background.copy()
        draw = ImageDraw.Draw(img)
        
        # Get font
        font = self._get_font(font_size, font_family)
        
        # Calculate text position if not specified
        if position is None:
            # Get text bounding box
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Center the text
            x = (img.width - text_width) // 2
            y = (img.height - text_height) // 2
            position = (x, y)
        
        # Add shadow if requested
        if shadow:
            shadow_offset = 3
            shadow_pos = (position[0] + shadow_offset, position[1] + shadow_offset)
            draw.text(
                shadow_pos,
                text,
                font=font,
                fill="#00000080",  # Semi-transparent black
                stroke_width=stroke_width,
                stroke_fill="#00000080"
            )
        
        # Draw main text with stroke
        draw.text(
            position,
            text,
            font=font,
            fill=color,
            stroke_width=stroke_width,
            stroke_fill=stroke_color
        )
        
        return img
    
    def export_as_svg(
        self,
        output_path: str,
        width: int,
        height: int,
        background_image_path: str,
        text_layers: List[Dict]
    ):
        """
        Export banner as SVG with editable text layers.
        
        Args:
            output_path: Path to save SVG file
            width: Banner width
            height: Banner height
            background_image_path: Path to background image
            text_layers: List of text layer definitions
                Each dict should have: text, x, y, font_size, font_family, color
        """
        dwg = svgwrite.Drawing(output_path, size=(width, height))
        
        # Add background image
        dwg.add(dwg.image(
            href=background_image_path,
            insert=(0, 0),
            size=(width, height)
        ))
        
        # Add text layers
        for layer in text_layers:
            text_element = dwg.text(
                layer.get('text', ''),
                insert=(layer.get('x', width//2), layer.get('y', height//2)),
                font_size=layer.get('font_size', 72),
                font_family=layer.get('font_family', 'Arial'),
                fill=layer.get('color', '#FFFFFF'),
                text_anchor='middle',
                stroke=layer.get('stroke_color', '#000000'),
                stroke_width=layer.get('stroke_width', 2)
            )
            dwg.add(text_element)
        
        dwg.save()
        print(f"SVG exported to: {output_path}")
    
    def export_with_metadata(
        self,
        output_path: str,
        background: Image.Image,
        text_layers: List[Dict]
    ):
        """
        Export banner with metadata JSON for later editing.
        
        Args:
            output_path: Base path for output (without extension)
            background: Background image
            text_layers: List of text layer definitions
        """
        # Save background
        bg_path = f"{output_path}_background.png"
        background.save(bg_path, "PNG")
        
        # Save metadata
        metadata = {
            "width": background.width,
            "height": background.height,
            "background": bg_path,
            "text_layers": text_layers
        }
        
        metadata_path = f"{output_path}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, indent=2, fp=f)
        
        print(f"Banner exported with metadata:")
        print(f"  Background: {bg_path}")
        print(f"  Metadata: {metadata_path}")
        
        return bg_path, metadata_path
    
    def create_composite_banner(
        self,
        background: Image.Image,
        text_elements: List[Dict],
        output_path: str = None
    ) -> Image.Image:
        """
        Create a complete banner with multiple text elements.
        
        Args:
            background: Background image
            text_elements: List of text element specifications
            output_path: Optional path to save the result
            
        Returns:
            Composite banner image
        """
        result = background.copy()
        
        for element in text_elements:
            result = self.add_text_to_banner(
                result,
                text=element.get('text', ''),
                position=element.get('position'),
                font_size=element.get('font_size', 72),
                font_family=element.get('font_family', 'Sans'),
                color=element.get('color', '#FFFFFF'),
                alignment=element.get('alignment', 'center'),
                stroke_width=element.get('stroke_width', 2),
                stroke_color=element.get('stroke_color', '#000000'),
                shadow=element.get('shadow', True)
            )
        
        if output_path:
            result.save(output_path, "PNG")
            print(f"Banner saved to: {output_path}")
        
        return result
    
    def load_from_metadata(self, metadata_path: str) -> Tuple[Image.Image, List[Dict]]:
        """
        Load banner configuration from metadata file.
        
        Args:
            metadata_path: Path to metadata JSON file
            
        Returns:
            Tuple of (background_image, text_layers)
        """
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        background = Image.open(metadata['background'])
        text_layers = metadata['text_layers']
        
        return background, text_layers
