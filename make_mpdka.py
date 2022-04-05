def make_mpdka(vertex_in_pdka, end_vertex_pdka, alphabet, array_edges_pdka):
    vertex_in_pdka = sorted(vertex_in_pdka)
    cur_condition = []
    for i in vertex_in_pdka:
        if i in end_vertex_pdka:
            cur_condition.append(1)
        else:
            cur_condition.append(0)

    new_condition = [None] * len(vertex_in_pdka)
    while 1:
        conditions = []
        for i in range(len(vertex_in_pdka)):
            cond_str = ""
            cond_str += str(cur_condition[i])
            for letter in alphabet:
                for edge in array_edges_pdka:
                    if edge[0] == i and edge[2] == letter:
                        cond_str += str(cur_condition[edge[1]])
                        break
            conditions.append(cond_str)
        original_conditions = []
        for cond in conditions:
            if cond not in original_conditions:
                original_conditions.append(cond)
        num_cond = 0
        for cond in original_conditions:
            for j in range(len(vertex_in_pdka)):
                if conditions[j] == cond:
                    new_condition[j] = num_cond
            num_cond += 1
        if cur_condition == new_condition:
            break
        cur_condition = new_condition
        new_condition = [None] * len(vertex_in_pdka)

    compression = {}
    for i in cur_condition:
        compression[i] = []
    for i in range(len(cur_condition)):
        compression[cur_condition[i]].append(i)
    return compression


def get_array_edges_mpdka(compression, array_edges_pdka):
    array_edges_mpdka = []
    for i in compression:
        for j in compression:
            for vertex1 in compression[i]:
                for vertex2 in compression[j]:
                    for edge in array_edges_pdka:
                        if edge[0] == vertex1 and edge[1] == vertex2:
                            new_edge = [i, j, edge[2]]
                            if new_edge not in array_edges_mpdka:
                                array_edges_mpdka.append(new_edge)
    return array_edges_mpdka


def find_end_start_vertex_mpdka(compression, start_vertex_pdka, end_vertex_pdka):
    start_vertex_mpdka = []
    end_vertex_mpdka = []
    for i in compression:
        for end_vertex in end_vertex_pdka:
            if end_vertex in compression[i]:
                if i not in end_vertex_mpdka:
                    end_vertex_mpdka.append(i)
    for i in compression:
        for start_vertex in start_vertex_pdka:
            if start_vertex in compression[i]:
                if i not in start_vertex_mpdka:
                    start_vertex_mpdka.append(i)
    return start_vertex_mpdka, end_vertex_mpdka
