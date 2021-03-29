#!/usr/bin/env python
"""Defines the base data types of Skiylia"""

from SkiyliaCallable import *

#base dataType class
class SkiyliaDataType(SkiyliaClass):
    callname=""
    value=None
    def __init__(self, interpreter):
        super().__init__(self.callname, None, [])
        #fetch all of the attributes of this class
        classattr = [getattr(self, x) for x in dir(self)]
        #and fetch all of the attributes that are classes themselves
        if not self.methods:
            self.methods = dict([(x.callname, x(x, interpreter)) for x in classattr if isinstance(x, type)])
        #print(self.methods)

    class SkiyliaAdd(SkiyliaFunction):
        callname = "__add__"
        params = ["other"]

#integer class handling
class SkiyliaInt(SkiyliaDataType):
    arity = "0,1"
    callname = "int"
    name = "int"
    def __init__(self, value=None, interpreter=""):
        super().__init__(interpreter)
        if not value:
            self.value = 0
        else:
            if isinstance(value, list):
                self.value = value[0].split(".")[0]
            else:
                self.value = value.split(".")[0]

    def call(self, interpreter, arguments, token=""):
        self.value = SkiyliaInt(arguments[0].value).value
        instance = super().call(interpreter, arguments, token)
        #print(args)
        return instance

#float class handling
class SkiyliaFloat(SkiyliaDataType):
    arity = "0,1"
    callname = "float"
    name = "float"
    def call(self, interpreter, value=[], token=""):
        if "." not in value:
            value+=".0"
        self.value = value
        #print(self.methods)
        return self.value
