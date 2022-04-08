import string
import numpy as np
from copy import deepcopy


def check_loop(adj_matrix):
    matrix = deepcopy(adj_matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                res = search(matrix, i, j, i)
                if res:
                    return res
    return False


def search(matrix, index_1, index_2, searched):
    m = deepcopy(matrix)
    m[index_1][index_2] = 0
    m[index_2][index_1] = 0
    row = m[index_2]
    res = False
    for i in range(len(row)):
        if row[i] == 1 and i == searched:
            return True
        elif row[i] == 1 and i != searched:
            res = search(m, index_2, i, searched)
    return res


def sort_edges(wei_matrix):
    edges = list()
    for i in range(len(wei_matrix)):
        for j in range(i + 1, len(wei_matrix[0])):
            if wei_matrix[i][j] == 0:
                continue
            edges.append({
                'weight': wei_matrix[i][j],
                'from': i,
                'to': j
            })
    sorted_edges = sorted(edges, key=lambda edge: edge['weight'])
    return sorted_edges


def read_file(filename):
    weights_list = list()
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines[1:]:
        split_line = [int(element) for element in line[:-1].split(' ')]
        weights_list.append(split_line)

    return np.array(weights_list)


def kruskal_method(matrix):
    adj_matrix = np.array([[0] * len(matrix)] * len(matrix))
    sorted_edges = sort_edges(matrix)
    visited_vertices = set()

    for edge in sorted_edges:
        adjacency_matrix_copy = deepcopy(adj_matrix)
        adjacency_matrix_copy[edge['from']][edge['to']] = 1
        adjacency_matrix_copy[edge['to']][edge['from']] = 1

        if not check_loop(adjacency_matrix_copy):
            visited_vertices.add(edge['from'])
            visited_vertices.add(edge['to'])
            adj_matrix = deepcopy(adjacency_matrix_copy)
    return adj_matrix


def print_result(adj_matrix, wei_matrix):
    total_length = 0
    edges = list()
    for i in range(len(adj_matrix)):
        for j in range(i + 1, len(adj_matrix)):
            if adj_matrix[i][j] == 1:
                edge = f'{string.ascii_uppercase[i]} - {string.ascii_uppercase[j]}'
                length = wei_matrix[i][j]
                edges.append({'edge': edge, 'length': length})
    edges = sorted(edges, key=lambda edge: edge['length'])
    for element in edges:
        print(f'Ребро {element["edge"]} ::: {element["length"]}')
        total_length += element["length"]
    print(f'          Σ ::: {total_length}')


if __name__ == '__main__':
    weight_matrix = read_file('test_files/l1_3.txt')
    adjacency_matrix = kruskal_method(weight_matrix)
    print_result(adjacency_matrix, weight_matrix)
