"""
Media-based elements for Sanim.
"""

from manim_engine.big_ol_pile_of_manim_imports import *
from .base import OutputElement
from util.exceptions import SanimParseError, SanimRenderError

# Constants
BACKGROUND_COLOR = "#e6f3ff"

class ImageElement(OutputElement):
    """Element representing an image in the presentation."""
    
    def __init__(self, input_elem):
        """
        Initialize a new ImageElement.
        
        Args:
            input_elem: The input element this output element is based on
            
        Raises:
            SanimParseError: If the image path is empty
            SanimRenderError: If the image can't be loaded
        """
        super().__init__(input_elem)
        
        # Split content into path and optional size multiplier
        content_parts = input_elem.content.strip().split()
        if not content_parts:
            raise SanimParseError('Empty image path')
        
        image_path = content_parts[0]
        # Default size multiplier is 1.0
        self.size_multiplier = 1.0
        
        # If size multiplier is provided, parse it
        if len(content_parts) > 1:
            try:
                self.size_multiplier = float(content_parts[1])
            except ValueError:
                raise SanimParseError('Invalid size multiplier - must be a number')
        
        try:
            # Load the image and scale it
            self.image = ImageMobject(image_path)
            self.image.scale(self.size_multiplier)
            
            # Runtime based on a constant value
            self.run_time = 0.8
        except Exception as e:
            raise SanimRenderError(f"Failed to load image {image_path}: {str(e)}")
    
    def copy(self):
        """Create a copy of this element."""
        return ImageElement(self.input_elem)
    
    def individual_play(self, scene):
        """Animate the image in the scene."""
        scene.play(FadeIn(self.image), run_time=self.run_time)
    
    def get_play_actions(self):
        """Get the animations to play this image."""
        return [FadeIn(self.image)]
    
    def individual_play_duration(self):
        """Get the duration of this image's animation."""
        return self.run_time
    
    def position_center_at(self, position):
        """Position this image centered at the given position."""
        self.image.move_to(position)
    
    def position_left_aligned(self, position):
        """
        Position this image at the given position, aligned with the top.
        
        This ensures the image appears below previous content, not overlapping.
        """
        # First align the top of the image with the current position
        self.image.move_to(position)
        
        # Align the top edge of the image with the position
        current_top = self.image.get_top()
        target_top = position.get_center() + UP * 0.1  # Small buffer
        self.image.shift(target_top - current_top)
        
        # Center horizontally in the frame
        center_x = ORIGIN[0]  # X-coordinate of the center of the screen
        current_x = self.image.get_center()[0]  # Current X-coordinate of the image
        self.image.shift(RIGHT * (center_x - current_x))
    
    def get_shift_center_at_actions(self, position):
        """Get animations to shift this image to be centered at the given position."""
        return [ApplyMethod(self.image.move_to, position)]
    
    def get_shift_left_aligned_actions(self, position):
        """Get animations to shift this image to be left-aligned at the given position."""
        # Create a target position object for positioning
        temp_image = self.image.copy()  # Used only for positioning
        
        # First align the top with current position (to avoid overlap)
        temp_image.move_to(position)
        current_top = temp_image.get_top()
        target_top = position.get_center() + UP * 0.1  # Small buffer
        temp_image.shift(target_top - current_top)
        
        # Center horizontally in the frame
        center_x = ORIGIN[0]  # X-coordinate of the center of the screen
        current_x = temp_image.get_center()[0]  # Current X-coordinate
        temp_image.shift(RIGHT * (center_x - current_x))
        
        return [ApplyMethod(self.image.move_to, temp_image)]
    
    def get_bottom_position(self):
        """Get the position at the bottom of this image."""
        return self.image
    
    def get_fade_out_actions(self):
        """Get animations to fade out this image."""
        return [FadeOut(self.image)]
