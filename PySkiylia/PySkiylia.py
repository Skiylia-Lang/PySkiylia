 #!/usr/bin/env python
"""The initialisation file that everything will interact with"""
#Python modules required
import sys, os

#Our modules that are required
from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter
from Resolver import Resolver
from ASTPrinter import ASTPrinter

#Main function to be called when executed
class Skiylia:
    #set the default values here
    haderror = False
<<<<<<< HEAD
    version = "v0.7.1"
=======
    version = "v0.7.0"
>>>>>>> a0a18c5... update readme and include better integer handling
    title = ""
    debug = False
    #run this at initialisation
    def __init__(self, args=""):
        #check if the user has asked for help
        if args and args[-1] in ["--help", "-h", "-?", "/?"]:
            #show them the default usage
            print("Usage:\tPySkiylia [scriptname]")
            sys.exit(0)
        #or if they want to enable debug mode
        elif args and args[-1] in ["-debug", "-d"]:
            #enable debugging
            self.debug = True
            #ad remove the flag from the arguments list
            args = args[:-1]
            self.title += " (Debug mode)"
        #we won't support more than one argument
        if len(args) > 1:
            #tell the user and exit
            print("PySkiylia does not accept more than one argument")
            sys.exit(1)
        #if we have been given a single argument
        elif len(args) == 1:
            #save the argument if it is valid
            self.args = self.checkValidFile(args[0])
            self.title = " - " + self.args.split("/")[-1] + self.title
        else:
            #otherwise we have no argument to speak of
            self.title = " Interactive" + self.title
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
        print("PySkiylia",self.version,"- debugging mode"*self.debug)
        #keep looping the code
        while True:
            #fetch the user input
            line = input(">> ")
            #check they did not ask to quit
            if line.lower() in ["quit", "exit"]:
                break
            #make sure the user hasn't given a function (or otherwise) that requires multi-line
            if line.replace(" ", "")[-1] == ":":
                while True:
                    nextinput = input(" |")
                    line += "\n"+nextinput
                    if not nextinput:
                        break
            #else, try to run the code they provided
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
        lexer = Lexer(self, source)
        #and scan the sourcecode for tokens
        tokens = lexer.scanTokens()
        #Lexer output for debugging
        if self.debug:
            print("\nTokenised source code:")
            print(*["{} {},".format(token.type, token.indent) for token in tokens])

        #fetch the Parser class
        parser = Parser(self, tokens, lexer.primitives)
        #run the parser
        statements = parser.parse()
        #stop if we had an error
        if self.haderror:
            return
        #Parser output for debugging
        if self.debug:
            print("\nAbstracted source code:")
            astprinter = ASTPrinter()
            astprinter.display(statements)
            print()

        #initialise the interpreter
        interpreter = Interpreter(self, parser.arglimit)
        #initialise the resolver
        resolver = Resolver(self, interpreter, parser.arglimit)
        #run the resolver on the parsed code
        resolver.Resolve(statements)
        #double check the resolver did not find any errors
        if self.haderror:
            return
        #and finally run the parsed code
        interpreter.interpret(statements)

    #define a way of showing an error to the user
    def error(self, line=0, char=0, message="", where="", noloc=False):
        #check if we don't have a position to give to the user
        if noloc:
            #print the error in a lovely form
            print("{} Error: {}".format(where, message))
        else:
            #print the error in a lovely form
            print("[Line {0}, Char {1}] {2} Error: {3}".format(line, char, where, message))
        #update our internals to show we had an error
        self.haderror = True

#if we're being run directly (and not imported from somewhere else)
if __name__ == "__main__":
    #startup the script, fetching any arguments passed
    skiylia = Skiylia(sys.argv[1:])
    #set the window title
    os.system("title PySkiylia {}{}".format(skiylia.version, skiylia.title))
    #start running the interpreter
    skiylia.init()
