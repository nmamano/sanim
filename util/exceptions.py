"""
Custom exceptions for Sanim.
"""

class SanimParseError(Exception):
    """Exception raised for errors in parsing the input file."""
    pass


class SanimRenderError(Exception):
    """Exception raised for errors in rendering the presentation."""
    pass 
