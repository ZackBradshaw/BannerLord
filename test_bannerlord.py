"""
Simple tests for BannerLord components
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from PIL import Image
import json
import os
import tempfile
from pathlib import Path


class TestBannerCompositor(unittest.TestCase):
    """Test the BannerCompositor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        from banner_compositor import BannerCompositor
        self.compositor = BannerCompositor()
        self.test_img = Image.new('RGB', (800, 400), color='#3498db')
    
    def test_add_text_to_banner(self):
        """Test adding text to a banner."""
        result = self.compositor.add_text_to_banner(
            background=self.test_img,
            text="TEST",
            font_size=48,
            color="#FFFFFF"
        )
        
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (800, 400))
    
    def test_export_with_metadata(self):
        """Test exporting banner with metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_banner")
            
            text_layers = [{
                'text': 'TEST',
                'position': (400, 200),
                'font_size': 48,
                'color': '#FFFFFF'
            }]
            
            bg_path, metadata_path = self.compositor.export_with_metadata(
                output_path=output_path,
                background=self.test_img,
                text_layers=text_layers
            )
            
            self.assertTrue(os.path.exists(bg_path))
            self.assertTrue(os.path.exists(metadata_path))
            
            # Verify metadata content
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            self.assertEqual(metadata['width'], 800)
            self.assertEqual(metadata['height'], 400)
            self.assertEqual(len(metadata['text_layers']), 1)
    
    def test_create_composite_banner(self):
        """Test creating a composite banner."""
        text_elements = [
            {
                'text': 'TITLE',
                'font_size': 72,
                'color': '#FFFFFF'
            },
            {
                'text': 'Subtitle',
                'font_size': 36,
                'color': '#ECF0F1'
            }
        ]
        
        result = self.compositor.create_composite_banner(
            background=self.test_img,
            text_elements=text_elements
        )
        
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (800, 400))


class TestBannerAgent(unittest.TestCase):
    """Test the BannerDesignAgent class."""
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_agent_initialization(self):
        """Test agent can be initialized with API key."""
        from banner_agent import BannerDesignAgent
        
        agent = BannerDesignAgent(api_key='test-key')
        self.assertIsNotNone(agent.agent)
        self.assertEqual(agent.api_key, 'test-key')
    
    def test_agent_requires_api_key(self):
        """Test agent raises error without API key."""
        from banner_agent import BannerDesignAgent
        
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                BannerDesignAgent()


class TestControlNetGenerator(unittest.TestCase):
    """Test the ControlNetBannerGenerator class."""
    
    def test_create_control_image(self):
        """Test creating control images."""
        from controlnet_generator import ControlNetBannerGenerator
        
        generator = ControlNetBannerGenerator()
        
        # Test different layouts
        for layout in ['minimal', 'geometric', 'split']:
            control = generator.create_control_image(
                width=1024,
                height=512,
                text_position='center',
                layout_type=layout
            )
            
            self.assertIsInstance(control, Image.Image)
            self.assertEqual(control.size, (1024, 512))
    
    def test_device_detection(self):
        """Test automatic device detection."""
        from controlnet_generator import ControlNetBannerGenerator
        
        generator = ControlNetBannerGenerator()
        device = generator._get_device()
        
        self.assertIn(device, ['cuda', 'mps', 'cpu'])


class TestBannerLordApp(unittest.TestCase):
    """Test the main BannerLord application."""
    
    def test_initialization(self):
        """Test BannerLord app initialization."""
        from bannerlord import BannerLord
        
        app = BannerLord(api_key='test-key')
        
        self.assertIsNone(app.agent)  # Not initialized until needed
        self.assertIsNone(app.controlnet)  # Not initialized until needed
        self.assertIsNotNone(app.compositor)
        self.assertTrue(app.output_dir.exists())
    
    def test_parse_design_response(self):
        """Test parsing design responses."""
        from bannerlord import BannerLord
        
        app = BannerLord(api_key='test-key')
        
        # Test JSON response
        json_response = '''
        {
            "concept": "Modern tech",
            "colors": ["#3498db", "#2ecc71"],
            "typography": "Sans-serif",
            "layout": "center",
            "image_prompt": "tech background"
        }
        '''
        
        result = app.parse_design_response(json_response)
        self.assertEqual(result['concept'], 'Modern tech')
        self.assertEqual(len(result['colors']), 2)
        
        # Test non-JSON response
        text_response = "This is a plain text response"
        result = app.parse_design_response(text_response)
        self.assertIn('raw_response', result)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestBannerCompositor))
    suite.addTests(loader.loadTestsFromTestCase(TestBannerAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestControlNetGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestBannerLordApp))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
