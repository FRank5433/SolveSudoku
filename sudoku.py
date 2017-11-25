# -*- coding: utf-8 -*-

"""
尝试使用非暴力的形式将数独解出
"""

from copy import deepcopy

RESULT = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class Sudoku:
    def __init__(self):
        self.matrix = []

    def read_init_problems_from_files(self, file_name):
        file = open("./problems/" + file_name, "r")
        file_data = file.read().split('\n')
        file.close()

        number_count = 0
        for r in file_data:
            self.matrix.append([])
            for c in range(len(r)):
                number = int(r[c])
                if number != 0:
                    number_count += 1
                self.matrix[-1].append(number)
        print("读取题目完毕。共读取数字%s个。\n" % number_count)

    def print_matrix_script(self):
        print("目前矩阵如下：")
        for ix in self.matrix:
            print(ix)
        print()

    def solve_the_problem(self):
        last_matrix_result = deepcopy(self.matrix)
        count = 0
        while True:
            count += 1
            print("开始进行第%s次循环计算\n" % str(count))
            for row_iter in range(9):
                for column_iter in range(9):
                    if self.matrix[row_iter][column_iter] in RESULT:
                        pass
                    elif self.matrix[row_iter][column_iter] == 0:
                        last_possible_result = set()
                        possible_result = self._get_a_cell_possible_result(last_possible_result, row_iter, column_iter)
                        if len(possible_result) == 1:
                            print("由于第%s行第%s列只可填入%s，所以确定其值为%s. \n" % (
                                row_iter + 1, column_iter + 1, possible_result[0], possible_result[0]))
                            self.matrix[row_iter][column_iter] = possible_result[0]
                        elif len(possible_result) == 0:
                            raise ValueError("没有可能的结果！逻辑错误！")
                        else:
                            self.matrix[row_iter][column_iter] = set(possible_result)
                    elif isinstance(self.matrix[row_iter][column_iter], set):
                        last_possible_result = deepcopy(self.matrix[row_iter][column_iter])
                        possible_result = self._get_a_cell_possible_result(last_possible_result, row_iter, column_iter)
                        if len(possible_result) == 1:
                            print("由于第%s行第%s列只可填入%s，所以确定其值为%s. \n" % (
                                row_iter + 1, column_iter + 1, possible_result[0], possible_result[0]))
                            self.matrix[row_iter][column_iter] = possible_result[0]
                        elif len(possible_result) == 0:
                            raise ValueError("没有可能的结果！逻辑错误！")
                        else:
                            self.matrix[row_iter][column_iter] = set(possible_result)

            if self.matrix == last_matrix_result:
                for ix in self.matrix:
                    for iix in ix:
                        if isinstance(iix, set):
                            print("进入死循环，无法解出答案")
                            return -1
                print("已经解出结果，", end="")
                self.print_matrix_script()
                return 0
            last_matrix_result = deepcopy(self.matrix)

    def _get_a_cell_possible_result(self, last_possible_result, r, c):
        pure = []
        print("确定第%s行第%s列的可能的值：" % (str(r + 1), str(c + 1)))
        if last_possible_result:
            print("之前确定过的可能的值有：" + ",".join([str(x) for x in last_possible_result]))
            pa = deepcopy(RESULT)
            for x in last_possible_result:
                if x in pa:
                    pa.remove(x)
            pure = pa

        for i, ix in enumerate(self.matrix[r]):
            if ix in RESULT:
                if ix not in pure:
                    print("由于第%s行第%s列已存在值%s，所以第%s行第%s列不可能为%s" % (r + 1, i + 1, ix, r + 1, c + 1, ix))
                    pure.append(ix)

        for ixx in range(9):
            if self.matrix[ixx][c] in RESULT:
                if self.matrix[ixx][c] not in pure:
                    print("由于第%s行第%s列已存在值%s，所以第%s行第%s列不可能为%s" % (
                        ixx + 1, c + 1, self.matrix[ixx][c], r + 1, c + 1, self.matrix[ixx][c]))
                    pure.append(self.matrix[ixx][c])

        r_b = r // 3
        c_b = c // 3

        for row_iter in range(r_b * 3, r_b * 3 + 3):
            for column_iter in range(c_b * 3, c_b * 3 + 3):
                _tmp = self.matrix[row_iter][column_iter]
                if _tmp in RESULT:
                    if _tmp not in pure:
                        print("由于第%s行第%s列已存在值%s，所以第%s行第%s列不可能为%s" % (
                            row_iter + 1, column_iter + 1, _tmp, r + 1, c + 1, _tmp))
                        pure.append(_tmp)

        p = deepcopy(RESULT)
        for x in pure:
            if x in p:
                p.remove(x)

        if set(p) == set(last_possible_result):
            print("可能的值无变化，第%s行第%s列的值可能为：" % (r + 1, c + 1) + ",".join([str(x) for x in p]) + "\n")
        else:
            print("第%s行第%s列的值可能为：" % (r + 1, c + 1) + ",".join([str(x) for x in p]) + "\n")

        return p


if __name__ == "__main__":
    a_sudoku = Sudoku()
    a_sudoku.read_init_problems_from_files('easy_1')
    a_sudoku.print_matrix_script()
    a_sudoku.solve_the_problem()
