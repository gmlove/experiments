tokens = ('NAME', 'NUMBER', )
literals = '+-*/'

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

precedence = (('left', '+', '-'), ('left', '*', '/'), )

def p_statement_expr(t):
    """statement : expression"""
    print(t[1])

def p_expression_binop(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
    """
    if p[2] == '+': p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def test_lex_yacc():
    import ply.lex as lex
    import ply.yacc as yacc
    lexer = lex.lex()
    parser = yacc.yacc()

    while True:
        try:
            s = input('calc > ')
            lexer.input(s)
            while True:
                tok = lexer.token()
                if not tok:
                    break
                print(tok)
            parser.parse(s, lexer=lexer)
        except EOFError:
            break


if __name__ == '__main__':
    test_lex_yacc()
