import numpy as np
from cam5axis.Machine import Machine
from cam5axis.utils import *


def simulate(m: Machine, NCdata):
    # 根據 NC data 計算機器所有軸方向與狀態 (正向)
    x = NCdata[:, 0]
    y = NCdata[:, 1]
    z = NCdata[:, 2]
    a = NCdata[:, 3]
    b = NCdata[:, 4]

    origin = [m.x.vec]*x[:, np.newaxis] + \
        [m.y.vec] * y[:, np.newaxis] + \
        [m.z.vec]*z[:, np.newaxis] + m.origin

    A = rotation_matrix(m.a.vec, a)  # 主轉軸旋轉矩陣
    B = rotation_matrix(m.b.vec, b)  # 副轉軸旋轉矩陣

    AB = matmul(A, B)

    n_pos = matvecmul(B, [m.n.pos - m.b.pos]) + m.b.pos
    n_pos = matvecmul(A, n_pos - m.a.pos) + m.a.pos
    n_pos += origin
    n_vec = norm(matvecmul(AB, [m.n.vec]))

    a_pos = m.a.pos + origin
    a_vec = np.repeat([m.a.vec], NCdata.shape[0], axis=0)

    b_pos = matvecmul(A, [m.b.pos - m.a.pos]) + m.a.pos + origin
    b_vec = norm(matvecmul(A, [m.b.vec]))



    return np.swapaxes(np.array([n_pos, n_vec, b_pos, b_vec, a_pos, a_vec, origin]), 0, 1)


def foward(m: Machine, NCdata):
    # 根據 NC data 計算機器所有軸方向與狀態 (正向)
    x = NCdata[:, 0]
    y = NCdata[:, 1]
    z = NCdata[:, 2]
    a = NCdata[:, 3]
    b = NCdata[:, 4]

    origin = [m.x.vec]*x[:, np.newaxis] + \
        [m.y.vec] * y[:, np.newaxis] + \
        [m.z.vec]*z[:, np.newaxis] + m.origin

    A = rotation_matrix(m.a.vec, a)  # 主轉軸旋轉矩陣
    B = rotation_matrix(m.b.vec, b)  # 副轉軸旋轉矩陣

    AB = matmul(A, B)

    n_pos = matvecmul(B, [m.n.pos - m.b.pos]) + m.b.pos
    n_pos = matvecmul(A, n_pos - m.a.pos) + m.a.pos
    n_pos += origin
    n_vec = norm(matvecmul(AB, [m.n.vec]))

    return np.concatenate([n_pos, n_vec], axis=1)


def backward(m: Machine, CLdata):
    # 由 CL data 反推 NC data
    # 核心演算法在此

    # x, y, z, nx, ny, nz

    pos = CLdata[:, :3]  # 目標刀具座標向量
    vec = norm(CLdata[:, 3:])  # 目標刀具法向量

    na = np.sum(vec * [m.a.vec], axis=1)  # 目標刀具法向量與主轉軸內積
    nb = np.dot(m.n.vec, m.b.vec)  # 原始刀具法向量與副轉軸內積

    a_dot_b = np.dot(m.a.vec, m.b.vec)  # 主轉軸與副轉軸內積

    # 求解：
    # 目標刀具繞主轉軸之圓 與 原始刀具繞副轉軸之圓 焦點

    u = (na - nb * a_dot_b) / (1 - a_dot_b**2)
    v = (nb - na * a_dot_b) / (1 - a_dot_b**2)
    C = [m.a.vec]*u[:, np.newaxis] + [m.b.vec]*v[:, np.newaxis]  # 兩焦點中心


    nsq = 1-np.sum(C**2, axis=1)

    error = nsq<0

    n = np.sqrt(nsq)  # 兩焦點中心 到 焦點距離
    N = norm(np.cross(m.a.vec,  m.b.vec))  # 中心到焦點方向向量為兩軸外積

    v1 = norm(C + [N] * n[:, np.newaxis])  # 兩圓焦點 1
    v2 = norm(C - [N] * n[:, np.newaxis])  # 兩圓焦點 2

    solve = []  # 此陣列用來存放求解結果

    xc = np.cross(m.y.vec, m.z.vec)
    yc = np.cross(m.z.vec, m.x.vec)
    zc = np.cross(m.x.vec, m.y.vec)

    v = np.dot(m.x.vec, xc)

    xc /= v
    yc /= v
    zc /= v

    for v in [v1, v2]:
        a = angle(v, vec, m.a.vec)  # 求主轉軸角度
        b = angle(m.n.vec, v, m.b.vec)  # 求副轉軸角度

        A = rotation_matrix(m.a.vec, a)  # 主轉軸旋轉矩陣
        B = rotation_matrix(m.b.vec, b)  # 副轉軸旋轉矩陣

        n_pos = matvecmul(B, [m.n.pos - m.b.pos]) + m.b.pos
        n_pos = matvecmul(A, n_pos - m.a.pos) + m.a.pos

        offset = pos - n_pos - m.origin  # 計算偏移向量

        x = np.dot(offset, xc)  # 第一平移軸
        y = np.dot(offset, yc)  # 第二平移軸
        z = np.dot(offset, zc)  # 第三平移軸

        solve.append(np.concatenate([[x, y, z, a, b]], axis=1).T)

    return solve, error
