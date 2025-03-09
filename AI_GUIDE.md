# Sanim AI Guide

This document is specifically designed to help AI assistants understand and modify Sanim code. It provides detailed information about the architecture, common tasks, and best practices.

## Architecture Overview

Sanim uses a clear separation of concerns following these principles:

1. **Parsing**: Convert text input into structured data
2. **Data Model**: Represent presentation content as objects
3. **Rendering**: Transform objects into animations

```
Input File → Parser → Content Model → Renderer → Animation
```

## Key Classes and Their Responsibilities

### Parser Components

- `InputParser`: Parses the input file into structured elements
- `InputElement`: Represents a single primitive element (e.g., a title, text)
- `InputLine`: Represents a line from the input file, containing multiple elements

### Data Model

- `OutputElement`: Base class for all visual elements
  - `TitleElement`: Represents a title
  - `PlainTextElement`: Represents plain text
  - `BulletElement`: Represents a bullet point
  - `DefinitionElement`: Represents a definition (term + explanation)
  - `ImageElement`: Represents an image

### Renderer Components

- `ElementPosition`: Manages the positioning of elements
- `AnimationBuffer`: Manages buffering of animations
- `PresentationRenderer`: Orchestrates the rendering process
- `Sanim`: The main scene class that renders the presentation

## Common Tasks and How to Implement Them

### Adding a New Element Type

To add a new element type (e.g., a code block element):

1. **Add the keyword**: Add your element keyword to `CONTENT_KEYWORDS`

```python
CONTENT_KEYWORDS = {"TITLE", "DEF", "-", "PLAIN", "IMAGE", "CODE"}  # Added "CODE"
```

2. **Create the element class**: Create a new class inheriting from `OutputElement`

```python
class CodeElement(OutputElement):
    """Element representing a code block in the presentation."""
    
    def __init__(self, input_elem: InputElement):
        super().__init__(input_elem)
        content = input_elem.content
        if not content:
            raise SanimParseError('Empty code block')
        
        # Create code mobject with monospace font
        self.text = TextMobject(
            "\\texttt{" + content + "}",
            color=BLACK,
            background_stroke_color=BACKGROUND_COLOR
        )
        self.run_time = 0.6 + len(content) / 150
        
        # Add a background rectangle
        self.background = SurroundingRectangle(
            self.text,
            color=LIGHT_GRAY,
            fill_color=LIGHT_GRAY,
            fill_opacity=0.2
        )
        
        # Group the elements
        self.group = VGroup(self.background, self.text)
    
    def copy(self):
        """Create a copy of this element."""
        return CodeElement(self.input_elem)
    
    def individual_play(self, scene):
        """Animate the code block in the scene."""
        scene.play(FadeIn(self.background), run_time=self.run_time/2)
        scene.play(CustomWrite(self.text), run_time=self.run_time)
    
    def get_play_actions(self):
        """Get the animations to play this code block."""
        return [FadeIn(self.background), CustomWrite(self.text)]
    
    def individual_play_duration(self):
        """Get the duration of this code block's animation."""
        return self.run_time * 1.5  # Extra time for the background
    
    def position_center_at(self, position):
        """Position this code block centered at the given position."""
        self.group.move_to(position)
    
    def position_left_aligned(self, position):
        """Position this code block left-aligned at the given position."""
        self.group.move_to(position)
        self.group.to_edge(LEFT)
    
    def get_shift_center_at_actions(self, position):
        """Get animations to shift this code block to be centered."""
        return [ApplyMethod(self.group.move_to, position)]
    
    def get_shift_left_aligned_actions(self, position):
        """Get animations to shift this code block to be left-aligned."""
        temp_group = VGroup(
            SurroundingRectangle(TextMobject("aux")),
            TextMobject("aux")
        )
        temp_group.move_to(position)
        temp_group.to_edge(LEFT)
        return [ApplyMethod(self.group.move_to, temp_group)]
    
    def get_bottom_position(self):
        """Get the position at the bottom of this code block."""
        return self.group
    
    def get_fade_out_actions(self):
        """Get animations to fade out this code block."""
        return [FadeOut(self.background), FadeOut(self.text)]
```

3. **Update the element creation logic**: Add your element to `InputLine.__init__`

```python
def __init__(self, line_num: int, raw_content: str):
    # ... existing code ...
    for elem in self.input_elements:
        if elem.keyword == "TITLE":
            self.output_elements.append(TitleElement(elem))
        elif elem.keyword == "PLAIN":
            self.output_elements.append(PlainTextElement(elem))
        elif elem.keyword == "-":
            self.output_elements.append(BulletElement(elem))
        elif elem.keyword == "DEF":
            self.output_elements.append(DefinitionElement(elem))
        elif elem.keyword == "IMAGE":
            self.output_elements.append(ImageElement(elem))
        elif elem.keyword == "CODE":  # Added this branch
            self.output_elements.append(CodeElement(elem))
```

### Adding a New Command

To add a new command (e.g., a command to change the background color):

1. **Add the keyword**: Add your command keyword to `COMMAND_KEYWORDS`

```python
COMMAND_KEYWORDS = {"FLUSH", "BACKGROUND"}  # Added "BACKGROUND"
```

2. **Update the command handling logic**: Modify `PresentationRenderer.render_presentation`

```python
# In PresentationRenderer.render_presentation
element = elements[0]
if element.keyword == 'FLUSH':
    # Existing FLUSH handling code...
elif element.keyword == 'BACKGROUND':
    # New BACKGROUND command
    try:
        color_name = element.content.strip()
        if not color_name:
            raise SanimParseError("Background color name is required")
        
        # Get the color from manim's color constants
        if color_name in globals():
            color = globals()[color_name]
        else:
            # Try as hex color
            color = color_name
        
        # Change the background
        self.scene.camera.background_color = color
        
        # Play a quick animation to show the change
        fullscreen_rect = Rectangle(
            width=FRAME_WIDTH*2, 
            height=FRAME_HEIGHT*2,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0
        )
        self.scene.play(FadeIn(fullscreen_rect), run_time=0.5)
        self.scene.play(FadeOut(fullscreen_rect), run_time=0.5)
        
    except Exception as e:
        raise SanimParseError(f"Invalid background color: {element.content}")
else:
    raise SanimParseError(f"Unknown command: {element.keyword}")
```

### Modifying Visual Appearance

To change the visual style of elements:

1. **Change default colors**: Modify the constants at the top of the file

```python
BACKGROUND_COLOR = "#f0f0f0"  # Changed from "#e6f3ff"
DEFINITION_COLOR = "#007acc"  # Changed from "#991f00"
```

2. **Modify the font**: Update the LaTeX template in `tex_template.tex`

3. **Change animation styles**: Modify or create new animations in `custom_animation.py`

```python
# Example: Create a fade-in-from-bottom animation
class FadeInFromBottom(Animation):
    CONFIG = {
        "rate_func": smooth,
        "submobject_mode": "lagged_start",
    }
    
    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs)
        mobject.shift(DOWN)  # Start from below
        mobject.fade(1)  # Start transparent
        Animation.__init__(self, mobject, **kwargs)
    
    def interpolate_mobject(self, alpha):
        self.mobject.become(self.starting_mobject)
        self.mobject.shift(DOWN * (1 - alpha))
        self.mobject.fade(1 - alpha)
```

## Pitfalls and Best Practices

### Common Pitfalls

1. **Position Tracking**: Be careful with position tracking. The `ElementPosition` class maintains the current position for new elements. Always use this system rather than hardcoding positions.

2. **Animation Buffering**: Understand the animation buffer. Elements are either played individually or grouped depending on the `wait_for_input` flag.

3. **Memory Management**: Avoid creating too many large mobjects. Manim can be memory-intensive.

4. **Error Handling**: Always use `SanimParseError` and `SanimRenderError` for errors. Never use `sys.exit()` directly.

### Best Practices

1. **Follow the Inheritance Pattern**: New elements should inherit from `OutputElement` and implement all abstract methods.

2. **Use Type Hints**: Always use type hints for function parameters and return values.

3. **Add Docstrings**: Document all classes and methods with clear docstrings.

4. **Separate Concerns**: Keep parsing, data model, and rendering logic separate.

5. **Test Thoroughly**: Test new features with different kinds of input.

## Debugging Tips

1. **Add Print Statements**: Use `print()` statements to see what's happening in the code.

2. **Inspect Mobjects**: To debug positioning issues, temporarily show the position markers.

```python
# For debugging positions
self.scene.play(ShowCreation(position))
```

3. **Check Parse Results**: Print the parsed elements to see if the input is parsed correctly.

```python
# For debugging parsing
print([elem.keyword for elem in input_line.input_elements])
```

4. **Visualize Bounding Boxes**: Add temporary bounding boxes to see where elements are positioned.

```python
# For debugging element positions
rect = SurroundingRectangle(element.get_bottom_position())
self.scene.play(ShowCreation(rect))
self.scene.wait(0.5)
self.scene.play(FadeOut(rect))
```