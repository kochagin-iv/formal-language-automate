from constants import syntax_tree, specsymbols, nka


class nka_vertex:
    edges = [[]]
    start_vertex = 0
    end_vertex = 0

    def get_edges(self):
        return self.edges

    def get_start_vertex(self):
        return self.start_vertex

    def get_end_vertex(self):
        return self.end_vertex

    def set_edges(self, new_edges):
        self.edges = new_edges

    def set_start_vertex(self, new_start):
        self.start_vertex = new_start

    def set_end_vertex(self, new_end):
        self.end_vertex = new_end


def find_max_vertex_in_nka():
    max_vertex = -1
    for v in nka:
        edges = v.get_edges()
        for edge in edges:
            if len(edge) > 0:
                max_vertex = max(edge[0], edge[1], max_vertex)
    return max_vertex


def make_nka(vertex, alphabet):
    if syntax_tree[vertex] is None:
        return
    if syntax_tree[vertex] in specsymbols:
        make_nka(vertex * 2 + 1, alphabet)
        make_nka(vertex * 2 + 2, alphabet)
    if syntax_tree[vertex] in alphabet or syntax_tree[vertex] == '$':
        new_start_vertex = find_max_vertex_in_nka() + 1
        if new_start_vertex == 0:
            new_start_vertex = 1
        new_end_vertex = new_start_vertex + 1
        if syntax_tree[vertex] == '$':
            new_edges = [[new_start_vertex, new_end_vertex, 'eps']]
        else:
            new_edges = [[new_start_vertex, new_end_vertex, syntax_tree[vertex]]]
        nka[vertex].set_edges(new_edges)
        nka[vertex].set_start_vertex(new_start_vertex)
        nka[vertex].set_end_vertex(new_end_vertex)
        return

    left_child_edges = nka[vertex * 2 + 1].get_edges()
    left_start = nka[vertex * 2 + 1].get_start_vertex()
    left_end = nka[vertex * 2 + 1].get_end_vertex()
    if syntax_tree[vertex] == '*':
        new_start_end_vertex = find_max_vertex_in_nka() + 1
        left_child_edges.append([new_start_end_vertex, left_start, 'eps'])
        left_child_edges.append([left_end, new_start_end_vertex, 'eps'])
        nka[vertex].set_start_vertex(new_start_end_vertex)
        nka[vertex].set_end_vertex(new_start_end_vertex)
        nka[vertex].set_edges(left_child_edges)
        return

    right_child_edges = nka[vertex * 2 + 2].get_edges()
    right_start = nka[vertex * 2 + 2].get_start_vertex()
    right_end = nka[vertex * 2 + 2].get_end_vertex()
    if syntax_tree[vertex] == '.':
        for edge in right_child_edges:
            left_child_edges.append(edge)
        left_child_edges.append([left_end, right_start, 'eps'])
        nka[vertex].set_start_vertex(left_start)
        nka[vertex].set_end_vertex(right_end)
        nka[vertex].set_edges(left_child_edges)
        return

    if syntax_tree[vertex] == '+':
        new_start_vertex = find_max_vertex_in_nka() + 1
        new_end_vertex = new_start_vertex + 1
        nka[vertex].set_start_vertex(new_start_vertex)
        nka[vertex].set_end_vertex(new_end_vertex)
        for edge in right_child_edges:
            left_child_edges.append(edge)
        left_child_edges.append([new_start_vertex, left_start, 'eps'])
        left_child_edges.append([new_start_vertex, right_start, 'eps'])
        left_child_edges.append([left_end, new_end_vertex, 'eps'])
        left_child_edges.append([right_end, new_end_vertex, 'eps'])
        nka[vertex].set_edges(left_child_edges)
        return


def delete_eps_edge_nka(nka, alphabet):
    array_edges = nka[0].get_edges()
    end_vertex_nka = [nka[0].get_end_vertex()]
    vertexs = []
    for edge in array_edges:
        if edge[0] not in vertexs:
            vertexs.append(edge[0])
        if edge[1] not in vertexs:
            vertexs.append(edge[1])
    fl = 1
    while fl:
        fl = 0
        for u in vertexs:
            for v in vertexs:
                for p in vertexs:
                    if [u, v, 'eps'] in array_edges and [v, p, 'eps'] in array_edges and [u, p,
                                                                                          'eps'] not in array_edges:
                        array_edges.append([u, p, 'eps'])
                        fl = 1

    fl = 1
    while fl:
        fl = 0
        for u in end_vertex_nka:
            for edge in array_edges:
                if edge[1] == u and edge[2] == 'eps' and edge[0] not in end_vertex_nka:
                    end_vertex_nka.append(edge[0])
                    fl = 1

    fl = 1
    while fl:
        fl = 0
        for u in vertexs:
            for v in vertexs:
                for p in vertexs:
                    for letter in alphabet:
                        if [u, v, 'eps'] in array_edges and [v, p, letter] in array_edges and [u, p,
                                                                                               letter] not in array_edges:
                            array_edges.append([u, p, letter])
                            fl = 1
                        if [u, v, letter] in array_edges and [v, p, 'eps'] in array_edges and [u, p,
                                                                                               letter] not in array_edges:
                            array_edges.append([u, p, letter])
                            fl = 1

    fl = 1
    while fl:
        fl = 0
        for i in range(len(array_edges)):
            if array_edges[i][2] == 'eps':
                del array_edges[i]
                fl = 1
                break
    return (array_edges, end_vertex_nka)


def from_array_edges_to_vector_vertex(array_edges):
    vector_vertex = []
    for i in range(nka[0].get_end_vertex() + 1):
        vector_vertex.append([])
    for edge in array_edges:
        vector_vertex[edge[0]].append([edge[1], edge[2]])
    return vector_vertex


def find_delete_vertex(start_vertex, used, vector_vertex):
    if start_vertex in used:
        return
    used.append(start_vertex)
    for v in vector_vertex[start_vertex]:
        find_delete_vertex(v[0], used, vector_vertex)
    return used


def make_correct_array_edges_end_vertex_vec_vertex_after_delete(array_edges, used, end_vertex_nka):
    array_edges1 = []
    for edge in array_edges:
        if (edge[0] not in used) or (edge[1] not in used):
            continue
        array_edges1.append(edge)

    end_vertex_nka1 = []
    for vertex in end_vertex_nka:
        if vertex in used:
            end_vertex_nka1.append(vertex)

    end_vertex_nka = end_vertex_nka1

    array_edges = array_edges1
    vector_vertex = []
    for i in range(max(used) + 1):
        vector_vertex.append([])
    for edge in array_edges:
        vector_vertex[edge[0]].append([edge[1], edge[2]])
    return array_edges, used, end_vertex_nka


