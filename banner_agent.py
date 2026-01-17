"""
BannerLord - AI Banner Generation Tool
This module contains the Swarms agent for intelligent banner design.
"""

from swarms import Agent
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class BannerDesignAgent:
    """
    Swarms-based AI agent for intelligent banner design recommendations.
    Analyzes user prompts and provides design guidance for banner creation.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Banner Design Agent.
        
        Args:
            api_key: OpenAI API key. If None, reads from environment.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Define the system prompt for banner design expertise
        system_prompt = """You are an expert banner designer and creative director with deep knowledge of:
- Visual design principles (hierarchy, balance, contrast, alignment)
- Color theory and harmonious color schemes
- Typography and font pairing
- Layout and composition
- Brand design and marketing effectiveness

When a user provides a banner request, analyze their needs and provide:
1. **Design Concept**: Overall visual direction and mood
2. **Color Scheme**: 3-5 specific colors with hex codes that work together
3. **Typography**: Font style recommendations (serif/sans-serif, weight, size hierarchy)
4. **Layout**: Text positioning and alignment suggestions
5. **Image Generation Prompt**: A detailed, optimized prompt for generating the banner background/imagery using AI image generation with ControlNet

Be specific, creative, and practical. Focus on designs that are visually striking and achieve the user's goals.
Format your response as structured JSON with these keys: concept, colors, typography, layout, image_prompt, controlnet_hints."""
        
        # Initialize the Swarms Agent
        self.agent = Agent(
            agent_name="BannerDesignExpert",
            system_prompt=system_prompt,
            model_name="gpt-4",
            openai_api_key=self.api_key,
            max_loops=1,
            autosave=False,
            verbose=True,
            temperature=0.7,
            max_tokens=2000,
        )
    
    def design_banner(self, user_prompt: str) -> str:
        """
        Generate banner design recommendations based on user prompt.
        
        Args:
            user_prompt: User's banner requirements and text content
            
        Returns:
            Design recommendations as structured text
        """
        enhanced_prompt = f"""Design a banner with the following requirements:

{user_prompt}

Provide a complete design specification including concept, colors (with hex codes), 
typography recommendations, layout/alignment suggestions, and a detailed image generation 
prompt optimized for AI image generation with ControlNet."""
        
        try:
            response = self.agent.run(enhanced_prompt)
            return response
        except Exception as e:
            return f"Error generating design: {str(e)}"
    
    def refine_design(self, original_prompt: str, feedback: str) -> str:
        """
        Refine a design based on user feedback.
        
        Args:
            original_prompt: Original design request
            feedback: User's feedback or modification requests
            
        Returns:
            Refined design recommendations
        """
        refinement_prompt = f"""Original banner request: {original_prompt}

User feedback/modification request: {feedback}

Please refine the banner design based on this feedback while maintaining design principles."""
        
        try:
            response = self.agent.run(refinement_prompt)
            return response
        except Exception as e:
            return f"Error refining design: {str(e)}"
