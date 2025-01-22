import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'IDENTIFIER', 'FLOAT_NUMBER', 'INT_NUMBER', 
    'PLUS', 'MINUS', 'MULT', 'DIVIDE', 'ASSIGN',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON', 'COMMA',
    'INT', 'RETURN', 'WHILE', 'FLOAT', 'CHAR',
    'CHARACTER', 'IF', 'ELSE', 'EQUALS',
    'GREATER', 'LESS', 'PRINT'
)

t_ignore = ' \t'

keywords = {
    'int' : 'INT',
    'return': 'RETURN',
    'while': 'WHILE',
    'float': 'FLOAT',
    'char': 'CHAR',
    'if': 'IF',
    'else': 'ELSE',
    'printf': 'PRINT'
}

def t_FLOAT_NUMBER(t):
    r'\d+(\.\d+)+'
    t.value = float(t.value)
    return t

def t_INT_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHARACTER(t):
    r'\'[a-zA-Z0-9]\''
    t.value = t.value[1]
    return t

t_INT = r'int'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','
t_EQUALS = r'=='
t_GREATER = r'>'
t_LESS = r'<'
t_FLOAT = r'float'
t_CHAR = r'char'
t_RETURN = r'return'
t_WHILE = r'while'
t_IF = r'if'
t_ELSE = r'else'
t_PRINT = r'print'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in keywords:
        t.type = keywords[t.value]
    return t

def t_printf(t):
    r'printf'
    return t

lexer = lex.lex()


def p_program(p):
    '''program : function_list'''
    p[0] = ('program', p[1])

def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR '''
    p[0] = p[1]

def p_function(p):
    '''function : type IDENTIFIER LPAREN parameter_list RPAREN LBRACE statement_list return_statement RBRACE
                | type IDENTIFIER LPAREN RPAREN LBRACE statement_list return_statement RBRACE
                | type IDENTIFIER LPAREN RPAREN LBRACE return_statement RBRACE
                | type IDENTIFIER LPAREN parameter_list RPAREN LBRACE return_statement RBRACE'''
    if len(p) == 10:
        p[0] = ('function', p[1], p[2], p[4], p[7], p[8])
    elif len(p) == 8:
        p[0] = ('function', p[1], p[2], [], [], p[6])
    elif len(p) == 9 and p[5] == ')':
        p[0] = ('function', p[1], p[2], p[4], [], p[7])
    else:
        p[0] = ('function', p[1], p[2], [],  p[6], p[7])
    
    

def p_function_list(p):
    '''function_list : function
                     | function_list function'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : while_statement
                 | declaration_statement
                 | assignment_statement
                 | if_statement
                 | ifelse_statement
                 | print_statement
                 | declaration_assignment_statement'''
    p[0] = p[1]

def p_print_statemenet(p):
    '''print_statement : PRINT LPAREN expression RPAREN SEMICOLON
                       | PRINT LPAREN expression_text RPAREN SEMICOLON'''
    p[0] = ('print', p[3])

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''
    p[0] = ('return', p[2])

def p_while_statement(p):
    '''while_statement : WHILE LPAREN if_expression RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('while', p[3], p[6])

def p_declaration_statement(p):
    '''declaration_statement : type IDENTIFIER SEMICOLON'''
    p[0] = ('declare', p[1], p[2])

def p_declaration_assignment_statement(p):
    '''declaration_assignment_statement : type IDENTIFIER ASSIGN expression SEMICOLON'''
    p[0] = ('declare_and_assign', p[1], p[2], p[4])

def p_assignment_statement(p):
    '''assignment_statement : IDENTIFIER ASSIGN expression SEMICOLON
                            | IDENTIFIER ASSIGN expression_text SEMICOLON'''
    p[0] = ('assign', p[1], p[3])

def p_if_statement(p):
    '''if_statement : IF LPAREN if_expression RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('if', p[3], p[6])

def p_else_statement(p):
    '''else_statement : ELSE LBRACE statement_list RBRACE'''
    p[0] = ('else', p[3])

def p_ifelse_statemenmt(p):
    '''ifelse_statement : if_statement else_statement'''
    p[0] = (p[1], p[2])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement
                      | statement_list return_statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p__expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_func_expression(p):
    '''func_expression : IDENTIFIER LPAREN RPAREN
                       | IDENTIFIER LPAREN expression_list RPAREN'''
    if len(p) == 4:
        p[0] = p[1]
    else:
        p[0] = p[1], p[3]

def p_if_expression(p):
    '''if_expression : expression EQUALS expression
                     | expression GREATER expression
                     | expression LESS expression'''
    
    p[0] = (p[2], p[1], p[3])

def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIVIDE expression
                  | INT_NUMBER
                  | FLOAT_NUMBER
                  | IDENTIFIER'''
    if len(p) == 2:
        if isinstance(p[1], int):
            p[0] = ('int', p[1])
        elif isinstance(p[1], float):
            p[0] = ('float', p[1])
        else:
            p[0] = ('var', p[1])
    else:
        p[0] = (p[2], p[1], p[3])

def p_expression_text(p):
    '''expression_text : CHARACTER'''
    p[0] = ('char', p[1])

def p_expression_func(p):
    '''expression : func_expression'''
    p[0] = ('func_call', p[1])

def p_parameter(p):
    '''parameter : type IDENTIFIER'''
    p[0] = ('param', p[1], p[2])

def p_parameter_list(p):
    '''parameter_list : parameter
                      | parameter_list COMMA parameter'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' (line: {p.lineno})")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

code = """
int main(){
    int a = 3;
}
"""

if __name__ == '__main__':

    lexer.input(code)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    result = parser.parse(code)
    print(result)