 #!/usr/bin/env python
"""Generates a sequence of tokens from plaintext"""
#Import our functions
import Tokens

#create the Lexer class
class Lexer:
    #the function to run at initialisation
    def __init__(self, skiylia, source, fetchprimitives=True):
        #return a method for accessing the skiylia class
        self.skiylia = skiylia
        #initialise the Lexer
        self.source = source
        #start pointer at zeroth character
        self.start = self.current = self.indent = 0
        #start at first character
        self.line = self.char = 1
        #start empty primitives
        if fetchprimitives:
            self.primitives = []
            self.fetchprimitives()

    #create tokens for primitives, so we do not have to search for a call
    def fetchprimitives(self):
        from SkiyliaCallable import SkiyliaCallable
        import Primitives
        #fetch all classes who are a subclass of SkiyliaCallable
        primitives = SkiyliaCallable.__subclasses__()
        #itterate through them
        for primitive in primitives:
            #if they are from the primitives module
            if primitive.__module__ == "Primitives":
                #fetch the call name
                callname = primitive.__name__
                #check if a custom one has been defined
                if primitive.callname:
                    callname=primitive.callname
                #add them to the token list
                Tokens.keywords[callname] = "Identifier"
                #and append to an internal primitives list
                self.primitives.append(callname)

    #create a method of scanning tokens
    def scanTokens(self):
        #empty token list
        self.tokens = []
        #while we are not at the end of the list, loop
        while not self.atEnd():
            #update the position of our lexer
            self.char += (self.current-self.start)
            self.start = self.current
            #fetch the next token
            token = self.tokenFromChar()
            #append the token to our list of tokens, provided we recieved one
            if token:
                #if the last token was an ending
                if self.checkPreviousToken("End"):
                    #fetch it
                    lt = self.previousToken()
                    #and check we haven't skipped an indentation
                    if token.indent<lt.indent-1:
                        #create a new ending token at the same position, but with one lower indentation
                        self.tokens.append(Tokens.Token("End", "", None, lt.line, lt.char, lt.indent - 1))
                #add the token
                self.tokens.append(token)
        #add an end token if none exists
        if not self.checkPreviousToken("End"):
            self.tokens.append(Tokens.Token("End", "", None, self.line, self.char+1, self.indent))
        #add an EOF token
        self.tokens.append(Tokens.Token("EOF", "", None, self.line, self.char+1, 0))
        #remove any leading end tokens
        while self.tokens[0].type == "End":
            self.tokens.pop(0)
        return self.tokens

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
            token = self.addToken("Colon")
            #indent after creating the token, ensures that the following block has the appropriate indentation
            self.indent += 1
            return token
        elif c == ",":
            return self.addToken("Comma")
        elif c == ".":
            return self.addToken("Dot")
        elif c == "-":
            if self.match("-"):
                return self.addToken("MMinus")
            return self.addToken("Minus")
        elif c == "+":
            if self.match("+"):
                return self.addToken("PPlus")
            return self.addToken("Plus")
        elif c == "*":
            if self.match("*"):
                return self.addToken("StStar")
            return self.addToken("Star")
        elif c == "/":
            #as division and comments use the same character, check if the next is a comment
            if self.match("/"):
                #as comments can mess with indentation, remove any leading up to it
                self.removewhitespace()
                #as multi-line comments are ///, whereas a single line is //, we need to check for that too!
                if self.match("/"):
                    #keep advancing until we find the tripple comment escape
                    self.advance(3)
                    while self.peeklast(3) != "///":
                        self.advance()
                else:
                    #keep advancing until we find a newline
                    while not self.match("\n", peek=True) and not self.atEnd():
                        self.advance()
            else:
                return self.addToken("Slash")
        elif c == ">":
            if self.match("="):
                return self.addToken("EGreater")
            return self.addToken("Greater")
        elif c == "<":
            if self.match("="):
                return self.addToken("ELess")
            return self.addToken("Less")
        elif c == "=":
            if self.match("="):
                if self.match("="):
                    return self.addToken("EEEqual")
                return self.addToken("EEqual")
            return self.addToken("Equal")
        elif c == "~" and self.match("~") and self.match("~"):
            return self.addToken("Fuzequal")
        elif c == "?":
            if self.match(":"):
                return self.addToken("QColon")
            elif self.match("?"):
                return self.addToken("QQuestion")
            #conditional question mark
            return self.addToken("Question")
        elif c == "&":
            #Check for logical and
            return self.addToken("And")
        elif c == "^":
            #Check for logical xor
            return self.addToken("Xor")
        elif c == "|":
            #Check for logical or
            return self.addToken("Or")
        elif c == "!":
            if self.match("="):
                if self.match("="):
                    return self.addToken("NEEqual")
                return self.addToken("NEqual")
            elif self.match("~") and self.match("~"):
                return self.addToken("NFuzequal")
            return self.addToken("Not")
        elif c == "\t":
            #if we met an indentation, then increment our indent tage
            self.indent += 1
        elif c == " ":
            #Two spaces are equivalent to and indent <- TEMPORARILY MIND YOU
            if self.match(" "):
                self.indent +=1
        elif c == '"':
            #if we have a string identifier
            return self.findString()
        elif c == "\n":
            #increment the line counter when we reach a newline
            self.line += 1
            self.char = 0
            tempindent = self.indent
            self.indent = 0
            #check we don't have a string of ending tokens
            if not self.checkPreviousToken("End"):
                #return the ending token (This will be useful for the parser, as it can identify if a line, and thus statement, has finished)
                return self.addToken("End", indent=tempindent)
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
                self.skiylia.error(self.line, self.char, "Unexpected character")

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
                self.char=1
            #increment the lexer position
            self.advance()
        #if we havent seen the end of the string, raise an error
        if self.atEnd():
            self.skiylia.error(self.line, self.char, "Unterminated string")
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
        #create a numeric token and return.
        return self.addToken("Number", self.source[self.start:self.current])

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
    def addToken(self, tokenType, literal=None, indent=""):
        #if we haven't been given an intentation, then fetch it from memory
        if not indent:
            indent = self.indent
        #return the text from the sourcecode (characters between the start and current position)
        text = self.source[self.start:self.current]
        #create and return a token
        return Tokens.Token(tokenType, text, literal, self.line, self.char, indent)

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

    #return the previous character(s) without advancing
    def peeklast(self, chars=1):
        return self.source[self.current-chars:self.current]

    #return the previous token
    def previousToken(self):
        #get the last token and test
        return self.tokens[-1]

    #return if the previous token was of an appropriate type
    def checkPreviousToken(self, tokentype):
        #if we don't have any tokens, this is false
        if len(self.tokens)==0:
            return False
        #if we don't have any tokens, this is false
        return self.previousToken().type == tokentype

    #advance through the source code and return the character
    def advance(self, chars=1):
        #increment the Lexer position
        self.current += chars
        #return the character we just skiped over
        return self.source[self.current-1]

    #check if we have reached the end of the source code
    def atEnd(self):
        #return if the current position s greater than the source length
        return self.current >= len(self.source)

    #match the indentation to any actual surrounding code
    def removewhitespace(self):
        #if we have a previous token
        if self.tokens:
            #then set our indent to that
            lt = self.previousToken()
            self.indent = lt.indent
            #unless it was a colon, then we have to indent further
            if lt.type == "Colon":
                self.indent += 1
