#!/usr/bin/env python
"""Generates the Abstract Syntax Tree Syntax file"""

#Import base python
import sys, os

ExprDict = {"Assign":"name,value",
            "Binary":"left,operator,right",
            "Call":"callee,parenthesis,arguments",
            "Grouping":"expression",
            "Logical":"left,operator,right",
            "Literal":"value",
            "Return":"keyword,value",
            "Unary":"operator,right",
            "Variable":"name"}

StmtDict = {"Block":"statements",
            "Expression":"expression",
            "Function": "name,params,body",
            "If":"condition,thenBranch,elseBranch",
            "Var":"name,initial",
            "While":"condition,body"}

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
        self.dir = args[0] + "/" + "AbstractSyntax" + ".py"

    #run this to start generating the AST
    def init(self):
        try:
            #try to remove any old versions of the Abstract Syntax
            os.remove(self.dir)
        except OSError:
            pass
        with open(self.dir, "a") as f:
            f.write('#!/usr/bin/env python\n"""Stores the abstracted syntax for Skiylia"""\n')
        self.defineAST("Expr", ExprDict)
        self.defineAST("Stmt", StmtDict)

    #Actual do the AST definitions
    def defineAST(self, baseName, baseDict):
        #ensure baseName is a string
        baseName = str(baseName)

        #define each of the classes
        toWrite = ["class " + baseName +":",
                      "\tpass"]
        #And the children of that class
        for x in baseDict:
            #fetch this child name
            className, args = x, baseDict[x]
            #write all the code
            toWrite.append("class "+className+"("+baseName+"):")
            toWrite.append("\tdef __init__(self, "+args+"):")
            #apply __init__ arguments
            for y in (baseDict[x]).split(","):
                toWrite.append("\t\tself."+y+" = "+y)

        #open the file
        with open(self.dir, "a") as f:
            #write to file
            f.writelines(self.listToLines(toWrite))

    #define a way of inserting newlines between each list index, as writelines doesn't do what I expected
    def listToLines(self, lines):
        #loop through all lines
        for line in lines:
            if "class" in line:
                yield "\n"
            #yield the current line
            yield line
            #yield a newline
            yield "\n"

if __name__ == "__main__":
    #startup the script, fetching any arguments passed
    astGen = ASTGen(sys.argv[1:])
    #start running the interpreter
    astGen.init()
