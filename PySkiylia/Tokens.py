 #!/usr/bin/env python
"""Stores token definitions, may end up moving this elsewhere"""

tokens = [#single character tokens
            "LeftParenthesis", "RightParenthesis", "Colon", "Comma", "Dot", "Minus", "Plus", "Slash", "Greater", "Less", "And", "Or", "Xor"
            #single or double character Tokens
            "NotEqual", "Not", "EqualEqual", "Equal", "Star", "StarStar"
            #Literal tokens
            "String", "Number", "Identifier",
            #keyword tokens
            "Class", "Def", "Do", "Elif", "Else", "False", "For", "If", "Null", "Return", "Self", "Super", "True", "Var", "Where", "While",
            #miscellaneous
            "EOF", "End"]

#a dictionary mapping keywords to their equivalent tokens
keywords = {"and":"And", "class":"Class", "def":"Def", "do":"Do", "elif":"Elif", "else":"Else",
            "false":"False", "for":"For", "if":"If", "not":"Not", "null":"Null", "or":"Or",
            "return":"Return", "self":"Self", "super":"Super", "true":"True", "var":"Var",
            "when":"Where", "where":"Where", "while":"While", "xor":"Xor",}

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
