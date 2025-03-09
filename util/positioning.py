from manim_engine.big_ol_pile_of_manim_imports import TextMobject, TOP, LEFT, MED_SMALL_BUFF, DOWN

class ElementPosition:
    """
    Manages the position of elements in the presentation.
    """
    
    def __init__(self):
        """Initialize a new position tracker at the top-left corner."""
        self.position = self._get_top_left_position()
    
    def _get_top_left_position(self):
        """Create a mobject positioned at the top-left corner of the screen."""
        position = TextMobject("aux")  # Auxiliary object used only for positioning
        position.to_corner(TOP+LEFT, buff=MED_SMALL_BUFF)
        return position
    
    def get_current_position(self):
        """Get the current position mobject."""
        return self.position
    
    def reset_to_top(self):
        """Reset the position to the top-left corner."""
        self.position = self._get_top_left_position()
    
    def update_after_element(self, element):
        """
        Update position after adding an element.
        
        Args:
            element: The element that was just added
        """
        # Move to the bottom of the element
        self.position.move_to(element.get_bottom_position().get_edge_center(DOWN))
        # Add some vertical spacing
        self.position.shift(DOWN * 0.5)
