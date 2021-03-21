 #!/usr/bin/env python
"""Generates a sequence of tokens from plaintext"""

#import our code
from Expr import *

#define the Interpreter class
class Interpreter:
    ##initialise
    def __init__(self):
        #fetch the Skiylia class so we have access to it's functions
        from PySkiylia import Skiylia
        self.skiylia = Skiylia()
