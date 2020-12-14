from cam5axis_old import solver
from cam5axis_old.Machine import Machine
from cam5axis_old.utils import norm
from cam5axis_old.visualize import plot

import numpy as np
import matplotlib.pyplot as plt

m = Machine()

t = np.linspace(0, np.pi*2, 200)

CLdata = np.array([
    t*0,
    t*0,
    t*0,
    np.sin(t*5),
    np.cos(t*5),
    np.cos(t)
]).T

CLdata[:, 3:] = norm(CLdata[:, 3:])

solve, error = solver.backward(m, CLdata)

CLdata1 = solver.foward(m, solve[0])

diff = np.max(CLdata1 - CLdata, axis=1)

print(error)
plt.scatter(CLdata[:, 4], error, s=4)
plt.show()


simulation = solver.simulate(m, solve[0])
i = 0

# plot(*simulation[0])
# plt.show()

for data in simulation:
    fig, ax = plot(*data)

    center = np.array([0,0,1.5])
    radius = 2.5
    ax.plot3D(*np.array([center+radius,center-radius]).T, alpha=0)


    plt.savefig("./render/{:04d}.png".format(i))
    plt.close()
    # plt.pause(0.01)
    print(i)
    i+=1
