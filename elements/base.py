"""
Base classes for Sanim elements.
"""

from manim_engine.big_ol_pile_of_manim_imports import *

class OutputElement:
    """
    Base class for all output elements.
    """
    
    def __init__(self, input_elem):
        """
        Initialize a new OutputElement.
        
        Args:
            input_elem: The input element this output element is based on
        """
        self.input_elem = input_elem
        self.wait_for_input = input_elem.should_wait_for_input()
    
    def individual_play(self, scene):
        """
        Animate the element in the scene.
        
        Args:
            scene: The scene to animate in
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_play_actions(self):
        """
        Get the animations to play this element.
        
        Returns:
            List of animations to play
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def individual_play_duration(self):
        """
        Get the duration of this element's animation.
        
        Returns:
            Animation duration in seconds
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def position_center_at(self, position):
        """
        Position this element centered at the given position.
        
        Args:
            position: The position to center at
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def position_left_aligned(self, position):
        """
        Position this element left-aligned at the given position.
        
        Args:
            position: The position to align to
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_shift_center_at_actions(self, position):
        """
        Get animations to shift this element to be centered at the given position.
        
        Args:
            position: The position to center at
            
        Returns:
            List of animations to play
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_shift_left_aligned_actions(self, position):
        """
        Get animations to shift this element to be left-aligned at the given position.
        
        Args:
            position: The position to align to
            
        Returns:
            List of animations to play
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_bottom_position(self):
        """
        Get the position at the bottom of this element.
        
        Returns:
            Mobject representing the bottom position
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_fade_out_actions(self):
        """
        Get animations to fade out this element.
        
        Returns:
            List of animations to play
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def copy(self):
        """
        Create a copy of this element.
        
        Returns:
            A new instance of this element
        """
        raise NotImplementedError("Subclasses must implement this method")
