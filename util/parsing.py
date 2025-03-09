"""
Input parsing utilities for Sanim.
"""

from util.exceptions import SanimParseError

# Input syntax definitions
CONTENT_KEYWORDS = {"TITLE", "DEF", "-", "PLAIN", "IMAGE", "TERM"}
COMMAND_KEYWORDS = {"FLUSH"}
MODIFIER_SYMBOLS = {">", "^"}  # ^ is reserved for future use

class InputParser:
    """
    Parses input from a text file into structured elements.
    """
    
    @staticmethod
    def parse_file(file_path):
        """
        Parse a file into a list of InputLine objects.
        
        Args:
            file_path: Path to the input file
            
        Returns:
            List of InputLine objects
            
        Raises:
            SanimParseError: If there's an error parsing the file
        """
        try:
            with open(file_path, 'r') as f:
                lines = f.read().splitlines()
            
            result = []
            for i, line in enumerate(lines, 1):
                if line.strip():  # Skip empty lines
                    result.append(InputLine(i, line))
            return result
        except Exception as e:
            raise SanimParseError(f"Error parsing file {file_path}: {str(e)}")


class InputElement:
    """
    Represents a single element from the input file.
    """
    
    def __init__(self, raw_content):
        """
        Initialize a new InputElement from raw text.
        
        Args:
            raw_content: Raw text content from the input file
            
        Raises:
            SanimParseError: If there's an error parsing the element
        """
        if ';' in raw_content:
            raise SanimParseError('Input element cannot contain ";"')
        
        # Store original content
        self.raw_content = raw_content[:]
        
        # Parse modifiers (>, ^, etc.)
        self.modifiers = []
        i = 0
        while i < len(raw_content) and (raw_content[i] == ' ' or raw_content[i] in MODIFIER_SYMBOLS):
            if raw_content[i] in MODIFIER_SYMBOLS:
                self.modifiers.append(raw_content[i])
            i += 1
        
        # Skip trailing whitespace after modifiers
        while i < len(raw_content) and raw_content[i] == ' ':
            i += 1
        
        # Parse keyword and content
        remaining_content = raw_content[i:]
        if not remaining_content:
            # Empty content
            self.keyword = "PLAIN"
            self.content = ""
            if '>' not in self.modifiers:
                self.modifiers.append('>')  # Never wait for empty input
            self.keyword_type = 'content'
            return
        
        # Extract the keyword
        space_index = remaining_content.find(' ')
        if space_index == -1:
            # No space - the entire string might be a keyword
            potential_keyword = remaining_content
            self.content = ""
        else:
            potential_keyword = remaining_content[:space_index]
            self.content = remaining_content[space_index+1:]
        
        # Check if it's a valid keyword
        if potential_keyword in CONTENT_KEYWORDS or potential_keyword in COMMAND_KEYWORDS:
            self.keyword = potential_keyword
        else:
            # Not a keyword, treat as plain text
            self.keyword = "PLAIN"
            self.content = remaining_content
            
        self.keyword_type = 'content' if self.keyword in CONTENT_KEYWORDS else 'command'
    
    def should_wait_for_input(self):
        """
        Check if this element should wait for user input after displaying.
        
        Returns:
            True if the element should wait for input, False otherwise
        """
        return '>' not in self.modifiers


class InputLine:
    """
    Represents a line from the input file.
    """
    
    def __init__(self, line_num, raw_content):
        """
        Initialize a new InputLine from raw text.
        
        Args:
            line_num: Line number in the source file
            raw_content: Raw text content from the input file
        """
        self.line_num = line_num
        self.raw_content = raw_content[:]
        
        # Split by semicolons
        self.raw_input_elements = raw_content.split(';')
        self.input_elements = [InputElement(elem) for elem in self.raw_input_elements]
        
        # Import element classes here to avoid circular imports
        from elements.text import TitleElement, PlainTextElement, BulletElement, DefinitionElement, TermElement
        from elements.media import ImageElement
        
        # Convert input elements to output elements
        self.output_elements = []
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
            elif elem.keyword == "TERM":
                self.output_elements.append(TermElement(elem))
    
    def is_content_line(self):
        """Check if this line contains content elements."""
        return bool(self.output_elements)
    
    def get_fade_out_actions(self):
        """Get animations to fade out all elements in this line."""
        result = []
        for elem in self.output_elements:
            result.extend(elem.get_fade_out_actions())
        return result
