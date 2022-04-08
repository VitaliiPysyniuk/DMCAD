import numpy as np
from copy import deepcopy
import string


def dijkstra_method(start, end, wei_matrix):
    number_of_vertices = len(wei_matrix)
    shortest_ways = [{'length': np.Infinity, 'way': f'{start}', 'used': False} for i in range(number_of_vertices)]
    shortest_ways[start]['length'] = 0
    current_vertex = start

    while True:
        for i in range(number_of_vertices):
            if i == current_vertex or wei_matrix[current_vertex][i] == 0:
                continue
            new_length = wei_matrix[current_vertex][i] + shortest_ways[current_vertex]['length']
            if new_length < shortest_ways[i]['length']:
                shortest_ways[i]['length'] = new_length
                shortest_ways[i]['way'] = shortest_ways[current_vertex]['way'] + f'-{i}'

        shortest_ways[current_vertex]['used'] = True
        prev_vertice = current_vertex

        min_length = {'length': np.Infinity}
        for element in shortest_ways:
            if element['length'] < min_length['length'] and not element['used']:
                min_length = element
                current_vertex = shortest_ways.index(element)

        if prev_vertice == current_vertex:
            break

    return shortest_ways[end]


def print_ways(ways):
    for way in ways:
        print(way)


def read_file(filename):
    weights_list = list()
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines[1:]:
        split_line = [int(element) for element in line[:-1].split(' ')]
        weights_list.append(split_line)

    return np.array(weights_list)


def select_vertices(wei_matrix):
    vertices = list()
    for i in range(len(wei_matrix)):
        if (len(wei_matrix[i]) - np.count_nonzero(wei_matrix[i] == 0)) % 2 != 0:
            vertices.append(i)

    return set(vertices)


def generate_matrix(wei_matrix, vertices):
    matrix = list()
    for i in vertices:
        row = list()
        for j in vertices:
            value = wei_matrix[i][j]
            if i != j and value == 0:
                result = dijkstra_method(i, j, wei_matrix)
                value = result['length']
            row.append(value)
        matrix.append(row)
    matrix = np.array(matrix)

    return matrix


def build_pairs(vertices):
    vertices = list(vertices)
    number_of_vertices = len(vertices)
    pairs = list()
    for i in range(number_of_vertices):
        for j in range(i + 1, number_of_vertices):
            pairs.append({vertices[i], vertices[j]})
    return pairs


def build_combinations(pairs, vertices):
    combinations = list()
    for i in range(len(pairs)):
        used_pairs = list()
        while True:
            unused_vertices = vertices
            combination = [pairs[i]]
            unused_vertices = unused_vertices.difference(pairs[i])
            for j in range(i + 1, len(pairs)):
                if pairs[j].issubset(unused_vertices) and pairs[j] not in used_pairs:
                    combination.append(pairs[j])
                    unused_vertices = unused_vertices.difference(pairs[j])
                    used_pairs.append(pairs[j])

                if len(unused_vertices) == 0:
                    combinations.append(combination)
                    break
            if len(unused_vertices) != 0:
                break

    return combinations


def select_best_combination(weight_matrix):
    vertices = select_vertices(weight_matrix)
    second_wei_matrix = generate_matrix(weight_matrix, vertices)
    pairs = build_pairs(vertices)
    combinations = build_combinations(pairs, vertices)

    minimal_length = np.Infinity
    best_combination = None
    vertices = list(vertices)
    for combination in combinations:
        length = 0
        for pair in combination:
            i = vertices.index(list(pair)[0])
            j = vertices.index(list(pair)[1])
            length += second_wei_matrix[i][j]

        if length <= minimal_length:
            minimal_length = length
            best_combination = deepcopy(combination)

    return best_combination


def generate_adjacency_matrix(weight_matrix, combination):
    number_of_vertices = len(weight_matrix)
    adjacency_matrix = np.array([np.zeros(number_of_vertices, int) for i in range(number_of_vertices)])

    for i in range(number_of_vertices):
        for j in range(i + 1, number_of_vertices):
            if weight_matrix[i][j] != 0:
                adjacency_matrix[i][j] += 1
                adjacency_matrix[j][i] += 1

    for pair in combination:
        i, j = pair
        if weight_matrix[i][j] == 0:
            result = dijkstra_method(i, j, weight_matrix)
            way = [int(vertex) for vertex in result['way'].split('-')]
            for k in range(len(way) - 1):
                adjacency_matrix[way[k]][way[k + 1]] += 1
                adjacency_matrix[way[k + 1]][way[k]] += 1
        else:
            adjacency_matrix[i][j] += 1
            adjacency_matrix[j][i] += 1

    return adjacency_matrix


def build_loop(start_vertex, weight_matrix, adjacency_matrix):
    number_of_vertices = len(weight_matrix)
    # adj_matrix = deepcopy(adjacency_matrix)
    adj_matrix = adjacency_matrix
    row_index = start_vertex
    loop_length = 0
    loop_direction = [row_index]

    while True:
        for i in range(number_of_vertices):
            if adj_matrix[row_index][i] > 0:
                loop_length += weight_matrix[row_index][i]
                adj_matrix[row_index][i] -= 1
                adj_matrix[i][row_index] -= 1
                loop_direction.append(i)
                row_index = i
                break
        if row_index == start_vertex and len(set(adj_matrix[row_index])) == 1:
            break

    return {'loop_length': loop_length, 'loop_direction': loop_direction}


def combine_loops(weight_matrix, adjacency_matrix):
    loops = list()
    stop_flag = False
    while not stop_flag:
        for i in range(len(adjacency_matrix)):
            if len(set(adjacency_matrix[i])) > 1:
                loop = build_loop(i, weight_matrix, adjacency_matrix)
                loops.append(loop)
                stop_flag = False
                break
            stop_flag = True

    while len(loops) > 1:
        loops[0]['loop_length'] += loops[1]['loop_length']
        i = loops[0]['loop_direction'].index(loops[1]['loop_direction'][0])
        loops[0]['loop_direction'] = \
            loops[0]['loop_direction'][:i] + loops[1]['loop_direction'] + loops[0]['loop_direction'][i + 1:]
        loops.pop(1)

    return loops[0]


def print_result(loop):
    print(f'Direction: {string.ascii_uppercase[loop["loop_direction"][0]]}', end='')
    for vertex in loop['loop_direction'][1:]:
        print(f' -> {string.ascii_uppercase[vertex]}', end='')
    print(f'\n   Length: {loop["loop_length"]}')


if __name__ == '__main__':
    weight_matrix = read_file('test_files/l2_4.txt')
    best_combination = select_best_combination(weight_matrix)
    adjacency_matrix = generate_adjacency_matrix(weight_matrix, best_combination)
    adjacency_matrix_copy = deepcopy(adjacency_matrix)
    main_loop = combine_loops(weight_matrix, adjacency_matrix_copy)

    print_result(main_loop)
