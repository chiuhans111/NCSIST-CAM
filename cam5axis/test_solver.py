import NCSolver.Solver as solver
import numpy as np

A = np.array([0, 0, 1], "float64")
B = np.array([1, 0, 0], "float64")

print(solver.Rotation_Solver(A, B, [0, 0, 1], np.array([0, 0, 1])))
print(solver.Rotation_Solver(A, B, [0, 0, 1], np.array([0, 1, 1])))
print(solver.Rotation_Solver(A, B, [0, 0, 1], np.array([0, 1, 0])))
print(solver.Rotation_Solver(A, B, [0, 0, 1], np.array([1, 1, 1])))
print(solver.Rotation_Solver(A, B, [0, 0, 1], np.array([1, 0, 0])))
