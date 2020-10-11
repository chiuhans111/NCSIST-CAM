import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d  # 3d visualization


def plot(n_pos, n_vec, b_pos, b_vec, a_pos, a_vec, origin, scale=0.5):
    # 由給定座標系統，繪製機器簡單棒狀模型圖
    # n_pos: 刀具位置
    # n_vec: 刀具法向量
    # b_pos: 副旋轉軸位置
    # b_vec: 副旋轉軸向量
    # a_pos: 主旋轉軸位置
    # a_vec: 主旋轉軸向量
    # origin: 機器原點
    # scale: 法向量長度
    # 繪製圖中，黑色為原點，藍色為主轉軸，綠色為副轉軸，紅色為刀具
    
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot3D(*np.array([origin, a_pos, b_pos, n_pos]).T, c='black')
    ax.scatter3D(*np.array([origin, a_pos, b_pos, n_pos]
                           ).T, c=["black", "blue", "green", "red"])

    ax.plot3D(*np.array([n_pos, n_pos+n_vec*scale]).T, c="red")
    ax.plot3D(*np.array([b_pos, b_pos+b_vec*scale]).T, c='green')
    ax.plot3D(*np.array([a_pos, a_pos+a_vec*scale]).T, c='blue')

    # center camera

    lim = np.array([ax.get_xlim(), ax.get_ylim(), ax.get_zlim()])
    center = np.mean(lim, axis=1)
    radius = np.max(lim[:, 1]-lim[:, 0])/2
    ax.plot3D(*np.array([center+radius, center-radius]).T, alpha=0)

    return fig, ax
