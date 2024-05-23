import sys
from antlr4 import *

from PenMotion.definitions.PenVisitor import PenVisitor
from PenMotion.definitions.antlr.PenMotionLexer import PenMotionLexer
from PenMotion.definitions.antlr.PenMotionParser import PenMotionParser


#https://github.com/vLesio/logotoma/blob/master/main.py
#https://github.com/Isdre/PenMotion
#https://github.com/antlr/antlr4/blob/master/doc/python-target.md

def main(argv):
    print(argv)
    input_stream = FileStream(argv[1])
    lexer = PenMotionLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PenMotionParser(stream)
    tree = parser.program()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    else:
        vinterp = PenVisitor()
        vinterp.visit(tree)

if __name__ == '__main__':
    main(sys.argv)

#antlr4 -Dlanguage=Python3 .\PenMotion.g4 -visitor -o PenMotion/definitions/antlr