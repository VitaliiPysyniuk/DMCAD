from lab_2_main import *

if __name__ == '__main__':
    weight = read_file('test_files/l2_1.txt')
    res = dijkstra_method(2, 6, weight)
    print(res)
