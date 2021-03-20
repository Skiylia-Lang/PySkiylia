 #!/usr/bin/env python
"""The initialisation file that everything will interact with"""
#Python modules required
import sys, os

#Our modules that are required
from Lexer import Lexer
from Parser import Parser

#Main function to be called when executed
class Skiylia:
    #set the default values here
    haderror = False
    #run this at initialisation
    def __init__(self, args=""):
        #we won't support more than one argument
        if len(args) > 1:
            #tell the user and exit
            print("PySkiylia does not accept more than one argument")
            sys.exit(1)
        #if we have been given a single argument
        elif len(args) == 1:
            #check if te user has asked for help
            if args[0] in ["--help", "-h", "-?", "/?"]:
                #show them the default usage
                print("Usage:\tPySkiylia [scriptname]")
                sys.exit(0)
            #save the argument if it is valid
            self.args = self.checkValidFile(args[0])
        else:
            #otherwise we have no argument to speak of
            self.args = ""

    #run this to determine the runtype
    def init(self):
        #if we have been given an argument, run that
        if self.args:
            self.runFile(self.args)
        #else startup the interpreter without anything else
        else:
            self.runPrompt()

    #check if an argument given is a valid filetype
    def checkValidFile(self, path):
        #valid extensions for skiylia files
        extensions = [".skiy"]
        #check if any of them match the provided file
        for x in extensions:
            if path[-len(x):] == x:
                #if they do, return the filepath
                return path
        #otherwise, show an error
        print("Invalid filetype for skiylia")
        sys.exit(1)

    #startup the prompt if no arguments have been given
    def runPrompt(self):
        #print some base information
        Print("PySkiylia 0.0.1")
        #keep looping the code
        while True:
            #fetch the user input
            line = input(">> ")
            #try to run the code they just provided
            self.run(line)
            #reset the error flag, if it was set
            self.haderror = False

    #define a way to run an appropriate Skiylia file
    def runFile(self, fname):
        #check the path exists first
        if os.path.isfile(fname):
            #open the file
            with open(fname, "r") as f:
                #return the contents
                bytes = f.read()
            #and try to run the script
            self.run(bytes)
            #exit if we had an error
            if self.haderror:
                sys.exit(1)
        else:
            print("No such file:", fname)
            sys.exit(1)

    def run(self, source):
        #fetch the Lexer class
        lexer = Lexer(source)
        #and scan the sourcecode for tokens
        tokens = lexer.scanTokens()
        #fetch the Parser class
        parser = Parser(tokens)
        #run the parser
        expression = parser.parse()

        #stop if we had an error
        if self.haderror:
            return

        #for now, print the parser output
        print(expression)

    #define a way of showing an error to the user
    def error(self, line=0, char=0, message="", where=""):
        #print the error in a lovely form
        print("[Line {0}, Char {1}] {2} Error: {3}".format(line, char, where, message))
        #update our internals to show we had an error
        self.haderror = True

#if we're being run directly (and not imported from somewhere else)
if __name__ == "__main__":
    #startup the script, fetching any arguments passed
    skiylia = Skiylia(sys.argv[1:])
    #start running the interpreter
    skiylia.init()
