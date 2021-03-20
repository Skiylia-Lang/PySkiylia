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
            #append the token to our list of tokens, provided we recieved one
            if token:
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
        elif c == ":":
            return self.addToken("Colon")
        elif c == ",":
            return self.addToken("Comma")
        elif c == ".":
            return self.addToken("Dot")
        elif c == "-":
            return self.addToken("Minus")
        elif c == "+":
            return self.addToken("Plus")
        elif c == "*":
            return self.addToken("Star")
        elif c == "/":
            #as division and comments use the same character, check if the next is a comment
            if self.match("/"):
                #keep advancing until we find a newline
                while self.match("\n", peek=True):
                    self.advance()
            else:
                return self.addToken("Slash")
        elif c == ">":
            return self.addToken("Greater")
        elif c == "<":
            return self.addToken("Less")
        elif c == "=":
            return self.addToken("Equal")
        elif c == "&":
            return self.addToken("Ampersand")
        elif c == "|":
            return self.addToken("Bar")
        elif c == "!":
            return self.addToken("Bang")
        elif c == "\n":
            #increment the line counter when we reach a newline
            self.line += 1
        elif c == '"':
            #if we have a string identifier
            return self.findString()
        else:
            #check if we have a number to parse
            if self.isDigit(c):
                #return the number to be found
                return self.findNumber()
            #check if we have any keywords
            elif self.isAlpha(c):
                return self.findIdentifier()
            else:
                #if nothing matches, throw an error
                self.skiylia.error(self.line, self.current, "Unexpected character")

    #define a way of fetching keyword identifiers
    def findIdentifier(self):
        #keep looping through sourcecode while there is an alphanumeric character to be found
        while self.isAlphaNumeric(self.peek()):
            self.advance()
        #fetch the identifier text
        thisIdentifier = self.source[self.start:self.current]
        #check if it is a keyword first
        if thisIdentifier in Tokens.keywords:

            return self.addToken(Tokens.keywords[thisIdentifier])
        #if nothing else, return a standard identifier
        return self.addToken("Identifier")

    #define a way of fetching a string from sourcecode
    def findString(self):
        #keep going until we hit the end of the code, or the string terminator
        while not self.match('"', peek=True):
            #we support multi-line strings, so if we find a newline, increment the line counter
            if self.match("\n", peek=True):
                self.line+=1
            #increment the lexer position
            self.advance()
        #if we havent seen the end of the string, raise an error
        if self.atEnd():
            self.skiylia.error(self.line, self.current, "Unterminated string")
        #consume the string closure identifier
        self.advance()
        #fetch the contents of the string, removing the leading and trailing identifiers
        stringVal = self.source[self.start+1:self.current-1]
        #create the token and return it
        return self.addToken("String", stringVal)

    #define a way of fetching a number from sourcecode
    def findNumber(self):
        #keep going untile we encounter something that isn't a digit
        while self.isDigit(self.peek()):
            #advance to the next character
            self.advance()

        #check if we have a decimal point in the middle
        if self.match(".", peek=True) and self.isDigit(self.peekNext()):
            #consume the decimal point
            self.advance()
                #keep going untile we encounter something that isn't a digit
            while self.isDigit(self.peek()):
                #advance to the next character
                self.advance()
        #create a numeric token and return. all numbers are float natively I guess
        return self.addToken("Number", float(self.source[self.start:self.current]))

    #define a way of checking if the value is a digit
    def isDigit(self, char):
        #I realise i could just use the python isdigit, but this allows any 'digit' including squared symbol. Maybe later?
        return "0" <= char <= "9"

    #define a way of checking if the value is a digit
    def isAlpha(self, char):
        #check if it is an alphabetical character or an underline
        return ("a" <= char.lower() <= "z") or (char == "_")

    #define a way of checking if the value is a digit
    def isAlphaNumeric(self, char):
        #check if it is an alphabetical character or an underline
        return ("0" <= char <= "9") or ("a" <= char.lower() <= "z") or (char == "_")

    #create a token
    def addToken(self, tokenType, literal=None):
        #return the text from the sourcecode (characters between the start and current position)
        text = self.source[self.start:self.current]
        #create and return a token
        return Tokens.Token(tokenType, text, literal, self.line, self.start)

    #advance through the source code if the current character matches what we would expect it to be
    def match(self, expected="", peek=False):
        #if we're at the end of the file, we'll want to return false
        if self.atEnd():
            return False
        #if the character is not the expected one, return false
        if self.source[self.current] != expected:
            return False
        #if we are only peeking, don't increment the position
        if not peek:
            #otherwise, we want to consume the token
            self.current+=1
        return True

    #return the current character without advancing
    def peek(self):
        #if we're at the end, return an eof
        if self.atEnd():
            return '\0'
        #otherwise return the character
        return self.source[self.current]

    #return the next character without advancing
    def peekNext(self):
        #if we're at the end, or about to be, return an eof
        if len(self.source) <= self.current+1:
            return '\0'
        #otherwise return the character
        return self.source[self.current+1]

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
