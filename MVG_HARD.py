from TreeNode import TreeNode
import heapq
import copy


def redux_strs(matrix, n, deleted_strs=[], deleted_cols=[]):
    mins = []
    for i in range(n):
        st_min = float('inf')
        for j in range(n):
            if matrix[i][j] < st_min and j not in deleted_cols and i not in deleted_strs:
                st_min = matrix[i][j]
        if i not in deleted_strs:
            mins.append(st_min)
            for j in range(n):
                matrix[i][j] -= st_min

    return mins


def redux_cols(matrix, n, deleted_strs=[], deleted_cols=[]):
    mins = []
    for i in range(n):
        col_min = float('inf')
        for j in range(n):
            if matrix[j][i] < col_min and i not in deleted_cols and j not in deleted_strs:
                col_min = matrix[j][i]
        if i not in deleted_cols:
            mins.append(col_min)
            for j in range(n):
                matrix[j][i] -= col_min

    return mins


def snd_min_str(matrix, str_ind, n, deleted_cols=[]):
    st = []
    for i in range(n):
        for j in range(n):
            if i == str_ind and j not in deleted_cols:
                st.append(matrix[i][j])
    min_1 = min(st)
    snd = False
    min_2 = float('inf')
    new_n = n - len(deleted_cols)
    for i in range(new_n):
        if st[i] == min_1 and snd:
            min_2 = min_1
            break
        elif st[i] == min_1:
            snd = True
        elif st[i] < min_2:
            min_2 = st[i]

    return min_2


def snd_min_col(matrix, col_ind, n, deleted_strs=[]):
    col = []
    for i in range(n):
        for j in range(n):
            if i == col_ind and j not in deleted_strs:
                col.append(matrix[j][i])
    min_1 = min(col)
    snd = False
    min_2 = float('inf')
    new_n = n - len(deleted_strs)
    for i in range(new_n):
        if col[i] == min_1 and snd:
            min_2 = min_1
            break
        elif col[i] == min_1:
            snd = True
        elif col[i] < min_2:
            min_2 = col[i]

    return min_2


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


def mvg(a, n, s):
    str_mins = redux_strs(a, n)
    col_mins = redux_cols(a, n)

    nodes = []
    heapq.heappush(nodes, TreeNode([], [], sum(str_mins) + sum(col_mins), 0, a))
    # наибольший будет последним в куче
    while True:
        node = nodes[0]

        max_penalty = float('-inf')
        max_penalty_el = ()
        for i in range(n):
            for j in range(n):
                if i not in node.v_from and j not in node.v_to and node.cur_matr[i][j] == 0:
                    penal = snd_min_str(node.cur_matr, i, n, node.v_to) \
                            + snd_min_col(node.cur_matr, j, n, node.v_from)
                    if penal > max_penalty:
                        max_penalty = penal
                        max_penalty_el = (i, j)

        if max_penalty == float('-inf'):
            continue

        v_from_t = node.v_from[::]
        v_to_t = node.v_to[::]
        cur_matr_t = copy.deepcopy(node.cur_matr)
        v_from_t.append(max_penalty_el[0])
        v_to_t.append(max_penalty_el[1])
        fr = node.v_to[-1] if node.v_to else 0
        if fr != 0:
            cur_matr_t[max_penalty_el[1]][max_penalty_el[0]] = float('inf')
        str_mins_t = redux_strs(cur_matr_t, n, v_from_t, v_to_t)
        col_mins_t = redux_cols(cur_matr_t, n, v_from_t, v_to_t)
        cur_cost_t = sum(str_mins_t) + sum(col_mins_t) + node.cost

        node_t = TreeNode(v_from_t, v_to_t, cur_cost_t, node.level + 1, cur_matr_t)
        node_dt = None
        if node.v_from:
            cur_matr = copy.deepcopy(node.cur_matr)
            cur_matr[max_penalty_el[0]][max_penalty_el[1]] = float('inf')
            str_mins = redux_strs(cur_matr, n, node.v_from, node.v_to)
            col_mins = redux_cols(cur_matr, n, node.v_from, node.v_to)
            cur_cost = sum(str_mins) + sum(col_mins) + node.cost

            node_dt = TreeNode(node.v_from, node.v_to, cur_cost, node.level + 1, cur_matr)

        zero_new = True
        if node_dt is not None and not contain_node(nodes, node_dt) and node_dt.cost != float('inf'):
            heapq.heappush(nodes, node_dt)
            zero_new = False
        if not contain_node(nodes, node_t) and node_t.cost != float('inf'):
            heapq.heappush(nodes, node_t)
            zero_new = False
        if zero_new:
            break

    ans_node = heapq.heappop(nodes)

    if ans_node.cost > 0 and ans_node.cost != float('inf'):
        print(ans_node.cost)
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
    for i in range(n):
        for j in range(n):
            a[i][j] -= s
            a[i][j] *= -1 if a[i][j] != float('inf') else 1

    if n > 1:
        mvg(a, n, s)
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
    ], 14)
    print("граф из двух вершин есть путь назад (ср):")
    main(2, [
        [float('inf'), 3],
        [12, float('inf')]
    ], 4)
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
    ], 20)
    print("граф из n(5) вершин, полный (ср):")
    main(5, [
        [float('inf'), 3, 8, 2, 2],
        [5, float('inf'), 4, 17, 9],
        [3, 6, float('inf'), 15, 2],
        [2, 14, 10, float('inf'), 12],
        [8, 3, 4, 9, float('inf')]
    ], 8)
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
    ], 20)
    print("граф из n(5) вершин, первый город изолирован (ср):")
    main(5, [
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 4, 17, 9],
        [float('inf'), 6, float('inf'), 15, 2],
        [float('inf'), 14, 10, float('inf'), 12],
        [float('inf'), 3, 4, 9, float('inf')]
    ], 7)
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
    ], 12)
    print("граф из n(5) вершин, неполный (ср):")
    main(5, [
        [float('inf'), 4, 5, float('inf'), 3],
        [3, float('inf'), 6, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [8, 6, float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), 9, float('inf')]
    ], 5)
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
    ], 12)
    print("граф из n(5) вершин, неполный, без циклов и пути в А (ср):")
    main(5, [
        [float('inf'), 4, 5, float('inf'), 3],
        [float('inf'), float('inf'), 6, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 8, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')]
    ], 5)
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
    ], 12)
    print(
        "граф из n(5) вершин, неполный, можно вернуться только из первого перехода, проход через А невыгоден (ср):")
    main(5, [
        [float('inf'), 4, 5, float('inf'), 3],
        [7, float('inf'), 6, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 8, float('inf'), float('inf')],
        [4, float('inf'), float('inf'), float('inf'), float('inf')]
    ], 5)
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
    ], 12)
    print(
        "граф из n(5) вершин, неполный, можно вернуться только из первого перехода, проход через А выгоден (ср):")
    main(5, [
        [float('inf'), 9, 8, float('inf'), 10],
        [4, float('inf'), 8, float('inf'), float('inf')],
        [float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
        [float('inf'), float('inf'), 8, float('inf'), float('inf')],
        [4, float('inf'), float('inf'), float('inf'), float('inf')]
    ], 7)
    # main()

