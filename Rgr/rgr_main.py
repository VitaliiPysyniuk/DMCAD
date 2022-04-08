import numpy as np
import copy
import sys

from rgr_ui import *


class EdmondsCarp:
    @staticmethod
    def dijkstra_method(start, end, wei_matrix):
        number_of_vertices = len(wei_matrix)
        shortest_ways = [{'length': [np.Infinity], 'way': f'{start}', 'used': False} for i in range(number_of_vertices)]
        current_vertex = start
        shortest_ways[current_vertex]['length'] = list()

        while True:
            for i in range(number_of_vertices):
                if i == current_vertex or wei_matrix[current_vertex][i] == 0:
                    continue
                new_length = shortest_ways[current_vertex]['length'] + [wei_matrix[current_vertex][i]]
                if sum(new_length) < sum(shortest_ways[i]['length']):
                    shortest_ways[i]['length'] = copy.copy(new_length)
                    shortest_ways[i]['way'] = shortest_ways[current_vertex]['way'] + f'-{i}'

            shortest_ways[current_vertex]['used'] = True
            prev_vertex = current_vertex

            min_length = {'length': [np.Infinity]}
            for element in shortest_ways:
                if sum(element['length']) < sum(min_length['length']) and not element['used']:
                    min_length = element
                    current_vertex = shortest_ways.index(element)

            if prev_vertex == current_vertex:
                break

        if shortest_ways[end]['length'] == [np.Infinity]:
            return None
        return shortest_ways[end]

    @staticmethod
    def read_file(filename):
        matrix = list()
        with open(filename, 'r') as file:
            lines = file.readlines()
        for line in lines[1:]:
            split_line = [int(element) for element in line[:-1].split(' ')]
            matrix.append(split_line)

        return np.array(matrix)

    @staticmethod
    def algorithm(weight_matrix):
        vertices_number = len(weight_matrix)
        ways = list()
        iter = 1
        while True:
            result = EdmondsCarp.dijkstra_method(0, vertices_number - 1, weight_matrix)
            if result is None:
                break

            weight_matrix = EdmondsCarp.change_matrix(result, weight_matrix)
            ways.append(result)
            iter += 1

        return EdmondsCarp.print_result(ways)

    @staticmethod
    def change_matrix(way, weight_matrix):
        matrix = copy.deepcopy(weight_matrix)
        min_value = min(way['length'])
        vertices = [int(vertex) for vertex in way['way'].split('-')]

        for k in range(len(vertices) - 1):
            i = vertices[k]
            j = vertices[k + 1]
            matrix[i][j] = matrix[i][j] - min_value
            matrix[j][i] = matrix[j][i] + min_value

        return matrix

    @staticmethod
    def print_result(ways):
        text = ''
        text += f'Шляхи для проходження потоку ({len(ways)}):\n'
        # text += f'Possible ways ({len(ways)}):\n'
        # print(f'Possible ways ({len(ways)}):')
        volume = 0
        for way in ways:
            min_value = min(way['length'])
            volume += min_value
            vertices = [int(vertex) for vertex in way['way'].split('-')]
            for elem in vertices[:-1]:
                text += f'{elem + 1} -> '
                # print(elem + 1, end=' -> ')
            text += f"{vertices[-1] + 1} = {min_value}\n"
            # print(f"{vertices[-1] + 1} = {min_value}")

        text += f'Загальний розмір потоку: {volume}'
        # text += f'Total volume: {volume}'
        # print(f'Total volume: {volume}')

        return text


class MainProgram(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainProgram, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.execute)
        self.ui.pushButton_1.clicked.connect(self.clear)
        self.lines_matrix = None

    def build_matrix(self):
        cells = [''] * 64
        i = 1
        for child in self.ui.centralwidget.children():
            if isinstance(child, QtWidgets.QLineEdit):
                index = int(child.objectName().split('_')[1])
                cells[index - 1] = child
        matrix = list()
        for i in range(8):
            matrix.append(cells[i * 8: (i + 1) * 8])

        self.lines_matrix = matrix

    def execute(self):
        self.build_matrix()
        vertices_number = self.ui.spinBox.value()
        weight_matrix = list()
        for i in range(vertices_number):
            row = list()
            for j in range(vertices_number):
                value = self.lines_matrix[i][j].text()
                row.append(int(0 if value == '' else value))
            weight_matrix.append(row)

        edmonds_carp = EdmondsCarp()
        # weight_matrix = edmonds_carp.read_file('test_files/rgr_2.txt')
        text = edmonds_carp.algorithm(np.array(weight_matrix))
        text = '------------------------------------------ Результати ------------------------------------------\n' \
               + text
        self.ui.textBrowser.setText(text)

    def clear(self):
        for row in self.lines_matrix:
            for item in row:
                item.setText('')
        self.ui.textBrowser.setText('')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MainProgram()
    application.show()
    sys.exit(app.exec())
