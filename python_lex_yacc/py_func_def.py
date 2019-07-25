
tokens = (
    'NAME', 'TYPE_POINTER', 'DEF', 'COMMENT'
)


def t_COMMENT(t):
    r"""\#.*"""
    pass


def t_DEF(t):
    r"""def"""
    return t


def t_NAME(t):
    r"""[a-zA-Z_][a-zA-Z0-9_]*"""
    return t


def t_TYPE_POINTER(t):
    r"""->"""
    return t


literals = ",:()[]*"
t_ignore = ' \t\n'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex
lexer = lex.lex()


def p_statement_expression(p):
    """
    statement : func_def_expression
    """
    print('p_statement_expression: {}'.format(p.slice))


def p_func_def_expression(p):
    """
    func_def_expression : DEF NAME '(' arg_list_expression ')' TYPE_POINTER type_expression ':'
                        | DEF NAME '(' arg_list_expression ')' ':'
                        | DEF NAME '(' ')' TYPE_POINTER type_expression ':'
                        | DEF NAME '(' ')' ':'
    """
    print('p_func_def_expression_3: {}'.format(p.slice))


def p_arg_list_expression(p):
    """
    arg_list_expression : NAME
                        | NAME ':' type_expression
                        | arg_list_expression ','
                        | arg_list_expression ',' arg_list_expression
    """
    print('p_arg_list_expression: {}'.format(p.slice))


def p_type_expression(p):
    """
    type_expression : NAME
                    | NAME '[' multi_type_expression ']'
    multi_type_expression : type_expression
                          | type_expression ',' multi_type_expression
    """
    print('type_expression: {}'.format(p.slice))


def p_error(p):
    raise Exception("Syntax error at '%s'" % p.value)


def test_lexer(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok.type, tok.value, tok.lineno, tok.lexpos)


import ply.yacc as yacc
yacc.yacc(debug=True)


def test_yacc():
    test_src = [
        'def abc(a,):',
        'def abc(a,):',
        'def abc(a,#xxx()[]\n):',
        'def abc(a: List[int],):',
        'def abc() -> int:',
        'def abc(a, b) -> List[int]:',
        'def abc(a, b: Union[int, List[float]],) -> Union[int, float]:',
        'def abc(a,) -> Union[int, List[float]]:',
        'def abc(a,) -> Union[int, List[float], float]:',
        'def abc(a,) #xxx()[]\n -> Union[int, List[float], float]:'
    ]
    for test_line in test_src:
        print('#####  test start for: {}'.format(test_line))
        test_lexer(test_line)
        yacc.parse(test_line)
        print('#####  test end for: {}\n'.format(test_line))


if __name__ == '__main__':
    # test_lexer()
    test_yacc()
