# Try to port python grammar to ply syntax, not finished yet. Maybe we could use a compiler to do this translation?


reserved = {
   'def': 'DEF',
   'if': 'IF',
   'then': 'THEN',
   'else': 'ELSE',
   'while': 'WHILE',
   'for': 'FOR',
   'lambda': 'LAMBDA',
   'is': 'IS',
   'or': 'OR',
   'and': 'AND',
    'await': 'AWAIT'
}


tokens = [
    'NAME', 'TYPE_POINTER', 'COMMENT', 'DOUBLE_STAR', 'EQ', 'NEQ', 'NEQ_1', 'GTE', 'LTE', 'SHIFT_RIGHT', 'SHIFT_LEFT', 'DIVIDE_INT'
] + list(reserved.values())


def t_COMMENT(t):
    r"""\#.*"""
    pass


def t_NAME(t):
    r"""[a-zA-Z_][a-zA-Z0-9_]*"""
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_DOUBLE_STAR(t):
    r"""\*\*"""
    return t


def t_TYPE_POINTER(t):
    r"""->"""
    return t


def t_EQ(t):
    r"""=="""
    return t


def t_NEQ(t):
    r"""\!="""
    return t


def t_NEQ_1(t):
    r"""<>"""
    return t


def t_LTE(t):
    r"""<="""
    return t


def t_GTE(t):
    r""">="""
    return t


def t_SHIFT_LEFT(t):
    r"""<<"""
    return t


def t_SHIFT_RIGHT(t):
    r""">>"""
    return t


def t_DIVIDE_INT(t):
    r"""//"""
    return t


literals = ",:()[]*|^&+-@%/~"
t_ignore = ' \t\n'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex
lexer = lex.lex()


def p_statement_expression(p):
    """
    statement : funcdef
    """
    print('p_statement_expression: {}'.format(p.slice))


def p_func_def_expression(p):
    """
    empty           :
    funcdef         : DEF NAME parameters ':'
                    | DEF NAME parameters TYPE_POINTER test ':'
    parameters      : '(' ')'
                    | '(' typedargslist ')'
    typedargslist   : tfpdef_withval_multi comma_
                    | tfpdef_withval_multi ',' '*' tfpdef comma_
                    | tfpdef_withval_multi ',' '*' tfpdef ',' DOUBLE_STAR tfpdef comma_
                    | tfpdef_withval_multi ',' '*' tfpdef ',' tfpdef_withval_multi
                    | tfpdef_withval_multi ',' '*' tfpdef ',' tfpdef_withval_multi DOUBLE_STAR tfpdef comma_
                    | tfpdef_withval_multi ',' DOUBLE_STAR tfpdef comma_
                    | '*' tfpdef comma_
                    | '*' tfpdef ',' DOUBLE_STAR tfpdef comma_
                    | '*' tfpdef ',' tfpdef_withval_multi
                    | '*' tfpdef ',' tfpdef_withval_multi DOUBLE_STAR tfpdef comma_
                    | DOUBLE_STAR tfpdef comma_
    comma_          : ','
                    | empty
    tfpdef          : NAME
                    | NAME ':' test
    tfpdef_withval   : tfpdef
                     | tfpdef '=' test
    tfpdef_withval_multi        : tfpdef_withval
                                | tfpdef_withval ',' tfpdef_withval
    varargslist     : vfpdef_withval_multi [',' [ '*' [vfpdef] (',' vfpdef ['=' test])* [',' ['**' vfpdef [',']]]
                    | vfpdef_withval_multi ',' '*' vfpdef comma_
                    | vfpdef_withval_multi ',' '*' vfpdef ',' vfpdef_withval_multi comma_
                    | vfpdef_withval_multi ',' '*' vfpdef ',' DOUBLE_STAR vfpdef comma_
                    | vfpdef_withval_multi ',' '*' vfpdef ',' vfpdef_withval_multi ',' DOUBLE_STAR vfpdef comma_
                    | '*' vfpdef comma_
                    | '*' vfpdef ',' vfpdef_withval_multi comma_
                    | '*' vfpdef ',' DOUBLE_STAR vfpdef comma_
                    | '*' vfpdef ',' vfpdef_withval_multi ',' DOUBLE_STAR vfpdef comma_
                    | DOUBLE_STAR vfpdef comma_
    vfpdef          : NAME
    vfpdef_withval  : vfpdef
                    | vfpdef '=' test
    vfpdef_withval_multi        : vfpdef_withval
                                | vfpdef_withval ',' vfpdef_withval


    test            : or_test
                    | or_test IF or_test ELSE test
                    | lambdef
    test_nocond     : or_test
                    | lambdef_nocond
    lambdef         : LAMBDA ':' test
                    | LAMBDA varargslist ':' test
    lambdef_nocond  : LAMBDA ':' test_nocond
                    | LAMBDA [varargslist] ':' test_nocond
    or_test         : and_test
                    | and_test OR or_test
    and_test        : not_test
                    | not_test AND and_test
    not_test        : NOT not_test
                    | comparison
    comparison      : expr
                    | expr comp_op comparison
    comp_op         : '<' | '>' | EQ | GTE | LTE | NEQ | NEQ_1 | IN | NOT IN | IS | IS NOT
    star_expr       : '*' expr
    expr            : xor_expr
                    | xor_expr '|' expr
    xor_expr        : and_expr
                    | and_expr '^' xor_expr
    and_expr        : shift_expr
                    | shift_expr '&' and_expr
    shift_expr      : arith_expr
                    | arith_expr SHIFT_LEFT arith_expr
                    | arith_expr SHIFT_RIGHT arith_expr
    arith_expr      : term
                    | term '+' arith_expr
                    | term '-' arith_expr
    term            : factor
                    | factor '*' term
                    | factor '@' term
                    | factor '/' term
                    | factor '%' term
                    | factor DIVIDE_INT term
    factor          : power
                    | '+' factor
                    | '-' factor
                    | '~' factor
    power           : atom_expr
                    | atom_expr DOUBLE_STAR factor
    atom_expr       : ['await'] atom trailer*
    atom: ('(' [yield_expr|testlist_comp] ')' |
           '[' [testlist_comp] ']' |
           '{' [dictorsetmaker] '}' |
           NAME | NUMBER | STRING+ | '...' | 'None' | 'True' | 'False')
    testlist_comp: (test|star_expr) ( comp_for | (',' (test|star_expr))* [','] )
    trailer: '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME
    subscriptlist: subscript (',' subscript)* [',']
    subscript: test | [test] ':' [test] [sliceop]
    sliceop: ':' [test]
    exprlist: (expr|star_expr) (',' (expr|star_expr))* [',']
    testlist: test (',' test)* [',']
    dictorsetmaker: ( ((test ':' test | '**' expr)
                       (comp_for | (',' (test ':' test | '**' expr))* [','])) |
                      ((test | star_expr)
                       (comp_for | (',' (test | star_expr))* [','])) )


    yield_expr: 'yield' [yield_arg]
    yield_arg: 'from' test | testlist

    comp_iter: comp_for | comp_if
    sync_comp_for: 'for' exprlist 'in' or_test [comp_iter]
    comp_for: ['async'] sync_comp_for
    comp_if: 'if' test_nocond [comp_iter]
    """




def p_error(p):
    p_error()
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
    test_yacc()

