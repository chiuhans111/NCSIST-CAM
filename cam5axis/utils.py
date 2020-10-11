import numpy as np


def rotation_matrix(normal, angle):
    # 製作旋轉矩陣的函數
    # normal: 旋轉軸法向量
    # angle: 旋轉角度 (弧度)
    # 參考 https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
    angle = np.reshape(angle, -1)
    normal = np.reshape(normal, [-1, 3])

    a = np.ones([1, 3, 3]) * np.reshape((1-np.cos(angle)), [-1, 1, 1])
    x = normal[:, :, np.newaxis] * normal[:, np.newaxis, :]
    b = np.moveaxis(np.array([
        [np.cos(angle),
         -normal[:, 2] * np.sin(angle),
         +normal[:, 1] * np.sin(angle)],
        [+normal[:, 2] * np.sin(angle),
         np.cos(angle),
         -normal[:, 0] * np.sin(angle)],
        [-normal[:, 1] * np.sin(angle),
         +normal[:, 0] * np.sin(angle),
         np.cos(angle)],
    ]), 2, 0)
    return a * x + b


def norm(vector):
    # 正規化向量 (向量除以長度)
    return vector/np.sqrt(np.sum(vector**2, axis=-1, keepdims=True))


def angle(vector1, vector2, axis):

    vector1 = np.reshape(vector1, [-1, 3])
    vector2 = np.reshape(vector2, [-1, 3])
    axis = np.reshape(axis, [-1, 3])

    # 計算 vector1 到 vector2 以 axis 方向看入的夾角角度

    vector1 = vector1 - axis * np.sum(vector1 * axis, axis=1, keepdims=True)
    vector2 = vector2 - axis * np.sum(vector2 * axis, axis=1, keepdims=True)
    s = np.sum(np.cross(vector1, vector2) * axis, axis=1)
    c = np.sum(vector1 * vector2, axis=1)
    return np.nan_to_num(np.arctan2(s, c), 0)


def matmul(A, B):
    A = np.expand_dims(A, 3)
    B = np.expand_dims(B, 3)
    A = np.swapaxes(A, 3, 2)
    B = np.swapaxes(B, 3, 1)
    return np.sum(A*B, axis=3)

def matvecmul(A, B):
    B = np.expand_dims(B, 2)
    return matmul(A, B)[:, :, 0]
