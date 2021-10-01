import re
import unittest
from constants import reg, specsymbols, max_length_testing, nka, regex
from make_dka import make_dka, make_array_edges_dka, add_edges_dka
from make_mpdka import make_mpdka, find_end_start_vertex_mpdka, get_array_edges_mpdka
from make_nka import nka_vertex, make_nka, delete_eps_edge_nka, find_delete_vertex, \
    make_correct_array_edges_end_vertex_vec_vertex_after_delete
from make_pdka import get_vertex_pdka, check_if_addition_regular
from make_syntax_tree import make_syntax_tree

alphabet = ""
for i in reg:
    if not (i in specsymbols) and not (i in alphabet) and i != '$':
        alphabet += i


class vertex_bor:
    to = []
    terminal = 0

    def __init__(self):
        self.to = [-1] * len(alphabet)
        self.terminal = 0


bor = [vertex_bor()]


def add_in_bor(num_vertex, length, max_length):
    if length == max_length:
        bor[num_vertex].terminal = 1
        return
    for letter in alphabet:
        if letter == '$': continue
        if bor[num_vertex].to[ord(letter) - ord('a')] == -1:
            bor.append(vertex_bor())
            bor[num_vertex].to[ord(letter) - ord('a')] = len(bor) - 1
        add_in_bor(bor[num_vertex].to[ord(letter) - ord('a')], length + 1, max_length)


add_in_bor(0, 0, max_length_testing)

bor_strs = []


def get_all_str_from_bor(vertex, tmp_str):
    if bor[vertex].terminal:
        bor_strs.append(tmp_str)
        return
    for i in range(len(bor[vertex].to)):
        idx = bor[vertex].to[i]
        if idx == -1:
            continue
        get_all_str_from_bor(idx, tmp_str + str(chr(ord('a') + i)))


get_all_str_from_bor(0, '')


# print(bor_strs)


def get_max_vertex(array_edges):
    ans = 0
    for edge in array_edges:
        if edge == []: continue
        ans = max(ans, edge[0], edge[1])
    return ans


def from_array_edges_to_vector_vertex(array_edges):
    vector_vertex = []
    for i in range(get_max_vertex(array_edges) + 1):
        vector_vertex.append([])
    for edge in array_edges:
        if edge == []: continue
        vector_vertex[edge[0]].append([edge[1], edge[2]])
    return vector_vertex

str_in_automate = 0


def is_in_automate(vertex, tmp_str, string, vector_vertex, end_vertex):
    #print(tmp_str, string, vertex, end_vertex)
    global str_in_automate
    if len(tmp_str) > len(string):
        return
    if isinstance(end_vertex, int):
        if tmp_str == string and vertex == end_vertex:
            str_in_automate = 1
            return
    if isinstance(end_vertex, list):
        if tmp_str == string and vertex in end_vertex:
            str_in_automate = 1
            return
    for edge in vector_vertex[vertex]:
        if edge[1] == 'eps':
            is_in_automate(edge[0], tmp_str, string, vector_vertex, end_vertex)
        if tmp_str + edge[1] in string:
            is_in_automate(edge[0], tmp_str + edge[1], string, vector_vertex, end_vertex)


def check(array_edges, start_vertex, end_vertex):
    ans = 1
    vector_vertex = from_array_edges_to_vector_vertex(array_edges)
    for string in bor_strs:
        is_in_regex = 0
        if re.fullmatch(regex, string) is not None:
            is_in_regex = 1
        global str_in_automate
        str_in_automate = 0
        is_in_automate(start_vertex, '', string, vector_vertex, end_vertex)
        if str_in_automate and is_in_regex:
            #print(string, "in automate and in regex")
            continue
        if not str_in_automate and not is_in_regex:
            #print(string, "not in automate and not in regex")
            continue
        if str_in_automate and not is_in_regex:
            #print('AAAAAAAAA')
            #print(string, "in automate and not in regex")
            ans = 0
            break
        if not str_in_automate and is_in_regex:
            ans = 0
            #print('AAAAAAAAA')
            #print(string, "not in automate and in regex")
            continue
    return ans


for i in range(1000):
    nka[i] = nka_vertex()

make_syntax_tree(0)
make_nka(0, alphabet)
print('nka')
nka_test = check(nka[0].get_edges(), nka[0].get_start_vertex(), nka[0].get_end_vertex())
array_edges, end_vertex_nka = delete_eps_edge_nka(nka, alphabet)
print('nka_without_eps')
#check(array_edges, nka[0].get_start_vertex(), end_vertex_nka)

vector_vertex = from_array_edges_to_vector_vertex(array_edges)
used = []
used = find_delete_vertex(nka[0].get_start_vertex(), used, vector_vertex)
array_edges, used, end_vertex_nka = make_correct_array_edges_end_vertex_vec_vertex_after_delete(array_edges, used, end_vertex_nka)

vertex_in_dka, start_vertex_dka, end_vertex_dka = make_dka(nka, alphabet, array_edges)
array_edges_dka = make_array_edges_dka(vertex_in_dka, alphabet)
array_edges_dka = add_edges_dka(array_edges_dka, alphabet)
print('dka')
dka_test = check(array_edges_dka, start_vertex_dka[0], end_vertex_dka)

array_edges_pdka = array_edges_dka
start_vertex_pdka = start_vertex_dka
end_vertex_pdka = end_vertex_dka
print('pdka')
pdka_test = check(array_edges_pdka, start_vertex_pdka[0], end_vertex_pdka)
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
print('mpdka')
mpdka_test = check(array_edges_mpdka, start_vertex_mpdka[0], end_vertex_mpdka)


class MyTestCase(unittest.TestCase):
    def test_nka(self):
        self.assertEqual(nka_test, 1)

    def test_dka(self):
        self.assertEqual(dka_test, 1)

    def test_pdka(self):
        self.assertEqual(pdka_test, 1)

    def test_mpdka(self):
        self.assertEqual(mpdka_test, 1)


if __name__ == '__main__':
    unittest.main()

