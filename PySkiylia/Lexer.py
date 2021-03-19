 #!/usr/bin/env python
"""Generates a sequence of tokens from plaintext"""
#Import our functions
import Tokens

#create the Lexer class
class Lexer:
    #the function to run at initialisation 
    def __init__(self, source):
        #fetch the Skiylia class so we have access to it's functions
        from PySkiylia import Skiylia
        self.skiylia = Skiylia()
        #initialise the Lexer
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.char = 1

    #create a method of scanning tokens
    def scanTokens(self):
        #empty token list
        tokens = []
        #while we are not at the end of the list, loop
        while not self.atEnd():
            #update the position of our lexer
            self.start = self.current
            #fetch the next token
            token = self.tokenFromChar()
            #append the token to our list of tokens
            tokens.append(token)
        #add an end of file token
        tokens.append(Tokens.Token("EOF", "", None, self.line+1, 0))
        return tokens

    #create the appropriate token given the character
    def tokenFromChar(self):
        #fetch the next character
        c = self.advance()
        #check if it is a single character we recognise
        if c == "(":
            return self.addToken("LeftParenthesis")
        elif c == ")":
            return self.addToken("RightParenthesis")
        else:
            #if nothing matches, throw an error
            self.skiylia.error(self.line, self.current, "Unexpected character")

    #create a token
    def addToken(self, tokenType, literal=None):
        #return the text from the sourcecode (characters between the start and current position)
        text = self.source[self.start:self.current]
        #create and return a token
        return Tokens.Token(tokenType, text, literal, self.line, self.start)

    #advance through the source code if the current character matches what we would expect it to be
    def match(self, expected=""):
        #if we're at the end of the file, we'll want to return false
        if self.atEnd():
            return False
        #if the character is not the expected one, return false
        if self.source[self.current] != expected:
            return False
        #otherwise, return true and increment the Lexer position
        self.current+=1
        return True

    #advance through the source code and return the character
    def advance(self):
        #increment the Lexer position
        self.current+=1
        #return the character we just skiped over
        return self.source[self.current-1]

    #check if we have reached the end of the source code
    def atEnd(self):
        #return if the current position s greater than the source length
        return self.current >= len(self.source)
