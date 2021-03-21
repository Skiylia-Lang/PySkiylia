#!/usr/bin/env python
"""Stores the abstracted syntax for Skiylia"""

class Expr:
	pass

class Binary(Expr):
	def __init__(self, left,operator,right):
		self.left = left
		self.operator = operator
		self.right = right

class Grouping(Expr):
	def __init__(self, expression):
		self.expression = expression

class Literal(Expr):
	def __init__(self, value):
		self.value = value

class Unary(Expr):
	def __init__(self, operator,right):
		self.operator = operator
		self.right = right

class Stmt:
	pass

class Binary(Stmt):
	def __init__(self, left,operator,right):
		self.left = left
		self.operator = operator
		self.right = right

class Grouping(Stmt):
	def __init__(self, expression):
		self.expression = expression

class Literal(Stmt):
	def __init__(self, value):
		self.value = value

class Unary(Stmt):
	def __init__(self, operator,right):
		self.operator = operator
		self.right = right
