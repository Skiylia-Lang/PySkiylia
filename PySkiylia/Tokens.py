 #!/usr/bin/env python
"""Stores token definitions, may end up moving this elsewhere"""

tokens = [#single character tokens
            "LeftParenthesis", "RightParenthesis", "Colon", "Comma", "Dot", "Minus", "Plus", "Star", "Slash", "Greater", "Less",
            #single or double character Tokens
            "NotEqual", "Not", "EqualEqual", "Equal", "And", "Xor", "Or",
            #Literal tokens
            "String", "Number", "Identifier",
            #keyword tokens
            "Class", "Def", "Do", "Elif", "Else", "False", "For", "If", "Null", "Return", "Self", "Super", "True", "Var","When", "While",
            #miscellaneous
            "EOF", "End"]

#a dictionary mapping keywords to their equivalent tokens
keywords = {"class":"Class", "def":"Def", "do":"Do", "elif":"Elif", "else":"Else",
            "false":"False", "for":"For", "if":"If", "null":"Null",
            "return":"Return", "self":"Self", "super":"Super", "true":"True", "var":"Var",
            "when":"When", "while":"While",}

class Token:
    def __init__(self, type, lexeme, literal, line, char, indent):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.char = char
        self.indent = indent

    def toString(self):
        return self.type + " " + self.lexeme + " " + self.literal
