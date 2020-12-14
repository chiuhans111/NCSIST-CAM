from NCSolver.Machine import *
import numpy as np
m = Machine()


print(m.foward([0,0,0,0,0]))
print(m.foward([1,0,0,0,0]))
print(m.foward([0,2,0,0,0]))
print(m.foward([0,0,3,0,0]))
print(m.foward([0,0,0,np.pi/2,0]))
print(m.foward([0,0,0,0,np.pi/2]))

print("\n\n")

print(m.solve([0,1,0],[0,0,1]))
print(m.solve([0,1,0],[1,0,0]))