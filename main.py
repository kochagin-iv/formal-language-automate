# eps = $
# reg = "a.b*+b.a"
# reg = "a.b"
# reg = "a.(a.b+b.a)*.b.(a+b.a)*"
# reg = "(a+b)*.(a.a.(a+b)*.b.b+a.b.a).b*.a.b*"
# reg = "a.b"
from constants import reg, make_addition_regular, alphabet, specsymbols, syntax_tree, nka
# reg = "a.(a.(a.b)*.b)*+b.a"

import re

from make_dka import make_dka, make_array_edges_dka, add_edges_dka
from make_mpdka import make_mpdka, get_array_edges_mpdka, find_end_start_vertex_mpdka
from make_nka import nka_vertex, make_nka, delete_eps_edge_nka, from_array_edges_to_vector_vertex, find_delete_vertex, \
    make_correct_array_edges_end_vertex_vec_vertex_after_delete
from make_pdka import get_vertex_pdka, check_if_addition_regular
from make_syntax_tree import make_syntax_tree


for i in reg:
    if not (i in specsymbols) and not (i in alphabet) and i != '$':
        alphabet += i
make_syntax_tree(0)

for i in range(1000):
    nka[i] = nka_vertex()

make_nka(0, alphabet)

#print(nka[0].get_start_vertex())
#print(nka[0].get_end_vertex())

array_edges, end_vertex_nka = delete_eps_edge_nka(nka, alphabet)

used = []

vector_vertex = from_array_edges_to_vector_vertex(array_edges)
used = find_delete_vertex(nka[0].get_start_vertex(), used, vector_vertex)
array_edges, used, end_vertex_nka = make_correct_array_edges_end_vertex_vec_vertex_after_delete(array_edges, used, end_vertex_nka)

vertex_in_dka, start_vertex_dka, end_vertex_dka = make_dka(nka, alphabet, array_edges)
print('Vertex in dka and relevant vertex in nka - 1st element in each array, next elements - transition by letters in '
      'alphabet')
print(vertex_in_dka)
print('Start dka vertex')
print(start_vertex_dka)
print('End dka vertex')
print(end_vertex_dka)
array_edges_dka = make_array_edges_dka(vertex_in_dka, alphabet)
array_edges_dka = add_edges_dka(array_edges_dka, alphabet)

array_edges_pdka = array_edges_dka
start_vertex_pdka = start_vertex_dka
end_vertex_pdka = end_vertex_dka
print('Array edges in pdka')
print(array_edges_pdka)
vertex_in_pdka = get_vertex_pdka(array_edges_pdka)
end_vertex_pdka = check_if_addition_regular(vertex_in_pdka, end_vertex_pdka)


# make mpdka
compression = make_mpdka(vertex_in_pdka, end_vertex_pdka, alphabet, array_edges_pdka)
print('Dict - each vertex of the mpdka is associated with a set of vertices of the pdka')
print(compression)

array_edges_mpdka = get_array_edges_mpdka(compression, array_edges_pdka)

print('Len of array edges in mpdka')
print(len(array_edges_mpdka))
print('Array edges in mpdka')
print(array_edges_mpdka)

start_vertex_mpdka, end_vertex_mpdka = find_end_start_vertex_mpdka(compression, start_vertex_pdka, end_vertex_pdka)
print('Start vertex in mpdka is:', start_vertex_mpdka)
print('End vertex in mpdka is:', end_vertex_mpdka)

'''max_v = max(cur_condition)
r = [[[''] * max_v] * max_v] * max_v
for i in range(max_v):
    for j in range(max_v):
        cur_r = ''
        if i != j:
            for edge in array_edges_mpdka:
                if edge[0] == i and edge[1] == j:
                    cur_r += edge[2]
                    cur_r += '+'
            if len(cur_r) > 0 and cur_r[-1] == '+':
                cur_r = cur_r[:len(cur_r) - 1]
            r[i][j][0] = cur_r
            continue
        if i == j:
            for edge in array_edges_mpdka:
                if edge[0] == i and edge[1] == j:
                    cur_r += edge[2]
                    cur_r += '+'
            if len(cur_r) > 0 and cur_r[-1] == '+':
                cur_r = cur_r[:len(cur_r) - 1]
            r[i][j][0] = cur_r + '+' + '$'
            continue

for i in range(max_v):
    for j in range(max_v):
        for k in range(1, max_v):
            r1 = r[i][j][k - 1]
            r2 = '.(' + r[k][k][k - 1] + ')' + '*'
            r3 = '.' + r[k][j][k - 1]
            r4 = '+' + r[i][j][k - 1]
            if len(r1) > 0:
                r[i][j][k] += r1
            if len(r2) > 4:
                r[i][j][k] += r2
            if len(r3) > 1:
                r[i][j][k] += r3
            if len(r4) > 1:
                r[i][j][k] += r4
# for vertex in end_vertex_mpdka:
#    print(r[start_vertex_mpdka[0]][vertex][max_v - 1], end='+')
'''