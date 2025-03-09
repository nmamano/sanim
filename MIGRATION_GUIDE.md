# Migration Guide: Original Sanim to Refactored Version

This guide will help you migrate from the original `sanim.py` implementation to the new refactored version.

## Major Changes Overview

The refactored version makes these significant improvements:

1. **Cleaner Architecture**: Clear separation between parsing, data model, and rendering
2. **Better Error Handling**: Uses exceptions instead of `sys.exit()`
3. **Improved Documentation**: Extensive docstrings and type hints
4. **Reduced Side Effects**: Explicit state management instead of mutable parameters
5. **More Maintainable Classes**: Better inheritance patterns and cleaner interfaces
6. **Consistent Naming**: Renamed classes and methods for clarity

## Class Name Changes

| Original | Refactored | Description |
|----------|------------|-------------|
| `InputLine` | `InputLine` | Represents a line from the input file (unchanged) |
| `InputElem` | `InputElement` | Represents a primitive element from the input |
| `OutputElem` | `OutputElement` | Base class for all visual elements |
| `TitleElem` | `TitleElement` | Represents a title |
| `PlainElem` | `PlainTextElement` | Represents plain text |
| `BulletElem` | `BulletElement` | Represents a bullet point |
| `DefElem` | `DefinitionElement` | Represents a definition |
| `ImageElem` | `ImageElement` | Represents an image |
| N/A | `ElementPosition` | Manages element positioning |
| N/A | `AnimationBuffer` | Manages animation buffering |
| N/A | `PresentationRenderer` | Orchestrates the rendering process |

## Method Name Changes

| Original | Refactored | Description |
|----------|------------|-------------|
| `get_bottom_right_mobject()` | `get_bottom_position()` | Returns the bottom position of an element |
| `individual_play()` | `individual_play()` | Plays an individual element (unchanged) |
| `input_to_lines()` | `InputParser.parse_file()` | Parses the input file |
| `animate_lines()` | `PresentationRenderer.render_presentation()` | Renders the presentation |
| `animate_content_line()` | `PresentationRenderer.render_line()` | Renders a content line |
| `get_shift_actions()` | `PresentationRenderer.get_shift_actions()` | Gets shift animations |
| `display_animation_buffer()` | `AnimationBuffer.flush()` | Plays and clears the animation buffer |

## Key Functional Differences

1. **Error Handling**:
   - Original: Uses `sys.exit()` to terminate on errors
   - Refactored: Uses custom exception classes (`SanimParseError`, `SanimRenderError`)

2. **Position Tracking**:
   - Original: Uses a mutable `curr_pos` parameter passed through functions
   - Refactored: Uses the `ElementPosition` class to manage position

3. **Animation Buffering**:
   - Original: Uses a mutable `anim_buffer` parameter
   - Refactored: Uses the `AnimationBuffer` class

4. **Constants**:
   - Original: Mixes constants throughout the code
   - Refactored: Groups related constants at the top of the file

## Code Examples

### Creating a New Element Type

**Original**:
```python
class NewElem(OutputElem):
    def __init__(self, input_elem):
        super().__init__(input_elem)
        self.text = TextMobject(input_elem.content)
        self.run_time = 1.0
        
    def individual_play(self, scene):
        scene.play(Write(self.text), run_time=self.run_time)
        
    def get_play_actions(self):
        return [Write(self.text)]
        
    # ... implement other required methods
```

**Refactored**:
```python
class NewElement(OutputElement):
    """Element representing a new type of content."""
    
    def __init__(self, input_elem: InputElement):
        super().__init__(input_elem)
        self.text = TextMobject(
            input_elem.content,
            color=BLACK,
            background_stroke_color=BACKGROUND_COLOR
        )
        self.run_time = 1.0
        
    def individual_play(self, scene: Scene) -> None:
        scene.play(CustomWrite(self.text), run_time=self.run_time)
        
    def get_play_actions(self) -> List[Animation]:
        return [CustomWrite(self.text)]
        
    # ... implement other required methods with type hints and docstrings
```

### Extending the Parser

**Original**:
```python
# In InputLine.__init__
for elem in self.input_elems:
    if elem.keyword == "TITLE":
        self.output_content_elems.append(TitleElem(elem))
    # ... other element types
    elif elem.keyword == "NEW":
        self.output_content_elems.append(NewElem(elem))
```

**Refactored**:
```python
# In InputLine.__init__
for elem in self.input_elements:
    if elem.keyword == "TITLE":
        self.output_elements.append(TitleElement(elem))
    # ... other element types
    elif elem.keyword == "NEW":
        self.output_elements.append(NewElement(elem))
```

## Migration Process

To migrate to the refactored version:

1. **Replace Core Files**:
   - Replace the original `sanim.py` with the refactored version
   - Add the new helper files (`AI_GUIDE.md`, `SANIM_README.md`)

2. **Update Entry Point**:
   - The entry point (`extract_scene.py`) should work without changes

3. **Test Thoroughly**:
   - Test with existing presentations to ensure compatibility
   - Test edge cases to verify improved error handling

4. **Update Custom Code**:
   - If you have created custom elements, update them to follow the new patterns

## Backward Compatibility

The refactored version should be fully compatible with existing presentation files. If you encounter any issues:

1. Check the parser logic for any subtle differences
2. Verify the positioning calculations match the original
3. Ensure animation timing is preserved

## Getting Help

If you need assistance with the migration:

1. Refer to the detailed documentation in `SANIM_README.md` and `AI_GUIDE.md`
2. Check the comprehensive docstrings in the new code
3. Look at the type hints for guidance on parameter types and return values