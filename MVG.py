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


def main():
    n = int(input())
    a = [[float(cost) for cost in input().replace("~", "inf").split()] for _ in range(n)]
    origin = copy.deepcopy(a)
    s = int(input())

    str_mins = redux_strs(a, n)
    col_mins = redux_cols(a, n)

    nodes = []
    heapq.heappush(nodes, TreeNode([], [], sum(str_mins) + sum(col_mins), 0, a))

    while True:
        node = nodes[0]
        if node.level == n:
            break

        heapq.heappop(nodes)
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

        v_from_t = node.v_from[::]
        v_to_t = node.v_to[::]
        cur_matr_t = copy.deepcopy(node.cur_matr)
        v_from_t.append(max_penalty_el[0])
        v_to_t.append(max_penalty_el[1])
        cur_matr_t[max_penalty_el[1]][max_penalty_el[0]] = float('inf')
        str_mins_t = redux_strs(cur_matr_t, n, v_from_t, v_to_t)
        col_mins_t = redux_cols(cur_matr_t, n, v_from_t, v_to_t)
        cur_cost_t = sum(str_mins_t) + sum(col_mins_t) + node.cost

        """
        sum_t = 0
        for i in range(n):
            for j in range(n):
                if i in v_from_t and j in v_to_t and origin[i][j] != float('inf'):
                    sum_t += origin[i][j]
        cur_cost_t = len(v_from_t) * s + node.cost - sum_t
        """

        node_t = TreeNode(v_from_t, v_to_t, cur_cost_t, node.level + 1, cur_matr_t)

        cur_matr = copy.deepcopy(node.cur_matr)
        cur_matr[max_penalty_el[0]][max_penalty_el[1]] = float('inf')
        str_mins = redux_strs(cur_matr, n, node.v_from, node.v_to)
        col_mins = redux_cols(cur_matr, n, node.v_from, node.v_to)
        cur_cost = sum(str_mins) + sum(col_mins) + node.cost

        """
        sum_dt = 0
        for i in range(n):
            for j in range(n):
                if i in node.v_from and j in node.v_to and origin[i][j] != float('inf'):
                    sum_dt += origin[i][j]
        cur_cost = len(node.v_from) * s + node.cost - sum_dt
        """

        node_dt = TreeNode(node.v_from, node.v_to, cur_cost, node.level + 1, cur_matr)

        heapq.heappush(nodes, node_dt)
        heapq.heappush(nodes, node_t)

    ans_node = heapq.heappop(nodes)

    print(ans_node.cost)
    for i in range(n):
    # for i in range(len(ans_node.v_to)):
        print("{}->{}".format(ans_node.v_from[i] + 1, ans_node.v_to[i] + 1), end="  ")


if __name__ == "__main__":
    main()

