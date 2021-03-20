 #!/usr/bin/env python
"""Generates usable code from our tokens"""
#The gramar of Skiylia is encoded in the Parser Class

#import our code
import Tokens

#define the parser class
class Parser:
    #initialise
    def __init__(self):
        #set our parser position to zero
        self.current = 0
        #set the output list to empty
        self.final = []

    #define the expression grammar
    def expression(self):
        return self.equality()
