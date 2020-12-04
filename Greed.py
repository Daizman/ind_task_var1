from TreeNode import TreeNode


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


def main(n=None, a=None, s=None):
    if n is None:
        n = int(input())
        a = [[float(cost) for cost in input().replace("~", "inf").split()] for _ in range(n)]
        if n == 0:
            input()
        s = int(input())
    e = []
    max_v = 0
    max_v_inf = ()
    for i in range(n):
        e_st = []
        for j in range(n):
            # cst = s/(a[i][j] + a[j][i]) if i != j else 0
            cst = s/a[i][j] if i != j and a[j][i] != float('inf') else 0
            e_st.append(cst)
            if cst > max_v and i == 0:
                max_v = cst
                max_v_inf = (i, j)
        e.append(e_st)

    if max_v <= 1:
        print("{}")
    else:
        node = TreeNode([max_v_inf[0]], [max_v_inf[1]], s - a[max_v_inf[0]][max_v_inf[1]], 1, a)
        node.cur_matr[max_v_inf[0]][max_v_inf[1]] = float('inf')
        while True:
            max_potential = float('-inf')
            max_potential_inf = ()
            cur_node_gr = node.v_to[-1]

            for i in range(n):
                if i not in node.v_from and s / node.cur_matr[cur_node_gr][i] > 1:
                    potential = s / node.cur_matr[i][0] + s / node.cur_matr[cur_node_gr][i] if node.cur_matr[i][0] != float('inf') else 0
                    if potential > max_potential:
                        max_potential = potential
                        max_potential_inf = (cur_node_gr, i)

            if max_potential < 1:
                node.cost -= a[node.v_to[-1]][node.v_from[-1]]
                node.v_from.append(node.v_to[-1])
                node.cur_matr[node.v_to[-1]][0] = float('inf')
                node.v_to.append(0)
                break
            else:
                node.v_from.append(max_potential_inf[0])
                node.v_to.append(max_potential_inf[1])
                node.cur_matr[max_potential_inf[0]][max_potential_inf[1]] = float('inf')
                node.cost += s - a[max_potential_inf[0]][max_potential_inf[1]]

        if node.cost > 0:
            print(node.cost)
            for i in range(len(node.v_to)):
                print("{}->{}".format(node.v_from[i] + 1, node.v_to[i] + 1), end="  ")
            print()
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
