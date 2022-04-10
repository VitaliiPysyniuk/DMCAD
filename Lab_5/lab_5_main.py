import numpy as np


def incident_check(graph_1, graph_2):
    vertex_number_1 = len(graph_1)
    vertex_number_2 = len(graph_2)
    if vertex_number_1 != vertex_number_2:
        return 'не встановлено'
    for i in range(vertex_number_1):
        if not (graph_1[i] == graph_2[i]).all():
            return 'не встановлено'
    return 'встановлено'


def read_file(filename):
    matrix = list()
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines[1:]:
        split_line = [int(element) for element in line[:-1].split(' ')]
        matrix.append(split_line)

    return np.array(matrix, float)


if __name__ == '__main__':
    incidence_matrix_1 = read_file('test_files/l5_1.txt')
    incidence_matrix_2 = read_file('test_files/l5_3.txt')
    print(f'Для поданих графів ізоморфізм {incident_check(incidence_matrix_1, incidence_matrix_2)}.')
