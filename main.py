import ply.lex as lex
import ply.yacc as yacc
from grammatic import *
from interpreter import Interpreter

lexer = lex.lex()
parser = yacc.yacc()


code = open("code.c", "r", encoding='utf-8')


code_ast = parser.parse(code.read())
interpeter = Interpreter()
interpeter.interpret(code_ast)