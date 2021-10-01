def find_vertex_dka(start_vertex, letter, array_edges, used):
    for edge in array_edges:
        if edge[0] == start_vertex and edge[2] == letter and edge[1] not in used:
            used.append(edge[1])


def make_dka(nka, alphabet, array_edges):
    vertex_in_dka = [[[]]]
    for i in range(len(alphabet)):
        vertex_in_dka[0].append(-2)
    # -2 - not describe, -1 - no vertex on way from current vertex by current letter

    vertex_in_dka[0][0] = [nka[0].get_start_vertex()]
    used = []
    str_in_dka = 0
    while str_in_dka < len(vertex_in_dka):
        if vertex_in_dka[str_in_dka][-1] != -2:
            str_in_dka += 1
            continue
        for i in range(len(alphabet)):
            letter = alphabet[i]
            for vertex in vertex_in_dka[str_in_dka][0]:
                find_vertex_dka(vertex, letter, array_edges, used)
            used = sorted(used)
            j = 0
            for arr in vertex_in_dka:
                if arr[0] == used:
                    vertex_in_dka[str_in_dka][1 + i] = j
                    break
                j += 1
            else:
                if not used:
                    vertex_in_dka[str_in_dka][1 + i] = -1
                else:
                    vertex_in_dka[str_in_dka][1 + i] = len(vertex_in_dka)
                    vertex_in_dka.append([used])
                    for j in range(len(alphabet)):
                        vertex_in_dka[-1].append(-2)
            used = []
    start_vertex_nka = nka[0].get_start_vertex()
    end_vertex_nka = nka[0].get_end_vertex()
    start_vertex_dka = []
    end_vertex_dka = []

    for i in range(len(vertex_in_dka)):
        if start_vertex_dka == [] and start_vertex_nka in vertex_in_dka[i][0]:
            start_vertex_dka.append(i)
        if end_vertex_nka in vertex_in_dka[i][0]:
            end_vertex_dka.append(i)
    return vertex_in_dka, start_vertex_dka, end_vertex_dka


def make_array_edges_dka(vertex_in_dka, alphabet):
    array_edges_dka = []
    for i in range(len(vertex_in_dka)):
        for j in range(len(alphabet)):
            array_edges_dka.append([i, vertex_in_dka[i][1 + j], alphabet[j]])
    return array_edges_dka


def add_edges_dka(array_edges_dka, alphabet):
    add_edge = 0
    for edge in array_edges_dka:
        if edge[1] == -1:
            add_edge = 1
            break
    if add_edge:
        max_vertex = -1
        for edge in array_edges_dka:
            max_vertex = max(edge[0], max_vertex)
        max_vertex += 1
        for i in range(len(array_edges_dka)):
            if array_edges_dka[i][1] == -1:
                array_edges_dka[i][1] = max_vertex
                array_edges_dka.append([array_edges_dka[i][0], max_vertex, array_edges_dka[i][2]])
        for i in range(len(alphabet)):
            array_edges_dka.append([max_vertex, max_vertex, alphabet[i]])
    return array_edges_dka