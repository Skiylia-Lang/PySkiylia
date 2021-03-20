 #!/usr/bin/env python
"""Stores token definitions, may end up moving this elsewhere"""

tokens = [#single character tokens
            "LeftParenthesis", "RightParenthesis", "Colon", "Comma", "Dot", "Minus", "Plus", "Star", "Slash", "Greater", "Less", "Equal", "Ampersand", "Bar", "Bang",
            #single or double character Tokens
            #Literal tokens
            "String", "Number", "Identifier",
            #keyword tokens
            "Class", "Def", "Do", "Elif", "Else", "False", "For", "If", "Null", "Print", "Return", "Self", "Super", "True", "Var","When", "While",
            #miscellaneous
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
