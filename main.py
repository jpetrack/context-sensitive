# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 23:14:25 2016

@author: josh
"""

import Parser
import Translator
import sys

def render(filename):
    sys.setrecursionlimit(10000)
    f = open(filename, 'r')
    text = f.read()
    AST = Parser.parse(text)
    Translator.translate(AST)

if __name__ == "__main__":
    render(sys.argv[1])