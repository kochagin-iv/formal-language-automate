from constants import syntax_tree


def is_good_psp(regexp):
    cnt = 0
    for i in regexp:
        if i == '(':
            cnt += 1
        if i == ')':
            cnt -= 1
        if cnt < 0:
            return False
    if cnt != 0:
        return False
    return True


# priority 1 - () 2 - * 3 - . 4 - +


def make_syntax_tree(vertex):
    current_regexp = syntax_tree[vertex]
    if len(current_regexp) == 1:
        return
    # delete () from start and end of line
    while current_regexp[0] == '(' and current_regexp[-1] == ')' and is_good_psp(
            current_regexp[1:len(current_regexp) - 1]):
        current_regexp = current_regexp[1:len(current_regexp) - 1]
    syntax_tree[vertex] = current_regexp
    # find if string is (...)*
    if len(current_regexp) > 3 and current_regexp[0] == '(' and current_regexp[-2] == ')' and is_good_psp(
            current_regexp[1:len(current_regexp) - 2]) and current_regexp[-1] == '*':
        syntax_tree[vertex] = '*'
        syntax_tree[vertex * 2 + 1] = current_regexp[:len(current_regexp) - 1]
        make_syntax_tree(vertex * 2 + 1)
        return
    # find if string is x*
    if len(current_regexp) == 2 and current_regexp[-1] == '*':
        syntax_tree[vertex] = '*'
        syntax_tree[vertex * 2 + 1] = current_regexp[0]
        return
    # find + between )(
    part_to_left = ''
    part_to_right = current_regexp
    priority = 0
    for i in current_regexp:
        if i == '(':
            priority += 1
        if i == ')':
            priority -= 1
        if i == '+' and priority == 0:
            part_to_right = part_to_right[1:]
            syntax_tree[vertex * 2 + 1] = part_to_left
            syntax_tree[vertex * 2 + 2] = part_to_right
            make_syntax_tree(vertex * 2 + 1)
            make_syntax_tree(vertex * 2 + 2)
            syntax_tree[vertex] = '+'
            return
        part_to_left += i
        part_to_right = part_to_right[1:]
    # find . between )(
    part_to_left = ''
    part_to_right = current_regexp
    priority = 0
    for i in current_regexp:
        if i == '(':
            priority += 1
        if i == ')':
            priority -= 1
        if i == '.' and priority == 0:
            part_to_right = part_to_right[1:]
            syntax_tree[vertex * 2 + 1] = part_to_left
            syntax_tree[vertex * 2 + 2] = part_to_right
            make_syntax_tree(vertex * 2 + 1)
            make_syntax_tree(vertex * 2 + 2)
            syntax_tree[vertex] = '.'
            return
        part_to_left += i
        part_to_right = part_to_right[1:]