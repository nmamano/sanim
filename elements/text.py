"""
Text-based elements for Sanim.
"""

from manim_engine.big_ol_pile_of_manim_imports import *
from .base import OutputElement
from animations.custom_animations import CustomWrite
from util.exceptions import SanimParseError

# Constants
DEFINITION_COLOR = "#991f00"
BACKGROUND_COLOR = "#e6f3ff"

class TitleElement(OutputElement):
    """Element representing a title in the presentation."""
    
    def __init__(self, input_elem):
        """
        Initialize a new TitleElement.
        
        Args:
            input_elem: The input element this output element is based on
            
        Raises:
            SanimParseError: If the title is empty
        """
        super().__init__(input_elem)
        content = input_elem.content
        if not content:
            raise SanimParseError('Empty title')
        
        # Calculate runtime based on content length
        self.run_time = 1.1 + len(content) / 200
        
        # Create the title mobject
        self.text = Title(
            content, 
            scale_factor=1.3, 
            color=BLACK, 
            background_stroke_color=BACKGROUND_COLOR
        )
    
    def copy(self):
        """Create a copy of this element."""
        return TitleElement(self.input_elem)
    
    def individual_play(self, scene):
        """Animate the title in the scene."""
        scene.play(CustomWrite(self.text), run_time=self.run_time)
    
    def get_play_actions(self):
        """Get the animations to play this title."""
        return [CustomWrite(self.text)]
    
    def individual_play_duration(self):
        """Get the duration of this title's animation."""
        return self.run_time
    
    def position_center_at(self, position):
        """Position this title centered at the given position."""
        self.text.move_to(position)
    
    def position_left_aligned(self, position):
        """Position this title at the top of the screen."""
        self.text.center()
        self.text.to_edge(UP)
    
    def get_shift_center_at_actions(self, position):
        """Get animations to shift this title to be centered at the given position."""
        return [ApplyMethod(self.text.move_to, position)]
    
    def get_shift_left_aligned_actions(self, position):
        """Get animations to shift this title to be left-aligned at the given position."""
        # Create a temporary position
        pos_title = TextMobject("aux")
        pos_title.center()
        pos_title.to_edge(UP)
        return [ApplyMethod(self.text.move_to, pos_title)]
    
    def get_bottom_position(self):
        """Get the position at the bottom of this title."""
        return self.text
    
    def get_fade_out_actions(self):
        """Get animations to fade out this title."""
        return [FadeOut(self.text)]


class PlainTextElement(OutputElement):
    """Element representing plain text in the presentation."""
    
    def __init__(self, input_elem):
        """
        Initialize a new PlainTextElement.
        
        Args:
            input_elem: The input element this output element is based on
        """
        super().__init__(input_elem)
        content = input_elem.content
        
        if not content:
            # Empty text - create an invisible placeholder
            self.text = TextMobject(
                "aux",  # This is never displayed but used for positioning
                color=BLACK,
                background_stroke_color=BACKGROUND_COLOR
            )
            self.run_time = 0
            self.is_empty = True
        else:
            # Regular text
            self.text = TextMobject(
                content, 
                color=BLACK, 
                background_stroke_color=BACKGROUND_COLOR
            )
            self.run_time = 0.6 + len(content) / 150
            self.is_empty = False
    
    def copy(self):
        """Create a copy of this element."""
        return PlainTextElement(self.input_elem)
    
    def individual_play(self, scene):
        """Animate the text in the scene."""
        if not self.is_empty:
            scene.play(CustomWrite(self.text), run_time=self.run_time)
    
    def get_play_actions(self):
        """Get the animations to play this text."""
        if self.is_empty:
            return []
        return [CustomWrite(self.text)]
    
    def individual_play_duration(self):
        """Get the duration of this text's animation."""
        return self.run_time
    
    def position_center_at(self, position):
        """Position this text centered at the given position."""
        self.text.move_to(position)
    
    def position_left_aligned(self, position):
        """Position this text left-aligned at the given position."""
        self.text.move_to(position)
        self.text.to_edge(LEFT)
    
    def get_shift_center_at_actions(self, position):
        """Get animations to shift this text to be centered at the given position."""
        if self.is_empty:
            return []
        return [ApplyMethod(self.text.move_to, position)]
    
    def get_shift_left_aligned_actions(self, position):
        """Get animations to shift this text to be left-aligned at the given position."""
        if self.is_empty:
            return []
        
        # Create a temporary mobject for positioning
        pos_text = TextMobject("aux")
        pos_text.move_to(position)
        pos_text.to_edge(LEFT)
        
        return [ApplyMethod(self.text.move_to, pos_text)]
    
    def get_bottom_position(self):
        """Get the position at the bottom of this text."""
        return self.text
    
    def get_fade_out_actions(self):
        """Get animations to fade out this text."""
        if self.is_empty:
            return []
        return [FadeOut(self.text)]


class BulletElement(OutputElement):
    """Element representing a bullet point in the presentation."""
    
    def __init__(self, input_elem):
        """
        Initialize a new BulletElement.
        
        Args:
            input_elem: The input element this output element is based on
            
        Raises:
            SanimParseError: If the bullet content is empty
        """
        super().__init__(input_elem)
        content = input_elem.content
        if not content:
            raise SanimParseError("Empty bullet item")
        
        # Create the bullet mobject
        self.text = BulletedItem(
            content, 
            color=BLACK, 
            background_stroke_color=BACKGROUND_COLOR
        )
        self.run_time = 0.6 + len(content) / 150
    
    def copy(self):
        """Create a copy of this element."""
        return BulletElement(self.input_elem)
    
    def individual_play(self, scene):
        """Animate the bullet in the scene."""
        scene.play(CustomWrite(self.text), run_time=self.run_time)
    
    def get_play_actions(self):
        """Get the animations to play this bullet."""
        return [CustomWrite(self.text)]
    
    def individual_play_duration(self):
        """Get the duration of this bullet's animation."""
        return self.run_time
    
    def position_center_at(self, position):
        """Position this bullet centered at the given position."""
        self.text.move_to(position)
    
    def position_left_aligned(self, position):
        """Position this bullet left-aligned at the given position."""
        self.text.move_to(position)
        self.text.to_edge(LEFT)
    
    def get_shift_center_at_actions(self, position):
        """Get animations to shift this bullet to be centered at the given position."""
        return [ApplyMethod(self.text.move_to, position)]
    
    def get_shift_left_aligned_actions(self, position):
        """Get animations to shift this bullet to be left-aligned at the given position."""
        # Create a temporary mobject for positioning
        pos_text = BulletedItem(self.input_elem.content)
        pos_text.move_to(position)
        pos_text.to_edge(LEFT)
        
        return [ApplyMethod(self.text.move_to, pos_text)]
    
    def get_bottom_position(self):
        """Get the position at the bottom of this bullet."""
        return self.text
    
    def get_fade_out_actions(self):
        """Get animations to fade out this bullet."""
        return [FadeOut(self.text)]


class DefinitionElement(OutputElement):
    """Element representing a definition (term and explanation) in the presentation."""
    
    def __init__(self, input_elem):
        """
        Initialize a new DefinitionElement.
        
        Args:
            input_elem: The input element this output element is based on
            
        Raises:
            SanimParseError: If the definition syntax is invalid
        """
        super().__init__(input_elem)
        content = input_elem.content.lstrip()
        
        # Parse term and definition
        if not content or content[0] != '"':
            raise SanimParseError('Invalid use of DEF. Syntax: DEF "term" definition')
        
        content = content[1:]
        if '"' not in content:
            raise SanimParseError('Invalid use of DEF. Syntax: DEF "term" definition')
        
        # Extract term and definition text
        self.term_text = content[:content.find('"')]
        self.definition_text = content[content.find('"')+1:].lstrip()
        
        if not self.term_text:
            raise SanimParseError('Empty term in DEF')
        if not self.definition_text:
            raise SanimParseError('Empty definition in DEF')
        
        # Create term and definition mobjects
        self.term = TextMobject(
            '\\textbf{' + self.term_text + '}:',
            background_stroke_color=BACKGROUND_COLOR, 
            alignment=""
        )
        self.term.set_color(DEFINITION_COLOR)
        
        self.definition = TextMobject(
            self.definition_text,
            color=BLACK, 
            background_stroke_color=BACKGROUND_COLOR, 
            alignment=""
        )
        
        # Animation timing
        self.term_run_time = 0.5
        self.in_between_time = 0.1
        self.definition_run_time = 0.6 + len(self.definition_text) / 150
    
    def copy(self):
        """Create a copy of this element."""
        return DefinitionElement(self.input_elem)
    
    def individual_play(self, scene):
        """Animate the definition in the scene."""
        scene.play(CustomWrite(self.term), run_time=self.term_run_time)
        scene.wait(self.in_between_time)
        scene.play(CustomWrite(self.definition), run_time=self.definition_run_time)
    
    def get_play_actions(self):
        """Get the animations to play this definition."""
        return [CustomWrite(self.term), CustomWrite(self.definition)]
    
    def individual_play_duration(self):
        """Get the duration of this definition's animation."""
        return self.term_run_time + self.in_between_time + self.definition_run_time
    
    def position_center_at(self, position):
        """Position this definition centered at the given position."""
        self.term.move_to(position)
        self.definition.next_to(self.term, RIGHT)
        self.definition.align_to(self.term, UP)
    
    def position_left_aligned(self, position):
        """Position this definition left-aligned at the given position."""
        self.term.move_to(position)
        self.term.to_edge(LEFT)
        self.definition.next_to(self.term, RIGHT)
        self.definition.align_to(self.term, UP)
    
    def get_shift_center_at_actions(self, position):
        """Get animations to shift this definition to be centered at the given position."""
        # Create temporary mobjects for positioning
        pos_term = TextMobject(self.term_text, alignment="")
        pos_definition = TextMobject(self.definition_text, alignment="")
        
        pos_term.move_to(position)
        pos_definition.next_to(pos_term, RIGHT)
        pos_definition.align_to(pos_term, UP)
        
        return [
            ApplyMethod(self.term.move_to, pos_term),
            ApplyMethod(self.definition.move_to, pos_definition)
        ]
    
    def get_shift_left_aligned_actions(self, position):
        """Get animations to shift this definition to be left-aligned at the given position."""
        # Create temporary mobjects for positioning
        pos_term = TextMobject(self.term_text, alignment="")
        pos_definition = TextMobject(self.definition_text, alignment="")
        
        pos_term.move_to(position)
        pos_term.to_edge(LEFT)
        pos_definition.next_to(pos_term, RIGHT)
        pos_definition.align_to(pos_term, UP)
        
        return [
            ApplyMethod(self.term.move_to, pos_term),
            ApplyMethod(self.definition.move_to, pos_definition)
        ]
    
    def get_bottom_position(self):
        """Get the position at the bottom of this definition."""
        return self.definition
    
    def get_fade_out_actions(self):
        """Get animations to fade out this definition."""
        return [FadeOut(self.term), FadeOut(self.definition)]


class TermElement(OutputElement):
    """Element representing a term in the presentation."""
    
    def __init__(self, input_elem):
        """
        Initialize a new TermElement.
        
        Args:
            input_elem: The input element this output element is based on
            
        Raises:
            SanimParseError: If the term syntax is invalid
        """
        super().__init__(input_elem)
        content = input_elem.content.lstrip()
        
        # Parse term
        if not content or content[0] != '"':
            raise SanimParseError('Invalid use of TERM. Syntax: TERM "term"')
        
        content = content[1:]
        if '"' not in content:
            raise SanimParseError('Invalid use of TERM. Syntax: TERM "term"')
        
        # Extract term text
        self.term_text = content[:content.find('"')]
        
        if not self.term_text:
            raise SanimParseError('Empty term in TERM')
        
        # Create term mobject
        self.term = TextMobject(
            '\\textbf{' + self.term_text + '}',
            background_stroke_color=BACKGROUND_COLOR, 
            alignment=""
        )
        self.term.set_color(DEFINITION_COLOR)
        
        # Animation timing
        self.term_run_time = 0.5
    
    def copy(self):
        """Create a copy of this element."""
        return TermElement(self.input_elem)
    
    def individual_play(self, scene):
        """Animate the term in the scene."""
        scene.play(CustomWrite(self.term), run_time=self.term_run_time)
    
    def get_play_actions(self):
        """Get the animations to play this term."""
        return [CustomWrite(self.term)]
    
    def individual_play_duration(self):
        """Get the duration of this term's animation."""
        return self.term_run_time
    
    def position_center_at(self, position):
        """Position this term centered at the given position."""
        self.term.move_to(position)
    
    def position_left_aligned(self, position):
        """Position this term left-aligned at the given position."""
        self.term.move_to(position)
        self.term.to_edge(LEFT)
    
    def get_shift_center_at_actions(self, position):
        """Get animations to shift this term to be centered at the given position."""
        return [ApplyMethod(self.term.move_to, position)]
    
    def get_shift_left_aligned_actions(self, position):
        """Get animations to shift this term to be left-aligned at the given position."""
        # Create a temporary mobject for positioning
        pos_term = TextMobject(self.term_text, alignment="")
        pos_term.move_to(position)
        pos_term.to_edge(LEFT)
        
        return [ApplyMethod(self.term.move_to, pos_term)]
    
    def get_bottom_position(self):
        """Get the position at the bottom of this term."""
        return self.term
    
    def get_fade_out_actions(self):
        """Get animations to fade out this term."""
        return [FadeOut(self.term)]
