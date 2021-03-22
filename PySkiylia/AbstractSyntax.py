#!/usr/bin/env python
"""Stores the abstracted syntax for Skiylia"""

class Expr:
	pass

class Assign(Expr):
	def __init__(self, name,value):
		self.name = name
		self.value = value

class Binary(Expr):
	def __init__(self, left,operator,right):
		self.left = left
		self.operator = operator
		self.right = right

class Call(Expr):
	def __init__(self, callee,parenthesis,arguments):
		self.callee = callee
		self.parenthesis = parenthesis
		self.arguments = arguments

class Grouping(Expr):
	def __init__(self, expression):
		self.expression = expression

class Logical(Expr):
	def __init__(self, left,operator,right):
		self.left = left
		self.operator = operator
		self.right = right

class Literal(Expr):
	def __init__(self, value):
		self.value = value

class Unary(Expr):
	def __init__(self, operator,right):
		self.operator = operator
		self.right = right

class Variable(Expr):
	def __init__(self, name):
		self.name = name

class Stmt:
	pass

class Block(Stmt):
	def __init__(self, statements):
		self.statements = statements

class Expression(Stmt):
	def __init__(self, expression):
		self.expression = expression

class Function(Stmt):
	def __init__(self, name,params,body):
		self.name = name
		self.params = params
		self.body = body

class If(Stmt):
	def __init__(self, condition,thenBranch,elseBranch):
		self.condition = condition
		self.thenBranch = thenBranch
		self.elseBranch = elseBranch

class Var(Stmt):
	def __init__(self, name,initial):
		self.name = name
		self.initial = initial

class While(Stmt):
	def __init__(self, condition,body):
		self.condition = condition
		self.body = body
