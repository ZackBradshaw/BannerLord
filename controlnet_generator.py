"""
ControlNet Integration for Banner Generation
Provides precise image generation with ControlNet guidance.
"""

import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from diffusers import UniPCMultistepScheduler
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from typing import Optional, Tuple, List
import os


class ControlNetBannerGenerator:
    """
    Generates banner images using Stable Diffusion with ControlNet for precise control.
    Supports various ControlNet modes for layout control.
    """
    
    def __init__(
        self,
        device: Optional[str] = None,
        controlnet_type: str = "canny",
        model_id: str = "runwayml/stable-diffusion-v1-5"
    ):
        """
        Initialize the ControlNet Banner Generator.
        
        Args:
            device: Device to run on ('cuda', 'mps', or 'cpu')
            controlnet_type: Type of ControlNet ('canny', 'depth', 'pose', 'scribble')
            model_id: Base Stable Diffusion model ID
        """
        self.device = device or self._get_device()
        self.controlnet_type = controlnet_type
        self.model_id = model_id
        self.pipeline = None
        
    def _get_device(self) -> str:
        """Automatically detect the best available device."""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        return "cpu"
    
    def load_model(self):
        """Load the ControlNet model and Stable Diffusion pipeline."""
        print(f"Loading ControlNet model ({self.controlnet_type}) on {self.device}...")
        
        # Map controlnet types to their model IDs
        controlnet_models = {
            "canny": "lllyasviel/sd-controlnet-canny",
            "depth": "lllyasviel/sd-controlnet-depth",
            "pose": "lllyasviel/sd-controlnet-openpose",
            "scribble": "lllyasviel/sd-controlnet-scribble",
        }
        
        controlnet_id = controlnet_models.get(self.controlnet_type, controlnet_models["canny"])
        
        # Load ControlNet
        controlnet = ControlNetModel.from_pretrained(
            controlnet_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )
        
        # Load Stable Diffusion pipeline with ControlNet
        self.pipeline = StableDiffusionControlNetPipeline.from_pretrained(
            self.model_id,
            controlnet=controlnet,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            safety_checker=None
        )
        
        # Optimize pipeline
        self.pipeline.scheduler = UniPCMultistepScheduler.from_config(
            self.pipeline.scheduler.config
        )
        self.pipeline = self.pipeline.to(self.device)
        
        # Enable memory optimizations
        if self.device == "cuda":
            self.pipeline.enable_model_cpu_offload()
        
        print("Model loaded successfully!")
    
    def create_control_image(
        self,
        width: int = 1024,
        height: int = 512,
        text_position: str = "center",
        layout_type: str = "minimal"
    ) -> Image.Image:
        """
        Create a control image for ControlNet to guide generation.
        
        Args:
            width: Banner width in pixels
            height: Banner height in pixels
            text_position: Position for text area ('left', 'center', 'right', 'top', 'bottom')
            layout_type: Layout style ('minimal', 'geometric', 'split')
            
        Returns:
            PIL Image to use as ControlNet control
        """
        # Create blank white image
        control_img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(control_img)
        
        # Define layout regions based on layout_type
        if layout_type == "minimal":
            # Simple edge detection style - just borders
            draw.rectangle([0, 0, width-1, height-1], outline='black', width=3)
            
        elif layout_type == "geometric":
            # Geometric shapes for structure
            draw.rectangle([0, 0, width-1, height-1], outline='black', width=3)
            # Add some geometric elements
            draw.line([width//3, 0, width//3, height], fill='black', width=2)
            draw.line([2*width//3, 0, 2*width//3, height], fill='black', width=2)
            
        elif layout_type == "split":
            # Split layout with distinct regions
            draw.rectangle([0, 0, width-1, height-1], outline='black', width=3)
            draw.line([width//2, 0, width//2, height], fill='black', width=4)
        
        # Mark text area based on position
        padding = 50
        if text_position == "center":
            text_box = [
                width//4, height//3,
                3*width//4, 2*height//3
            ]
        elif text_position == "left":
            text_box = [
                padding, height//4,
                width//2 - padding, 3*height//4
            ]
        elif text_position == "right":
            text_box = [
                width//2 + padding, height//4,
                width - padding, 3*height//4
            ]
        elif text_position == "top":
            text_box = [
                padding, padding,
                width - padding, height//3
            ]
        elif text_position == "bottom":
            text_box = [
                padding, 2*height//3,
                width - padding, height - padding
            ]
        else:
            text_box = [width//4, height//3, 3*width//4, 2*height//3]
        
        # Draw text area box
        draw.rectangle(text_box, outline='black', width=2)
        
        return control_img
    
    def generate_banner(
        self,
        prompt: str,
        control_image: Image.Image,
        negative_prompt: str = "ugly, blurry, low quality, distorted, text, watermark",
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        controlnet_conditioning_scale: float = 1.0,
        seed: Optional[int] = None
    ) -> Image.Image:
        """
        Generate a banner image using ControlNet.
        
        Args:
            prompt: Text prompt describing the desired banner
            control_image: Control image for ControlNet guidance
            negative_prompt: Things to avoid in generation
            num_inference_steps: Number of denoising steps
            guidance_scale: How closely to follow the prompt
            controlnet_conditioning_scale: Strength of ControlNet influence
            seed: Random seed for reproducibility
            
        Returns:
            Generated banner image
        """
        if self.pipeline is None:
            self.load_model()
        
        # Set seed for reproducibility
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        else:
            generator = None
        
        # Prepare control image (convert to RGB if needed)
        if control_image.mode != 'RGB':
            control_image = control_image.convert('RGB')
        
        # Generate image
        print("Generating banner with ControlNet...")
        output = self.pipeline(
            prompt=prompt,
            image=control_image,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            controlnet_conditioning_scale=controlnet_conditioning_scale,
            generator=generator
        )
        
        return output.images[0]
