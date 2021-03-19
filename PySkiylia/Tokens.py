 #!/usr/bin/env python
"""Stores token definitions, may end up moving this elsewhere"""

tokens = ["LeftParenthesis", "RightParenthesis",

        "STRING",
        "PRINT",
        "EOF"]

class Token:
    def __init__(self, type, lexeme, literal, line, char):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.char = char

    def toString(self):
        return self.type + " " + self.lexeme + " " + self.literal
