# Sanim Project Guide

This document describes the project layout, architecture, and common tasks.

It can help AI assistants understand and modify Sanim code.

## Directory Structure

```
sanim/
├── manim_engine/ # Core manim engine components
│ └── ... (manim components)
│
├── animations/ # Reusable custom animations
│ ├── __init__.py
│ └── custom_animation.py
│
├── elements/ # Element types
│ ├── __init__.py
│ ├── base.py # Base OutputElement class
│ ├── text.py # Text-based elements
│ └── media.py # Image and video elements
│
├── util/ # Utility functions
│ ├── __init__.py
│ ├── parsing.py # Input parsing utilities
│ ├── positioning.py # Element positioning utilities
| ├── exceptions.py # Custom exception types
│ └── rendering.py # Rendering utilities
│
├── presentations/ # Your presentation files
│ ├── example1/
│ │ ├── example1.txt
│ │ └── sanim_interactive_AUTOGENERATED.html
│ └── example2/
│ └── ...
│
├── sanim.py # Main implementation
├── README.md # Main documentation
└── PROJECT_GUIDE.md # Guide for AI assistants
```

## Architecture

### Architecture Overview

Sanim uses a clear separation of concerns following these principles:

1. **Parsing**: Convert text input into structured data
2. **Data Model**: Represent presentation content as objects
3. **Rendering**: Transform objects into animations

```
Input File → Parser → Content Model → Renderer → Animation
```

### Module Structure

| Module                | Responsibility                             |
| --------------------- | ------------------------------------------ |
| `elements/base.py`    | Base element class definition              |
| `elements/text.py`    | Text-based elements                        |
| `elements/media.py`   | Media elements (images, etc.)              |
| `util/parsing.py`     | Parsing utilities and input representation |
| `util/rendering.py`   | Rendering logic                            |
| `util/positioning.py` | Positioning of elements logic              |
| `sanim.py`            | Main implementation and orchestration      |

### Key Classes

| Class Name             | Module                | Description                                   |
| ---------------------- | --------------------- | --------------------------------------------- |
| `OutputElement`        | `elements/base.py`    | Base class for all visual elements            |
| `TitleElement`         | `elements/text.py`    | Represents a title                            |
| `PlainTextElement`     | `elements/text.py`    | Represents plain text                         |
| `BulletElement`        | `elements/text.py`    | Represents a bullet point                     |
| `DefinitionElement`    | `elements/text.py`    | Represents a definition                       |
| `TermElement`          | `elements/text.py`    | Represents a term                             |
| `ImageElement`         | `elements/media.py`   | Represents an image                           |
| `InputParser`          | `util/parsing.py`     | Parses input from a text file                 |
| `InputElement`         | `util/parsing.py`     | Represents a primitive element from the input |
| `InputLine`            | `util/parsing.py`     | Represents a line from the input file         |
| `ElementPosition`      | `util/positioning.py` | Manages element positioning                   |
| `AnimationBuffer`      | `util/rendering.py`   | Manages animation buffering                   |
| `PresentationRenderer` | `util/rendering.py`   | Orchestrates the rendering process            |
| `Sanim`                | `sanim.py`            | Main scene class                              |

### Key Components

1. **Parser**: Converts text input into structured elements

- `InputParser`: Parses the input file into structured elements
- `InputElement`: Represents a single primitive element (e.g., a title, text)
- `InputLine`: Represents a line from the input file, containing multiple elements

2. **Elements**: Different types of content

   - `OutputElement`: Base class for all output/visual elements
   - `TitleElement`: For titles
   - `PlainTextElement`: For plain text
   - `BulletElement`: For bullet points
   - `DefinitionElement`: For definitions (term + explanation)
   - `ImageElement`: For images

3. **Renderer**: Handles animation and positioning

   - `ElementPosition`: Manages element positioning
   - `AnimationBuffer`: Manages animation buffering
   - `PresentationRenderer`: Orchestrates the rendering process

4. **Main Scene**: The entry point
   - `Sanim`: The main scene class that renders the presentation

## Extending Sanim

Sanim is designed to be easily extensible.

### Adding New Elements

When adding new elements, follow this structure:

1. Create the element class in the appropriate module that inherits from `OutputElement`

- For standard elements: Add to the appropriate module in `elements/`
- For project-specific elements: Create a new module in `elements/`

Example for adding a code block element:

```python
# In elements/special.py
from .base import OutputElement

class CodeBlockElement(OutputElement):
    """Element representing a code block in the presentation."""

    def __init__(self, input_elem: InputElement):
        super().__init__(input_elem)
        content = input_elem.content
        if not content:
            raise SanimParseError('Empty code block')

        # Create the code mobject with monospace font and syntax highlighting
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

    # Implement all the required methods...
```

Implement all required methods (see the existing element classes for examples).

2. To add support for a new element type, update the `InputLine.__init__` method in `util/parsing.py`

```python
# In InputLine.__init__
from elements.text import CodeElement  # Import your new element

# Inside the method:
elif elem.keyword == "CODE":
    self.output_elements.append(CodeElement(elem))
```

3. Add the keyword to `CONTENT_KEYWORDS` in `util/parsing.py`:

```python
CONTENT_KEYWORDS = {"TITLE", "DEF", "-", "PLAIN", "IMAGE", "TERM", "CODE"}
```

### Adding New Animations

To change how elements are animated, you can modify the `CustomWrite` class in `animations/custom_animation.py` or create new animation classes.

When adding new animations, follow this structure:

1. For general-purpose animations: Add to `animations/custom_animation.py`
2. For special effects: Add to `animations/special_effects.py`
3. For project-specific animations: Create a new module in `animations/`

Example for adding a glitch effect animation:

```python
# In animations/special_effects.py
from manim import Animation

class GlitchEffect(Animation):
    """Creates a digital glitch effect on a mobject."""
    # ... implementation
```

### Modifying Visual Appearance

To change the visual style of elements:

1. **Change default colors**: Modify the constants at the top of the file

```python
BACKGROUND_COLOR = "#f0f0f0"  # Changed from "#e6f3ff"
DEFINITION_COLOR = "#007acc"  # Changed from "#991f00"
```

2. **Modify the font**: Update the LaTeX template in `tex_template.tex`

3. **Change animation styles**: Modify or create new animations in `animations/custom_animations.py`

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

## Troubleshooting

### Common Issues

- **ParseError**: Check your input syntax, especially for definitions and images
- **RenderError**: Make sure all referenced files (images) exist and are accessible
- **Position Issues**: If elements overlap, check the positioning code in your element classes

### Common Pitfalls

1. **Position Tracking**: Be careful with position tracking. The `ElementPosition` class maintains the current position for new elements. Always use this system rather than hardcoding positions.

2. **Animation Buffering**: Understand the animation buffer. Elements are either played individually or grouped depending on the `wait_for_input` flag.

3. **Error Handling**: Always use `SanimParseError` and `SanimRenderError` for errors. Never use `sys.exit()` directly.

## Internal Documentation for AI Assistants

### Key Files

- `sanim.py`: Main implementation file and entry point
- `animations/custom_animation.py`: Custom animation classes

### Implementation Notes

- Element positioning is tracked by `ElementPosition` which updates after each element
- Animations are buffered in `AnimationBuffer` to allow grouping multiple elements
- All visual elements inherit from `OutputElement` which defines the interface
- Error handling uses custom exception classes for clear error messages
- Type hints are used extensively to make the code more maintainable

### Modifying Visuals

- Font: Modified in `tex_template.tex`
- Colors: Changed via constants at the top of `sanim.py`
- Animation styles: Modified in `animations/custom_animation.py`

### Adding Commands

New commands (like `FLUSH`) would need:

1. Add the command to `COMMAND_KEYWORDS`
2. Add a branch in `PresentationRenderer.render_presentation` to handle the command
3. Implement the command's logic

### Best Practices

1. New elements should inherit from `OutputElement` and implement all abstract methods.

2. Use type hints for function parameters and return values.

3. Keep parsing, data model, and rendering logic separate.

### Debugging Tips

1. Use `print()` statements to see what's happening in the code.

2. To debug positioning issues, temporarily show the position markers.

```python
# For debugging positions
self.scene.play(ShowCreation(position))
```

3. Print the parsed elements to see if the input is parsed correctly.

```python
# For debugging parsing
print([elem.keyword for elem in input_line.input_elements])
```

4. Add temporary bounding boxes to see where elements are positioned.

```python
# For debugging element positions
rect = SurroundingRectangle(element.get_bottom_position())
self.scene.play(ShowCreation(rect))
self.scene.wait(0.5)
self.scene.play(FadeOut(rect))
```
