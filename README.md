# Sanim: Slide ANIMation

Sanim (Slide ANIMation) is both a markup language for preparing presentations, and a parser for this language that produces the presentations.

It allows you to create animated presentations from simple text files using a specialized syntax.

The transition between slides is animated using Manim. [Manim (Math ANIMation)](https://github.com/3b1b/manim) is an animation engine for explanatory math videos made for the youtube channel [3Blue1Brown](https://www.youtube.com/c/3blue1brown).

Sanim encapsulates Manim so that the user can prepare slides with a style similar to Manim but without needing to write Python code. Conceptually, a Sanim presentation can be thought of as a long "scroll" of paper. Lines appear one by one (by default), below the previous one. Once there is no more space, previous lines scroll up until they disappear.
The presentation is displayed in a browser, and the user can move forward and backward using arrow keys.

**Sanim is unfinished and I have no concrete plans to finish it.** It is still buggy and has limited features. I made Sanim because I was planning to create some educational videos and I liked 3blue1brown a lot, but I wanted a tool that was easier to use. I will continue the development if/when I resume making the videos.

# Demo

The following sanim source generates [this animation](http://nmamano.com/sanim/index.html) **Use the right arrow key to start displaying the slides**. The right arrow goes back. (If the demo does not work, [here](demo.mp4) is the raw video without the advance/go back features.)

```
TITLE Complexity Theory\textemdash  Lecture 1: Introduction

DEF "In a nutshell" how to classify \textit{\textbf{problems}} according to how \textit{\textbf{hard}} they are to solve by computer \textit{\textbf{programs}}.

DEF "In this lecture" define ``problem'', ``hard'', and ``program'' formally so that we can do mathematical proofs.

- What is a \textit{\textbf{problem}}?

\textbf{Problem} ; > vs ; > \textbf{Instance}
>Multiplication ; ; >$37\times 13$
>Sorting ; ; >$8,2,3,6,1$

FLUSH 4

- A \textit{\textbf{problem}} is a \textbf{function} mapping each instance to its solution.

>\textbf{Problem} ; ; > \textbf{Instance} ; ; > \textbf{Solution}
>Multiplication ; ; >$37\times 13$ ; >$\longrightarrow$ ; >$481$
>Sorting ; ; > $8,2,3,6,1$ ;  >$\longrightarrow$ ; > $1,2,3,6,8$
>Median ; ; > $8,2,3,6,1$ ;  >$\longrightarrow$ ; > $3$

- We focus on \textit{\textbf{decision problems}}: problems where the solution is YES$/$NO.

FLUSH 12

\textbf{Decision Problem} ; ; > \textbf{Instance} ; ; > \textbf{Solution}
>Prime testing ; ; >$9$ ; >$\longrightarrow$ ; > NO
;; >$11$; >$\longrightarrow$; >YES

DEF "In general" a decision problem asks ``does the instance have $X$ property?''

- We assume that the instance is just a (finite) \textbf{binary string}.

Mathematical object ; >vs ; >Binary representation
```

### Basic Usage

1. Create a text file for your presentation (e.g., `presentations/my_presentation/my_presentation.txt`)

This file uses Sanim syntax.

2. Run: `./sanim.py presentations/my_presentation/my_presentation.txt`

Add -l for fast render/lower quality. Recommended for fast iteration.

3. View the generated animation in the same folder.

Running the script generates a file `sanim_interactive_AUTOGENERATED.html` in the same folder as the sanim source. It can be opened with a browser (I tested on chrome), and advanced with left/right arrow keys.

The HTML file loads an mp4 file (vid.mp4 in the same folder) with all the slide transitions. Then it plays the mp4 forward or backward the correct amount of time when pressing right/left arrows.

It is recommended that each sanim project is in its own folder in the `presentations/` folder because the output/auxiliary files have generic names, so they are identified by the folder they are in.

# Sanim Syntax

Every non-empty line of the input file corresponds to an "item" of the presentation.
Items can be of several types. The first word the line determines the type. By default, the rest of the input line is parsed as latex (it can include $ $, \textit{}, \textbf{}, and \underline{ }).

### Item types

- **TITLE**: Creates a title (e.g., `TITLE My Presentation`)

Appears with bigger font and underlining.

- **<nothing>**: Creates plain text (e.g., `This is some text`)
- **-**: Creates a bullet point (e.g., `- This is a bullet point`)

Appears as a bullet point with 'X' highlighted, followed by ':' and the text.

- **DEF**: Creates a definition with a term and explanation (e.g., `DEF "Algorithm" A step-by-step procedure for calculations`)
- **IMAGE**: Displays an image (e.g., `IMAGE path/to/image.png`)

Displays an image from the specified path. Optionally accepts a size multiplier (default 1.0) to adjust the image size. For example: "IMAGE img.png 1.5" makes the image 50% larger.

### Commands

- **FLUSH**: Removes all content so far.

It accepts an optional number, in which case it removes content up to a specific line number and repositions the remaining content (e.g., `FLUSH 5`).

### Modifiers

- **>**: Indicates that this element shouldn't wait for user input to display (e.g., `>PLAIN This appears immediately`)
- **^**: Reserved for future use

### Special symbols:

#### Multiple Elements Per Line

To insert several items spaced evenly in the same line, separate them by `;`

```
TITLE My Presentation; >PLAIN Subtitle
```

This can be used to center a single item by surrounding it by `;`.

#### Rendering multiple elements at once:

- `>`: when this is the first char of an item, the line displays together with the previous line, without waiting for user input.

# Todo

- add shortcuts for and \textbf \textit
- smoother play backwards
- modify the Manim tex template depending on the browser's width, so that it adds line breaks at the appropriate points
- try different fonts and animations to distinguish the style from Manim
- add command to color specific words (\color{}{} not working)
- add labels for flushing instead of line numbers
- fix that DEF item shifts slightly to the right when flushing.
- reduce width of title underline

#### Ideas for features

- pin functionality for lines that don't get flushed (using symbol "^")
- Automatic flush: once there is no more space, previous lines scroll up until they disappear (without cutting lines in half).
- Integration with native Manim animations.

# Prerequisites

- Python 3.6 or higher
- The Manim engine dependencies
