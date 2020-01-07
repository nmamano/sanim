
===============================================
About
===============================================

Sanim is a a mark-up language for videos lectures and presentations, and a parser that takes as input a file in this mark-up language and produces a presentation using manim.

Conceptually, the presentation is a long "scroll" of paper. Lines appear one by one, below the previous one. Once there is no more space, previous lines scroll up until they disappear.
The presentation is displayed in the web, and the user can move forward and backward using arrow keys.

===============================================
Usage
===============================================

1.
> python extract_scene.py sanim.py Sanim -x presentations/lecture1/lecture1.txt -l
(Add -p for video preview and remove -l for best quality)

2. Open presentations/lecture1/sanim_web_COPY.html
and use left/right arrows

- It is recommended that each sanim project is in its own folder, because the output files are identified by the folder they are in, and not by their names. they have names such as "folder/pic.png" and "folder/vid.mp4". Currently, all our projects are in presentations/projectname/



===============================================
Syntax of the mark-up language: (NOT ALL FEATURES LISTED FOR NOW)
===============================================

Every line of the mark-up file (input) corresponds to an "item" of the output (presentation).
An  item can be of many types. The first word of every input line determines the type of the item. In general, the rest of the input line is parsed as latex (you can use $ $, \textit{}, \textbf{}, and \underline{ }).

Item types:
TITLE --- bigger font, underline
- --- adds text with a bullet point
<nothing> --- adds plain text
DEF "X" --- Definition: bullet point with X highlighted and ':'
SCENE "X" Y --- loads the scene X, centered, and with a height of Y
IMAGE "X" Y --- loads image X, centered, and with a height of Y

To insert several items spaced evenly in the same line, separate them by ;
(can be used to center a single item too)

Special keywords:
FLUSH X --- removes all the lines befor line X
> --- when it is the first char of an item, there is no wait for user input before showing the line. Cannot appear before (

===============================================
Example:
===============================================

TITLE Complexity Theory\textemdash  Lecture 1: Introduction
DEF "In a nutshell" how to classify \textit{\textbf{problems}} according to how \textit{\textbf{hard}} they are to solve by computer \textit{\textbf{programs}}.
DEF "In this video" define ``problem'', ``hard'', and ``program'' mathematically so we can prove stuff.
- What is a \textit{\textbf{problem}}?
\textbf{Instance} ; > vs ; > \textbf{General case}
$37\times 13$ ; ; > Multiplication
$8,2,3,6,1$ ; ; > Sorting
- A \textit{\textbf{problem}} is a \textbf{function} mapping each instance to its solution.
FLUSH 4
\textbf{Problem} ; ; > \textbf{Instance} ; ; > \textbf{Solution}
Multiplication ; ; >$37\times 13$ ; >$\longrightarrow$ ; >$481$
>Sorting ; ; > $8,2,3,6,1$ ;  >$\longrightarrow$ ; > $1,2,3,6,8$
Median ; ; > $8,2,3,6,1$ ;  $\longrightarrow$ ; > $3$
- We focus on \textit{\textbf{decision problems}}: problems where the solution is YES$/$NO.
FLUSH 8
\textbf{Decision Problem} ; ; > \textbf{Instance} ; ; > \textbf{Solution}
Prime testing ; ; $9$ ; >$\longrightarrow$ ; > NO
;; >$11$; >$\longrightarrow$; >YES
DEF "In general" a decision problem asks ``does the instance have $X$ property?''
- We assume that the instance is just a (finite) \textbf{binary string}.
FLUSH 14
Mathematical object ; >vs ; >Binary representation


===============================================
TODO:
===============================================

- add \hl1{} and \hl2{} commands
- add START and END commands to simulate only sections
- modify the tex file depending on the width available, so that it adds line breaks at the appropriate points
- try different fonts to make it more different than manim
- add command to color specific words (\color{}{} not working)
- add labels for flushing instead of line numbers
- pin functionality (^)
- embed animations and images and videos
- fix why defitem is moving to the right when flushing
- reduce width of title underline

ideas for features:
- add command to switch to secondary colors or arbitrary color with
COLOR X


===============================================
OLD README:
===============================================


Idea: design a mark-up language for videos lectures and presentations, and a parser that takes as input a file in this mark-up language and produces a presentation using manim.

Conceptually, the presentation is a long "scroll" of paper. Lines appear one by one, below the previous one. Once there is no more space, previous lines scroll up until they disappear (without cutting lines in half). To show the next line, the user must press intro. It allows the integration of manim scenes.

Syntax of the mark-up language:
Every line of the mark-up file (input) corresponds to a "line" of the output (presentation).
An output line can be of many types. The first word of every input line determines the type of the output line. The rest of the input line is parsed as latex.

Line types:
Title --- bigger font, flushes everything before it
- --- adds text with a bullet point
* --- adds text without a bullet point
Def "X" --- Definition: bullet point with X highlighted and ':'
( --- A set of lines aligned horizontally and evenly spaced. one item per line until a line with ) is reached. Trick: using ( and ) with a single line can be used to center it.
Scene "X" Y --- loads the scene X, centered, and with a height of Y
Image "X" Y --- loads image X, centered, and with a height of Y

Special keywords:
> --- when it is the first char of a line, there is no wait for user input before showing the line


Example presentation:

Title Introduction to Computational Complexity
- This video: basic definitions needed for explaining Turing Machines (next video)
Def "Alphabet" a finite set of symbols
(
* $\Sigma=\{a,b,c\}$
* $\Sigma=\{0,1\}$
* $\Sigma=\{a,b,\ldots,z\}$
* ASCII symbols
)
Def "Word" a finite sequence of symbols from an alphabet
(
* $w=abbab$
* $w=0110$
* $w=\varepsilon$
* hello my name is martha
)
Def "Language" a set of words from an alphabet (can be infinite!)
- $\{aa, aba, babab\}$
- words over $\{a,b\}$ with an even number of $a$'s
- words in english
- sentences in english


