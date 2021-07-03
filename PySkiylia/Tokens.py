 #!/usr/bin/env python
"""Stores token definitions, may end up moving this elsewhere"""

tokens = [#single character tokens
            "LeftParenthesis", "RightParenthesis", "LeftSquareBrace", "RightSquareBrace", "Colon", "Comma", "Dot", "Slash", "And", "Or", "Xor",
            #single or double character Tokens
            "NFuzequal", "NEEqual", "NEqual", "Not", "Fuzequal", "EEEqual", "EEqual", "Equal",
            "Greater", "EGreater", "Less", "ELess", "Question", "QColon", "QQuestion",
            "Star", "StStar", "Minus", "MMinus", "Plus", "PPlus",
            #Literal tokens
            "String", "Number", "Identifier",
            #miscellaneous
            "EOF", "End"]

#a dictionary mapping keywords to their equivalent tokens
keywords = {"and":"And", "break":"Break", "continue":"Continue", "class":"Class", "def":"Def", "do":"Do", "elif":"Elif", "else":"Else",
            "false":"False", "for":"For", "if":"If", "import":"Import", "in":"In", "not":"Not", "null":"Null", "or":"Or",
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
