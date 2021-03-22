#!/usr/bin/env python
"""Coverts an AST to a printable output"""

#import our code
from AbstractSyntax import *
from Tokens import Token

#define the ASTprint class
class ASTPrinter:
    def display(self, Abstractions):
        for x in Abstractions:
            print(self.evaluate(x))

    def AssignExpr(self, expr):
        return self.toparenthesis("=", expr.name.lexeme, expr.value)

    def BinaryExpr(self, expr):
        return self.toparenthesis(expr.operator.lexeme, expr.left, expr.right)

    def BlockStmt(self, stmt):
        return self.toparenthesis("block", stmt.statements)

    def ExpressionStmt(self, stmt):
        return self.toparenthesis("",stmt.expression)

    def GroupingExpr(self, expr):
        return self.toparenthesis("group", expr.expression)

    def IfStmt(self, stmt):
        if stmt.elseBranch == None:
            return self.toparenthesis("if", stmt.condition, stmt.thenBranch)
        return self.toparenthesis("if-else", stmt.condition, stmt.thenBranch, stmt.elseBranch)

    def LiteralExpr(self, expr):
        if expr.value == None:
            return "null"
        return str(expr.value)

    def LogicalExpr(self, expr):
        return self.toparenthesis(expr.operator.lexeme, expr.left, expr.right)

    def PrintStmt(self, stmt):
        return self.toparenthesis("print",stmt.expression)

    def UnaryExpr(self, expr):
        return self.toparenthesis(expr.operator.lexeme, expr.right)

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

    def evaluate(self, Abstraction):
        absts = {"Assign":self.AssignExpr,
                "Binary": self.BinaryExpr,
                "Block": self.BlockStmt,
                "Expression": self.ExpressionStmt,
                "Grouping": self.GroupingExpr,
                "If": self.IfStmt,
                "Literal": self.LiteralExpr,
                "Logical": self.LogicalExpr,
                "Print": self.PrintStmt,
                "Unary": self.UnaryExpr,
                "Var":self.VarStmt,
                "Variable": self.VarExpr,
                "While":self.WhileStmt,}
        abstName = Abstraction.__class__.__name__
        return absts[abstName](Abstraction)
