
tokens = (
    'NAME', 'TYPE_POINTER', 'TYPE_INT', 'DEF',
)


def t_DEF(t):
    r'def'
    return t


def t_TYPE_INT(t):
    r'int'
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


def t_TYPE_POINTER(t):
    r'->'
    return t


literals = ",:()"
t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex
lexer = lex.lex()


def p_statement_expression(p):
    """statement : func_def_expression"""
    print('p_statement_expression: {}'.format(p.slice))


def p_func_def_expression(p):
    """func_def_expression : DEF NAME '(' arg_list_expression ')' TYPE_POINTER type_expression ':'"""
    print('p_func_def_expression: {}'.format(p.slice))


def p_func_def_expression_1(p):
    """func_def_expression : DEF NAME '(' arg_list_expression ')' ':'"""
    print('p_func_def_expression_1: {}'.format(p.slice))


def p_func_def_expression_2(p):
    """func_def_expression : DEF NAME '(' ')' TYPE_POINTER type_expression ':'"""
    print('p_func_def_expression_2: {}'.format(p.slice))


def p_func_def_expression_3(p):
    """func_def_expression : DEF NAME '(' ')' ':'"""
    print('p_func_def_expression_3: {}'.format(p.slice))


def p_arg_list_expression(p):
    """arg_list_expression : NAME
                           | NAME ',' arg_list_expression"""
    print('p_arg_list_expression: {}'.format(p.slice))


def p_type_expression(p):
    '''type_expression : TYPE_INT'''
    print('type_expression: {}'.format(p.slice))


def p_error(p):
    print("Syntax error at '%s'" % p.value)


def test_lexer():
    data = 'def abc_1_b(a, b) -> int:'
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok.type, tok.value, tok.lineno, tok.lexpos)


import ply.yacc as yacc
yacc.yacc(debug=True)


def test_yacc():
    while True:
        try:
            s = input('calc > ')   # use input() on Python 3
        except EOFError:
            break
        yacc.parse(s)


if __name__ == '__main__':
    # test_lexer()
    test_yacc()
