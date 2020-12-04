from TreeNode import TreeNode
import heapq
from queue import Queue
import copy


def contain_node(lst, node):
    node_from_len = len(node.v_from)
    node_to_len = len(node.v_to)
    for lst_node in lst:
        if lst_node.level != node.level:
            continue
        if lst_node.cost != node.cost:
            continue
        lst_node_from_len = len(lst_node.v_from)
        if lst_node_from_len != node_from_len:
            continue
        lst_node_to_len = len(lst_node.v_to)
        if lst_node_to_len != node_to_len:
            continue
        from_test = True
        for i in range(lst_node_from_len):
            if lst_node.v_from[i] != node.v_from[i]:
                from_test = False
                break
        if not from_test:
            continue
        to_test = True
        for i in range(lst_node_to_len):
            if lst_node.v_to[i] != node.v_to[i]:
                to_test = False
                break
        if not to_test:
            continue
        return True
    return False


def exh_search(a, n, s):
    nodes = []
    queue = Queue()
    node = TreeNode([0], [], 0, 0, a)
    queue.put(node)
    heapq.heappush(nodes, node)
    while True:
        u = queue.get()
        fr = u.v_to[-1] if u.v_to else 0
        for _node in range(n):
            if u.cur_matr[fr][_node] != float('inf'):
                new_cost = u.cur_matr[fr][_node] - s + u.cost if _node not in u.v_from else u.cur_matr[fr][_node] + u.cost
                new_to = copy.deepcopy(u.v_to)
                new_from = copy.deepcopy(u.v_from)
                new_matr = copy.deepcopy(u.cur_matr)
                if fr != 0 or not u.v_to == []:
                    new_from.append(u.v_to[-1])
                new_matr[fr][_node] = float('inf')
                new_level = u.level + 1 if _node not in u.v_from else u.level - 1
                new_to.append(_node)
                new_node = TreeNode(new_from, new_to, new_cost, new_level, new_matr)
                if not contain_node(nodes, new_node):
                    heapq.heappush(nodes, new_node)
                    queue.put(new_node)

        if queue.empty():
            break

    for el in nodes:
        if el.v_to and a[el.v_to[-1]][0] == float('inf'):
            el.cost = float('inf')
        elif el.v_to:
            el.cost += a[el.v_to[-1]][0]

    nodes.sort(key=lambda elem: elem.cost)
    ans_node = nodes[0]
    if ans_node.cost < 0:
        print(-ans_node.cost)
        ans_node.v_from.append(ans_node.v_to[-1])
        ans_node.v_to.append(0)
        for i in range(len(ans_node.v_to)):
            print("{}->{}".format(ans_node.v_from[i] + 1, ans_node.v_to[i] + 1), end="  ")
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

    if n > 1:
        exh_search(a, n, s)
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
