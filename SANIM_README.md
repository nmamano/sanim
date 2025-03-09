# Sanim: Simplified Animation System

Sanim is a simplified animation system built on top of the [Manim](https://github.com/3b1b/manim) animation engine. It allows you to create animated presentations from simple text files using a specialized syntax.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Manim engine and its dependencies

### Installation

1. Make sure you have Manim installed
2. Clone this repository
3. You're ready to go!

### Basic Usage

1. Create a text file for your presentation (e.g., `my_presentation.txt`)
2. Run: `python extract_scene.py -x my_presentation.txt`
3. View the generated animation

## Input File Syntax

Sanim uses a special syntax for creating presentations:

### Content Elements

- **TITLE**: Creates a title (e.g., `TITLE My Presentation`)
- **PLAIN**: Creates plain text (e.g., `PLAIN This is some text`)
- **-**: Creates a bullet point (e.g., `- This is a bullet point`)
- **DEF**: Creates a definition with a term and explanation (e.g., `DEF "Algorithm" A step-by-step procedure for calculations`)
- **IMAGE**: Displays an image (e.g., `IMAGE path/to/image.png`)

### Commands

- **FLUSH**: Removes all content up to a specific line number and repositions the remaining content (e.g., `FLUSH 5`)

### Modifiers

- **>**: Indicates that this element shouldn't wait for user input to display (e.g., `>PLAIN This appears immediately`)
- **^**: Reserved for future use

### Multiple Elements Per Line

You can include multiple elements on a single line, separated by semicolons:

```
TITLE My Presentation; >PLAIN Subtitle
```

## Architecture

The refactored Sanim codebase follows a clean, modular architecture:

### Key Components

1. **Parser**: Converts text input into structured elements
   - `InputParser`: Parses the input file
   - `InputElement`: Represents a single element from the input
   - `InputLine`: Represents a line from the input file

2. **Elements**: Different types of content
   - `OutputElement`: Base class for all output elements
   - `TitleElement`: For titles
   - `PlainTextElement`: For plain text
   - `BulletElement`: For bullet points
   - `DefinitionElement`: For definitions
   - `ImageElement`: For images

3. **Renderer**: Handles animation and positioning
   - `ElementPosition`: Manages element positioning
   - `AnimationBuffer`: Manages animation buffering
   - `PresentationRenderer`: Orchestrates the rendering process

4. **Main Scene**: The entry point
   - `Sanim`: The main scene class that renders the presentation

## Extending Sanim

Sanim is designed to be easily extensible. Here's how to add new element types:

1. Create a new class that inherits from `OutputElement`
2. Implement all required methods (see the existing element classes for examples)
3. Add your new element to the `CONTENT_KEYWORDS` list
4. Add a new case in the `InputLine.__init__` method to create your element

## Common Scenarios

### Adding a New Element Type

Example: Adding a `CODE` element to display code blocks:

```python
class CodeElement(OutputElement):
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

Then update:
1. Add "CODE" to `CONTENT_KEYWORDS`
2. Add a case in `InputLine.__init__` to create your element

### Modifying Animation Styles

To change how elements are animated, you can modify the `CustomWrite` class in `custom_animation.py` or create new animation classes.

## Troubleshooting

### Common Issues

- **ParseError**: Check your input syntax, especially for definitions and images
- **RenderError**: Make sure all referenced files (images) exist and are accessible
- **Position Issues**: If elements overlap, check the positioning code in your element classes

## Best Practices

1. **Keep it Simple**: Use short, focused lines of text
2. **Use Modifiers Sparingly**: Only use `>` when you really need elements to appear together
3. **Test Incrementally**: Build your presentation one section at a time
4. **Use Flush**: Use `FLUSH` to clear the screen and start new sections

## Internal Documentation for AI Assistants

### Key Files

- `sanim.py`: Main implementation file
- `custom_animation.py`: Custom animation classes
- `extract_scene.py`: Entry point script (modified from manim)

### Implementation Notes

- Element positioning is tracked by `ElementPosition` which updates after each element
- Animations are buffered in `AnimationBuffer` to allow grouping multiple elements
- All visual elements inherit from `OutputElement` which defines the interface
- Error handling uses custom exception classes for clear error messages
- Type hints are used extensively to make the code more maintainable

### Modifying Visuals

- Font: Modified in `tex_template.tex`
- Colors: Changed via constants at the top of `sanim.py`
- Animation styles: Modified in `custom_animation.py`

### Adding Commands

New commands (like `FLUSH`) would need:
1. Add the command to `COMMAND_KEYWORDS`
2. Add a branch in `PresentationRenderer.render_presentation` to handle the command
3. Implement the command's logic