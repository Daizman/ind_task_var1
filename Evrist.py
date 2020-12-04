from TreeNode import TreeNode
import copy
import random


__PRECISION = 1000
__ALPHA = 0.5
__BETA = 1 - __ALPHA


def calc_probability_i_j(i, j, a, n, fer, alpha, beta):
    """
    :param i: i город
    :param j: j город
    :param a: матрица расстояний
    :param n: количество городов
    :param fer: матрица ферамонов
    :param alpha: коэффицент натройки влияния растояния
    :param beta: коэффицент натройки влияния наследственности
    :return: вероятность похода муравья из i в j
    """
    all_sum = 0
    for k in range(n):
        teta = 1 / a[i][k] if a[i][k] != float('inf') else 0
        tau = fer[i][k]
        all_sum += teta**alpha * tau**beta
    if a[i][j] == float('inf') or all_sum == 0:
        return 0
    return 100 * (1 / a[i][j]) ** alpha * fer[i][j] ** beta / all_sum


def go_ants(a, n, s):
    fer = [[1 for _ in range(n)] for _ in range(n)]
    node = None
    for i in range(__PRECISION):
        node = TreeNode([0], [], 0, 1, copy.deepcopy(a))
        while True:
            probs = [0]
            fr = node.v_to[-1] if node.v_to else 0
            for j in range(n):
                probs.append(probs[-1] + calc_probability_i_j(fr, j, node.cur_matr, n, fer, __ALPHA, __BETA))
            probs = probs[1:]
            roulete = random.randrange(0, 100)
            cur_way = -1
            for j in range(n):
                if roulete <= probs[j]:
                    if node.cur_matr[fr][j] == float('inf'):
                        if j != 0:
                            cur_way = j + 1
                        else:
                            cur_way = j
                    else:
                        cur_way = j
                    break

            if cur_way == -1:
                """
                for k in node.v_to:
                    for j in node.v_from:
                        fer[j][k] -= 1
                """
                node.v_from = []
                node.v_to = []
                node.cost = 0
                break

            # fer[node.v_from[-1]][cur_way] += 1
            node.cost += s - a[fr][cur_way] if cur_way not in node.v_from else -a[fr][cur_way]
            # node.cur_matr[fr][cur_way] = float('inf')
            if node.v_to:
                node.cur_matr[cur_way][fr] = float('inf')
            if node.v_to:
                node.v_from.append(fr)
            node.v_to.append(cur_way)
            if cur_way == 0:
                probs = [0]
                for j in range(n):
                    probs.append(probs[-1] + calc_probability_i_j(cur_way, j, node.cur_matr, n, fer, __ALPHA, __BETA))
                probs = probs[1:]
                if node.cost >= 0:
                    for k in node.v_to:
                        for j in node.v_from:
                            fer[j][k] += node.cost
                break

    if node.cost > 0:
        print(node.cost)
        for i in range(len(node.v_to)):
            print("{}->{}".format(node.v_from[i] + 1, node.v_to[i] + 1), end="  ")
        print()
    else:
        print("{}")


def main(n=None, a=None, s=None):
    if n is None:
        n = int(input())
        a = [[float(cost) for cost in input().replace("~", "inf").split()] for _ in range(n)]
        if n == 0:
            input()
        s = int(input())
    if n != 0:
        go_ants(a, n, s)
    else:
        print("{}")


if __name__ == "__main__":
    print("пустой граф:")
    main(0, [], 1)
    print("граф из одной вершины:")
    main(1, [[float('inf')]], 14)
    print("граф из двух вершин нет пути назад (невыг):")
    main(2, [
        [float('inf'), 5],
        [float('inf'), float('inf')]
    ], 2)
    print("граф из двух вершин нет пути назад (выг):")
    main(2, [
        [float('inf'), 5],
        [float('inf'), float('inf')]
    ], 6)
    print("граф из двух вершин есть путь назад (невыг):")
    main(2, [
        [float('inf'), 3],
        [12, float('inf')]
    ], 2)
    print("граф из двух вершин есть путь назад (выг):")
    main(2, [
        [float('inf'), 3],
        [12, float('inf')]
    ], 18)
    print("граф из двух вершин есть путь назад (ср):")
    main(2, [
        [float('inf'), 3],
        [12, float('inf')]
    ], 6)
    print("граф из n(5) вершин, полный (невыг):")
    main(5, [
        [float('inf'), 3, 8, 2, 2],
        [5, float('inf'), 4, 17, 9],
        [3, 6, float('inf'), 15, 2],
        [2, 14, 10, float('inf'), 12],
        [8, 3, 4, 9, float('inf')]
    ], 1)
    print("граф из n(5) вершин, полный (выг):")
    main(5, [
        [float('inf'), 3, 8, 2, 2],
        [5, float('inf'), 4, 17, 9],
        [3, 6, float('inf'), 15, 2],
        [2, 14, 10, float('inf'), 12],
        [8, 3, 4, 9, float('inf')]
    ], 140)
    print("граф из n(5) вершин, полный (ср):")
    main(5, [
        [float('inf'), 3, 8, 2, 2],
        [5, float('inf'), 4, 17, 9],
        [3, 6, float('inf'), 15, 2],
        [2, 14, 10, float('inf'), 12],
        [8, 3, 4, 9, float('inf')]
    ], 35)
    print("граф из n(5) вершин, первый город изолирован (невыг):")
    main(5, [
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 4, 17, 9],
        [float('inf'), 6, float('inf'), 15, 2],
        [float('inf'), 14, 10, float('inf'), 12],
        [float('inf'), 3, 4, 9, float('inf')]
    ], 1)
    print("граф из n(5) вершин, первый город изолирован (выг):")
    main(5, [
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 4, 17, 9],
        [float('inf'), 6, float('inf'), 15, 2],
        [float('inf'), 14, 10, float('inf'), 12],
        [float('inf'), 3, 4, 9, float('inf')]
    ], 140)
    print("граф из n(5) вершин, первый город изолирован (ср):")
    main(5, [
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 4, 17, 9],
        [float('inf'), 6, float('inf'), 15, 2],
        [float('inf'), 14, 10, float('inf'), 12],
        [float('inf'), 3, 4, 9, float('inf')]
    ], 25)
    print("граф из n(5) вершин, неполный (невыг):")
    main(5, [
        [float('inf'), 4, 5, float('inf'), 3],
        [3, float('inf'), 6, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [8, 6, float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), 9, float('inf')]
    ], 2)
    print("граф из n(5) вершин, неполный (выг):")
    main(5, [
        [float('inf'), 4, 5, float('inf'), 3],
        [3, float('inf'), 6, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [8, 6, float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), 9, float('inf')]
    ], 45)
    print("граф из n(5) вершин, неполный (ср):")
    main(5, [
        [float('inf'), 4, 5, float('inf'), 3],
        [3, float('inf'), 6, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [8, 6, float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), 9, float('inf')]
    ], 12)
    print("граф из n(5) вершин, неполный, без циклов и пути в А (невыг):")
    main(5, [
        [float('inf'), 4, 5, float('inf'), 3],
        [float('inf'), float('inf'), 6, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 8, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')]
    ], 1)
    print("граф из n(5) вершин, неполный, без циклов и пути в А (выг):")
    main(5, [
        [float('inf'), 4, 5, float('inf'), 3],
        [float('inf'), float('inf'), 6, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 8, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')]
    ], 45)
    print("граф из n(5) вершин, неполный, без циклов и пути в А (ср):")
    main(5, [
        [float('inf'), 4, 5, float('inf'), 3],
        [float('inf'), float('inf'), 6, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 8, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')]
    ], 12)
    print(
        "граф из n(5) вершин, неполный, можно вернуться только из первого перехода, проход через А невыгоден (невыг):")
    main(5, [
        [float('inf'), 4, 5, float('inf'), 3],
        [7, float('inf'), 6, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 8, float('inf'), float('inf')],
        [4, float('inf'), float('inf'), float('inf'), float('inf')]
    ], 1)
    print(
        "граф из n(5) вершин, неполный, можно вернуться только из первого перехода, проход через А невыгоден (выг):")
    main(5, [
        [float('inf'), 4, 5, float('inf'), 3],
        [7, float('inf'), 6, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 8, float('inf'), float('inf')],
        [4, float('inf'), float('inf'), float('inf'), float('inf')]
    ], 38)
    print(
        "граф из n(5) вершин, неполный, можно вернуться только из первого перехода, проход через А невыгоден (ср):")
    main(5, [
        [float('inf'), 4, 5, float('inf'), 3],
        [7, float('inf'), 6, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 8, float('inf'), float('inf')],
        [4, float('inf'), float('inf'), float('inf'), float('inf')]
    ], 9)
    print(
        "граф из n(5) вершин, неполный, можно вернуться только из первого перехода, проход через А выгоден (невыг):")
    main(5, [
        [float('inf'), 9, 8, float('inf'), 10],
        [4, float('inf'), 8, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 8, float('inf'), float('inf')],
        [4, float('inf'), float('inf'), float('inf'), float('inf')]
    ], 1)
    print(
        "граф из n(5) вершин, неполный, можно вернуться только из первого перехода, проход через А выгоден (выг):")
    main(5, [
        [float('inf'), 9, 8, float('inf'), 10],
        [4, float('inf'), 8, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 8, float('inf'), float('inf')],
        [4, float('inf'), float('inf'), float('inf'), float('inf')]
    ], 52)
    print(
        "граф из n(5) вершин, неполный, можно вернуться только из первого перехода, проход через А выгоден (ср):")
    main(5, [
        [float('inf'), 9, 8, float('inf'), 10],
        [4, float('inf'), 8, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 8, float('inf'), float('inf')],
        [4, float('inf'), float('inf'), float('inf'), float('inf')]
    ], 28)
    # main()
