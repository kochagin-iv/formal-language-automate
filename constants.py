# eps = $
reg = "(a.(a.b+b.(b.a)*.a)*)*"
regex = "(a(ab|b(ba)*a)*)*"  # reg in correct for python format

make_addition_regular = 0
specsymbols = '().*+'
alphabet = ""
syntax_tree = [None] * 1000
nka = [None] * 1000
syntax_tree[0] = reg
max_length_testing = 10
