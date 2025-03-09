from manim_engine.constants import *
from util.exceptions import SanimParseError
from util.positioning import ElementPosition

# Animation timing constants
DEFAULT_ANIMATION_RUNTIME = 0.8
FLUSH_ANIMATION_RUNTIME = 0.8
ELEMENT_DISPLAY_WAIT_TIME = 0.2
FLUSH_DISPLAY_WAIT_TIME = 0.2

class AnimationBuffer:
    """
    Manages a buffer of animations to be played together.
    """
    
    def __init__(self, scene):
        """
        Initialize a new animation buffer.
        
        Args:
            scene: The scene to play animations in
        """
        self.scene = scene
        self.buffer = []
        self.time_stamps = []
    
    def add_element(self, element):
        """
        Add an element to the animation buffer.
        
        If the element should wait for input, the buffer is flushed before
        adding the element.
        
        Args:
            element: The element to add
        """
        if element.wait_for_input:
            self.flush()
        self.buffer.append(element)
    
    def flush(self):
        """
        Play all animations in the buffer and clear it.
        """
        if not self.buffer:
            return
        
        if len(self.buffer) == 1:
            # Play a single element
            element = self.buffer[0]
            element.individual_play(self.scene)
        else:
            # Play multiple elements together
            actions = []
            for element in self.buffer:
                actions.extend(element.get_play_actions())
            self.scene.play(*actions, run_time=DEFAULT_ANIMATION_RUNTIME)
        
        # Clear the buffer
        self.buffer.clear()
        
        # Record timestamp for the web player
        self.time_stamps.append(self.scene.current_scene_time + ELEMENT_DISPLAY_WAIT_TIME / 2)
        self.scene.wait(ELEMENT_DISPLAY_WAIT_TIME)
    
    def get_time_stamps(self):
        """
        Get the timestamps of all animations.
        
        Returns:
            List of timestamps in seconds
        """
        return self.time_stamps


class PresentationRenderer:
    """
    Renders a presentation from InputLines.
    """
    
    def __init__(self, scene):
        """
        Initialize a new presentation renderer.
        
        Args:
            scene: The scene to render in
        """
        self.scene = scene
        self.position = ElementPosition()
        self.animation_buffer = AnimationBuffer(scene)
    
    def render_line(self, line):
        """
        Render a line of content.
        
        Args:
            line: The line to render
        """
        elements = line.output_elements
        
        if len(elements) == 1:
            # Single element - left aligned
            element = elements[0]
            element.position_left_aligned(self.position.get_current_position())
            self.position.update_after_element(element)
            self.animation_buffer.add_element(element)
        else:
            # Multiple elements - distribute horizontally
            num_elements = len(elements)
            for i, element in enumerate(elements, 1):
                # Create a position for this element
                position = self.position.get_current_position()
                position.to_edge(LEFT, buff=0)
                position.shift(RIGHT * (position.get_edge_center(LEFT) - position.get_center()))
                position.shift(i * 2 * FRAME_X_RADIUS * RIGHT / (num_elements + 1))
                
                # Position and animate the element
                element.position_center_at(position)
                self.animation_buffer.add_element(element)
            
            # Update position to the bottom of the last element
            self.position.update_after_element(elements[-1])
    
    def get_shift_actions(self, line, position):
        """
        Get animations to shift elements in a line to a new position.
        
        Args:
            line: The line to shift
            position: The new position
            
        Returns:
            List of animations to play
        """
        elements = line.output_elements
        result = []
        
        if not elements:
            return []
        
        if len(elements) == 1:
            # Single element - left aligned
            element = elements[0]
            result.extend(element.get_shift_left_aligned_actions(position))
            
            # Update position
            element_copy = element.copy()
            element_copy.position_left_aligned(position)
            position.move_to(element_copy.get_bottom_position().get_edge_center(DOWN))
        else:
            # Multiple elements - distribute horizontally
            num_elements = len(elements)
            for i, element in enumerate(elements, 1):
                # Create a position for this element
                elem_position = position.copy()
                elem_position.to_edge(LEFT, buff=0)
                elem_position.shift(RIGHT * (elem_position.get_edge_center(LEFT) - elem_position.get_center()))
                elem_position.shift(i * 2 * FRAME_X_RADIUS * RIGHT / (num_elements + 1))
                
                # Get shift actions
                result.extend(element.get_shift_center_at_actions(elem_position))
            
            # Update position
            element_copy = elements[-1].copy()
            element_copy.position_center_at(elem_position)
            position.move_to(element_copy.get_bottom_position().get_edge_center(DOWN))
        
        # Add some vertical spacing
        position.shift(DOWN * 0.5)
        return result
    
    def render_presentation(self, lines):
        """
        Render a complete presentation.
        
        Args:
            lines: List of input lines to render
            
        Returns:
            List of timestamps for the web player
        """
        flush_index = 0  # Starting line to flush when using FLUSH
        
        # Initial wait
        self.scene.wait(ELEMENT_DISPLAY_WAIT_TIME)
        self.animation_buffer.time_stamps = [ELEMENT_DISPLAY_WAIT_TIME / 2]  # Initial timestamp
        
        for line in lines:
            if line.is_content_line():
                # Render content line
                self.render_line(line)
            else:
                # Process command line
                elements = line.input_elements
                if not elements:
                    raise SanimParseError("Empty line")
                if len(elements) > 1:
                    raise SanimParseError("More than one command in a line")
                
                element = elements[0]
                if element.keyword == 'FLUSH':
                    # Flush command
                    self.animation_buffer.flush()  # Flush any leftover animations
                    
                    # Parse flush line number (if empty, use the current line)
                    try:
                        if element.content.strip():
                            flush_line_num = int(element.content)
                        else:
                            flush_line_num = line.line_num
                    except ValueError:
                        raise SanimParseError(f"Invalid flush line number: {element.content}")
                    
                    current_line_num = line.line_num
                    if flush_line_num > current_line_num:
                        raise SanimParseError("Cannot flush beyond the current line")
                    
                    # Collect fade out animations for lines to be flushed
                    fade_out_actions = []
                    while flush_index < len(lines) and lines[flush_index].line_num < flush_line_num:
                        if lines[flush_index].is_content_line():
                            fade_out_actions.extend(lines[flush_index].get_fade_out_actions())
                        flush_index += 1
                    
                    # Reset position to top
                    self.position.reset_to_top()
                    
                    # Collect shift animations for lines to be kept
                    shift_actions = []
                    i = flush_index
                    current_position = self.position.get_current_position()
                    while i < len(lines) and lines[i].line_num < current_line_num:
                        shift_actions.extend(self.get_shift_actions(
                            lines[i], current_position))
                        i += 1
                    
                    # Play flush animations
                    if fade_out_actions or shift_actions:
                        self.scene.play(
                            *fade_out_actions, *shift_actions, 
                            run_time=FLUSH_ANIMATION_RUNTIME
                        )
                    
                    # Record timestamp and wait
                    self.animation_buffer.time_stamps.append(
                        self.scene.current_scene_time + FLUSH_DISPLAY_WAIT_TIME / 2
                    )
                    self.scene.wait(FLUSH_DISPLAY_WAIT_TIME)
                else:
                    raise SanimParseError(f"Unknown command: {element.keyword}")
        
        # Flush any remaining animations
        self.animation_buffer.flush()
        
        return self.animation_buffer.get_time_stamps()

