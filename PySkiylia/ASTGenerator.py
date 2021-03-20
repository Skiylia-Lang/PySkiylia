#!/usr/bin/env python
"""Generates an Abstract Syntax Tree (I hope)"""

#Import base python
import sys, os

ExprDict = {"Binary":"left, operator, right",
            "Grouping":"expression",
            "Literal":"value",
            "Unary":"operator, right"}

#create the class for the AST generator
class ASTGen:
    def __init__(self, args):
        #check we have exactly one argument
        if len(args) != 1:
            #show a usage error if we haven't
            print("Usage:\tASTGenerator.py <output dir>")
            sys.exit(1)
        #if the user asked for help
        if args[0] in ["--help", "-h", "-?", "/?"]:
            #show them the default usage
            print("Usage:\tASTGenerator.py <output dir>")
            #exit cleanly
            sys.exit(0)
        #otherwise, save the directory provided
        self.dir = args[0]

    #run this to start generating the AST
    def init(self):
        self.defineAST("Expr", ExprDict)

    #Actual do the AST definitions
    def defineAST(self, baseName, baseDict):
        #ensure baseName is a string
        baseName = str(baseName)
        #find the path of the file to write
        path = self.dir + "/" + baseName + ".py"

        #define each of the classes
        toWrite = ["class " + baseName +":",
                      "\tpass"]
        #And the children of that class
        for x in ExprDict:
            #fetch this child name
            className, args = x, ExprDict[x]
            #write all the code
            toWrite.append("class "+className+"("+baseName+"):")
            toWrite.append("\tdef __init__(self, "+args+"):")
            #apply __init__ arguments
            for y in (ExprDict[x]).split(","):
                toWrite.append("\t\tself."+y+" = "+y)

        #open the file
        with open(path, "w") as f:
            #write to file
            f.writelines(self.listToLines(toWrite))

    #define a way of inserting newlines between each list index, as writelines doesn't do what I expected
    def listToLines(self, lines):
        #loop through all lines
        for line in lines:
            #yield the current line
            yield line
            #yield a newline
            yield '\n'

if __name__ == "__main__":
    #startup the script, fetching any arguments passed
    astGen = ASTGen(sys.argv[1:])
    #start running the interpreter
    astGen.init()
