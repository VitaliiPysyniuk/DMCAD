# shortest_ways = [{'length': 0, 'way': list()} for i in range(5)]
# print(shortest_ways)
# shortest_ways[0]['length'] = 5
# print(shortest_ways)
#
import numpy as np
# print(0 < np.Infinity)

# x = [0, 0, 1, 5]
# print(x.count(0))

# a = {0, 1, 3, 4, 5, 7}
# b = {0, 1}
# print(b.issubset(a))
# print(a)

# x = np.array([np.zeros(5, int) for i in range(5)])
# x[0][0] = 1
# print(x)
#
# y = np.zeros(5, int)
# print(y)
b = {0, 1}
i, j = b
print(i, j)


# def build_combinations(pairs, vertices):
#     combinations = list()
#     for i in range(len(pairs)):
#         # unused_vertices = vertices
#         # combination = [pairs[i]]
#         # unused_vertices = unused_vertices.difference(pairs[i])
#
#         # unused_pairs = deepcopy(pairs).pop(i)
#         # for j in range(len(pairs)):
#         #     if i == j:
#         #         continue
#         #     if pairs[j].issubset(unused_vertices):
#         #         combination.append(pairs[j])
#         #         unused_vertices = unused_vertices.difference(pairs[j])
#         #
#         #     if len(unused_vertices) == 0:
#         #         combinations.append(combination)
#         #         break
#         pairs_copy = deepcopy(pairs)
#         while True:
#             unused_vertices = vertices
#             combination = [pairs[i]]
#             unused_vertices = unused_vertices.difference(pairs[i])
#             for pair in pairs_copy:
#                 if pair.issubset(unused_vertices):
#                     combination.append(pair)
#                     unused_vertices = unused_vertices.difference(pair)
#                     pairs_copy.remove(pair)
#
#                 if len(unused_vertices) == 0:
#                     combinations.append(combination)
#                     break
#             if len(unused_vertices) != 0:
#                 break
#
#     for x in combinations:
#         print(x)
#     print(len(combinations))
#
#     return combinations

x = [1, 2, 3, 4, 5, 6]
# for i in x:
#     print(i)
#     if i == 3:
#         x.remove(i)
#
#
# x = [{1, 2}]
# print({1, 2} in x)

k = [3, 9, 9, 9, 3]
# x = x[:2] + k + x[3:]
# print(x)
print(k[1:])

# weight_matrix = np.array([
#     [0, 7, 0, 5, 0, 0, 0],
#     [7, 0, 8, 9, 7, 0, 0],
#     [0, 8, 0, 0, 5, 0, 0],
#     [5, 9, 0, 0, 15, 6, 0],
#     [0, 7, 5, 0, 0, 8, 9],
#     [0, 0, 0, 6, 8, 0, 11],
#     [0, 0, 0, 0, 9, 11, 0]
# ])
