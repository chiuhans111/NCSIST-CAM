import numpy as np


def norm(vector):
    # 正規化向量 (向量除以長度)
    return vector/np.sqrt(np.sum(vector**2))


def angle(vector1, vector2, axis):
    # 計算 vector1 到 vector2 以 axis 方向看入的夾角角度
    vector1 = vector1 - axis * np.dot(vector1, axis)
    vector2 = vector2 - axis * np.dot(vector2, axis)
    s = np.dot(np.cross(vector1, vector2), axis)
    c = np.dot(vector1, vector2)
    return np.nan_to_num(np.arctan2(s, c), 0)


def Rotation_Solver(axis1, axis2, vec1, vec2):
    """
    axis1: 主轉軸
    axis2: 副轉軸
    vec1: 刀具初始向量
    vec2: 目標工件向量
    """

    vec2 = norm(vec2)  # 目標刀具法向量

    na = np.dot(vec2, axis1)  # 目標刀具法向量與主轉軸內積
    nb = np.dot(vec1, axis2)  # 原始刀具法向量與副轉軸內積

    a_dot_b = np.dot(axis1, axis2)  # 主轉軸與副轉軸內積

    # 求解：
    # 目標刀具繞主轉軸之圓 與 原始刀具繞副轉軸之圓 焦點

    u = (na - nb * a_dot_b) / (1 - a_dot_b**2)
    v = (nb - na * a_dot_b) / (1 - a_dot_b**2)
    C = axis1*u + axis2*v  # 兩焦點中心

    nsq = 1-np.sum(C**2)

    success = True

    if nsq < 0:
        success = False
        nsq = 0

    n = np.sqrt(nsq)  # 兩焦點中心 到 焦點距離
    N = norm(np.cross(axis1,  axis2))  # 中心到焦點方向向量為兩軸外積

    v1 = norm(C + N * n)  # 兩圓焦點 1
    v2 = norm(C - N * n)  # 兩圓焦點 2

    solve = []  # 此陣列用來存放求解結果

    for v in [v1, v2]:
        a = angle(v, vec2, axis1)  # 求主轉軸角度
        b = angle(vec1, v, axis2)  # 求副轉軸角度

        solve.append([a, b])

    return solve, success


def Translate_Solver(x, y, z, offset):
    x_depend = np.cross(y, z)
    y_depend = np.cross(z, x)
    z_depend = np.cross(x, y)

    V = np.dot(x_depend, x)

    x_value = np.dot(x_depend, offset) / V
    y_value = np.dot(y_depend, offset) / V
    z_value = np.dot(z_depend, offset) / V

    return x_value, y_value, z_value
