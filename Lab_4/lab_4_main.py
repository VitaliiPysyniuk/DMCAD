import numpy as np
import copy


def read_file(filename):
    matrix = list()
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines[1:]:
        split_line = [int(element) for element in line[:-1].split(' ')]
        matrix.append(split_line)

    return np.array(matrix, float)


def search_way(weight_matrix, current_vertex=0, visited_vertices=None):
    possible_ways = copy.copy(weight_matrix[current_vertex])
    sorted_list = np.sort([elem for elem in possible_ways if elem != 0])[::-1]
    visited = (visited_vertices if visited_vertices else []) + [current_vertex]
    for value in sorted_list:
        max_value_index = np.where(possible_ways == value)[0][0]
        if max_value_index in visited:
            possible_ways[max_value_index] = 0
            continue

        way_part = np.array([{'from': current_vertex, 'to': max_value_index, 'value': value}])
        if max_value_index == len(weight_matrix) - 1:
            return way_part

        inter_result = search_way(weight_matrix, max_value_index, visited)

        if inter_result is not None:
            return np.concatenate((way_part, inter_result))

        possible_ways[max_value_index] = 0

    return None


def change_matrix(way, weight_matrix):
    matrix = copy.deepcopy(weight_matrix)
    min_value = min([elem['value'] for elem in way])

    for elem in way:
        i = elem['from']
        j = elem['to']
        matrix[i][j] = matrix[i][j] - min_value
        matrix[j][i] = matrix[j][i] + min_value

    return matrix


def ford_falkerson_algorithm(filename):
    weight_matrix = read_file(filename)
    ways = list()
    iteration = 1
    while True:
        result = search_way(weight_matrix)
        if result is None:
            break

        weight_matrix = change_matrix(result, weight_matrix)
        ways.append(result)
        iteration += 1

    print_result(ways)


def print_result(ways):
    print(f'Possible ways ({len(ways)}):')
    volume = 0
    for way in ways:
        # print(way)
        min_value = min([elem['value'] for elem in way])
        volume += min_value
        for elem in way[:-1]:
            print(elem['from'] + 1, end=' -> ')
        print(f"{way[-1]['from'] + 1} -> {way[-1]['to'] + 1} = {min_value}")

    print(f'Total volume: {volume}')


if __name__ == '__main__':
    ford_falkerson_algorithm('test_files/l4_2.txt')
