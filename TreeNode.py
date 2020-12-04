import copy


class TreeNode:
    def __init__(self, v_from, v_to, cost, level, cur_matr):
        """
        :param v_from: вершины, из которых перешли
        :param v_to: вершины, в которые ходили
        :param cost: суммарная цена пути
        :param level: уровень
        :param cur_matr: текущая матрица
        """
        self.v_from = copy.deepcopy(v_from)
        self.v_to = copy.deepcopy(v_to)
        self.cost = cost
        self.level = level
        self.cur_matr = copy.deepcopy(cur_matr)

    def __lt__(self, other):
        return self.cost < other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def __eq__(self, other):
        return self.cost == other.cost

    def __ne__(self, other):
        return self.cost != other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __ge__(self, other):
        return self.cost >= other.cost
