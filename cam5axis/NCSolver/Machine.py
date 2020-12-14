from .Axis import *
from .Solver import *
import numpy as np


class Machine:
    def __init__(self):
        """
        若軸配置在工件端而非手臂端，法線向量必須相反
        """
        self.axis_x = TranslateAxis(-100, 100, [1, 0, 0])
        self.axis_y = TranslateAxis(-100, 100, [0, 1, 0])
        self.axis_z = TranslateAxis(-100, 100, [0, 0, 1])
        self.axis_a = RotationAxis(-np.pi, np.pi, [0, 0, -1], [0, 0, -1])
        # A 比須為主旋轉軸 (與工件相對位置不改變)
        self.axis_b = RotationAxis(-np.pi, np.pi, [1, 0, 0], [0, 0, 2])
        # B 必須為副旋轉軸 (與刀具相對位置不改變)

        self.knife_position = np.array([0, 0, 1, 1])  # 刀具
        self.knife_normal = np.array([0, 0, 1, 0])  # 刀具

        """
        軸順序以工件端末端開始，依序到工件端根部
        再來是手臂端根部，最後是手臂端末端
        刀具一定是最末端。
        """
        self.operate_order = [
            self.axis_a,
            self.axis_x,
            self.axis_y,
            self.axis_z,
            self.axis_b
        ]

        self.axis_x_index = self.operate_order.index(self.axis_x)
        self.axis_y_index = self.operate_order.index(self.axis_y)
        self.axis_z_index = self.operate_order.index(self.axis_z)
        self.axis_a_index = self.operate_order.index(self.axis_a)
        self.axis_b_index = self.operate_order.index(self.axis_b)

    def foward(self, nc_data):
        nc_data = np.array(nc_data)
        mats = []
        for i, axis in enumerate(self.operate_order):
            mats.append(axis.transform_matrix(nc_data[i]))
        mat = np.linalg.multi_dot(mats)

        pos = np.dot(mat, self.knife_position)
        nor = np.dot(mat, self.knife_normal)
        return pos[:3], nor[:3]

    def solve(self, pos, nor):
        pos = np.array(pos)
        nor = np.array(nor)
        result = Rotation_Solver(
            self.axis_a.normal, self.axis_b.normal, self.knife_normal[:3], nor)

        solve = []

        for sol in result[0]:

            mat_x = mat_y = mat_z = np.identity(4)

            mat_a = self.axis_a.get_transform_matrix(sol[0])
            mat_b = self.axis_b.get_transform_matrix(sol[1])

            if self.axis_x_index > self.axis_b_index:
                mat_x = mat_b
            if self.axis_y_index > self.axis_b_index:
                mat_y = mat_b
            if self.axis_z_index > self.axis_b_index:
                mat_z = mat_b

            if self.axis_x_index > self.axis_a_index:
                mat_x = np.dot(mat_a, mat_x)
            if self.axis_y_index > self.axis_a_index:
                mat_y = np.dot(mat_a, mat_y)
            if self.axis_z_index > self.axis_a_index:
                mat_z = np.dot(mat_a, mat_z)

            displace = np.linalg.multi_dot([mat_a, mat_b, self.knife_position])
            offset = pos - displace[:3]

            print("offset=", offset)

            x_offset = np.dot(mat_x, np.append(self.axis_x.offset, 0))[:3]
            y_offset = np.dot(mat_y, np.append(self.axis_y.offset, 0))[:3]
            z_offset = np.dot(mat_z, np.append(self.axis_z.offset, 0))[:3]

            translate = Translate_Solver(x_offset, y_offset, z_offset, offset)

            solve.append([*translate, *sol])

        return solve, result[1]
