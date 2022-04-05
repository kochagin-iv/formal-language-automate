from constants import make_addition_regular


def get_vertex_pdka(array_edges_pdka):
    vertex_in_pdka = []
    for edge in array_edges_pdka:
        if edge[0] not in vertex_in_pdka:
            vertex_in_pdka.append(edge[0])
    return vertex_in_pdka


def check_if_addition_regular(vertex_in_pdka, end_vertex_pdka):
    if make_addition_regular:
        end_vertex_pdka_new = []
        for vertex in vertex_in_pdka:
            if vertex not in end_vertex_pdka:
                end_vertex_pdka_new.append(vertex)
        end_vertex_pdka = end_vertex_pdka_new
    return end_vertex_pdka

