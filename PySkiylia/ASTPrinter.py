#!/usr/bin/env python
"""Coverts an AST to a printable output"""

#import our code
from AbstractSyntax import *
from Tokens import Token

#class that converts AST nodes to their corresponding functions
class Evaluator:
    #define a way of sending the interpreter to the correct method
    def evaluate(self, abstract):
        #print(abstract)
        ##List of all supported expressions and statements
        abstracts = {"Assign":self.AssignExpr,
                     "Block": self.BlockStmt,
                     "Binary": self.BinaryExpr,
                     "Call": self.CallExpr,
                     "Check": self.CheckStmt,
                     "Class": self.ClassStmt,
                     "Conditional": self.ConditionalStmt,
                     "Do": self.DoStmt,
                     "Expression": self.ExpressionStmt,
                     "Function": self.FunctionStmt,
                     "Get": self.GetExpr,
                     "Grouping": self.GroupingExpr,
                     "If": self.IfStmt,
                     "Import": self.ImportStmt,
                     "Interupt": self.Interuptstmt,
                     "Logical": self.LogicalExpr,
                     "Literal": self.LiteralExpr,
                     "Return": self.ReturnStmt,
                     "Self": self.SelfExpr,
                     "Set": self.SetExpr,
                     "Super": self.SuperExpr,
                     "Unary": self.UnaryExpr,
                     "Until":self.UntilStmt,
                     "Var":self.VarStmt,
                     "Variable": self.VarExpr,
                     "While":self.WhileStmt,}
        #fetch the class name of the abstract provided
        abstractName = abstract.__class__.__name__
        #return the correct method and pass in own value
        return abstracts[abstractName](abstract)

#define the ASTprint class
class ASTPrinter(Evaluator):
    def display(self, Abstractions):
        for x in Abstractions:
            print(self.evaluate(x))

    def AssignExpr(self, expr):
        return self.toparenthesis("=", expr.name.lexeme, expr.value)

    def BinaryExpr(self, expr):
        return self.toparenthesis(expr.operator.lexeme, expr.left, expr.right)

    def BlockStmt(self, stmt):
        return self.toparenthesis("block", stmt.statements)

    def CallExpr(self, expr):
        return self.toparenthesis("call", expr.callee, expr.arguments)

    def CheckStmt(self, stmt):
        return self.toparenthesis("check", stmt.condition, stmt.message)

    def ClassStmt(self, stmt):
        if stmt.superclass:
            return self.toparenthesis("class {}".format(stmt.name.lexeme), "superclass {}".format(stmt.superclass.name.lexeme), [x for x in stmt.methods])
        return self.toparenthesis("class {}".format(stmt.name.lexeme), [x for x in stmt.methods])

    def ConditionalStmt(self, stmt):
        if stmt.type=="T":
            return self.toparenthesis("conditional", stmt.condition, stmt.thenBranch, stmt.elseBranch)
        elif stmt.type=="E":
            return self.toparenthesis("conditional-elvis", stmt.condition, stmt.elseBranch)
        return self.toparenthesis("conditional-null", stmt.condition, stmt.elseBranch)

    def DoStmt(self, stmt):
        return self.toparenthesis("do", stmt.loop.body, self.evaluate(stmt.loop))

    def ExpressionStmt(self, stmt):
        return self.toparenthesis("",stmt.expression)

    def FunctionStmt(self, stmt):
        return self.toparenthesis("define {}".format(stmt.name.lexeme), stmt.params, stmt.body)

    def GetExpr(self, expr):
        return self.toparenthesis(".", expr.object, expr.name.lexeme)

    def GroupingExpr(self, expr):
        return self.toparenthesis("group", expr.expression)

    def IfStmt(self, stmt):
        if not stmt.elseBranch:
            return self.toparenthesis("if", stmt.condition, stmt.thenBranch)
        if not stmt.elseifs:
            return self.toparenthesis("if-else", stmt.condition, stmt.thenBranch, stmt.elseBranch)
        return self.toparenthesis("if-elif-else", stmt.condition, stmt.thenBranch, *stmt.elseifs, stmt.elseBranch)

    def ImportStmt(self, stmt):
        return self.toparenthesis("import", stmt.name.lexeme)

    def Interuptstmt(self, stmt):
        return self.toparenthesis(stmt.keyword.lexeme)

    def LiteralExpr(self, expr):
        if expr.value is None:
            return "null"
        return str(expr.value)

    def LogicalExpr(self, expr):
        return self.toparenthesis(expr.operator.lexeme, expr.left, expr.right)

    def ReturnStmt(self, stmt):
        return self.toparenthesis("return", stmt.value)

    def SelfExpr(self, expr):
        return "self"

    def SetExpr(self, expr):
        return self.toparenthesis("=", expr.object, expr.name.lexeme, expr.value)

    def SuperExpr(self, expr):
        return self.toparenthesis("super", expr.method)

    def UnaryExpr(self, expr):
        if expr.postfix:
            return self.toparenthesis(expr.right, expr.operator.lexeme)
        return self.toparenthesis(expr.operator.lexeme, expr.right)

    def UntilStmt(self, stmt):
        return self.toparenthesis("until", stmt.condition, stmt.body)

    def VarStmt(self, stmt):
        if stmt.initial in [None, 0.0]:
            return self.toparenthesis("var", stmt.name)
        return self.toparenthesis("var", stmt.name, "=", stmt.initial)

    def VarExpr(self, expr):
        return expr.name.lexeme

    def WhileStmt(self, stmt):
        return self.toparenthesis("while", stmt.condition, stmt.body)

    def toparenthesis(self, *args):
        return "("+self.transform(*args)+")"

    def transform(self, *parts):
        out=[]
        for part in parts:
            if isinstance(part, Expr):
                out.append(self.evaluate(part))
            elif isinstance(part, Stmt):
                out.append(self.evaluate(part))
            elif isinstance(part, Token):
                out.append(part.lexeme)
            elif isinstance(part, list):
                out.append(self.transform(*part))
            else:
                out.append(part)
        return " ".join([str(x) for x in out])
