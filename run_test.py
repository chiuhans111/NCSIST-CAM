from cam5axis import solver
from cam5axis.Machine import Machine
import numpy as np
from cam5axis.utils import norm
import matplotlib.pyplot as plt
from cam5axis.visualize import plot

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

result = solver.backward(m, CLdata)

CLdata1 = solver.foward(m, result[0])

error = np.max(CLdata1 - CLdata, axis=1)

# plt.scatter(CLdata[:, 4], error, s=4)
# plt.show()


simulation = solver.simulate(m, result[0])
i = 0


for data in simulation:
    fig, ax = plot(*data)

    center = np.array([0,0,1.5])
    radius = 2.5
    ax.plot3D(*np.array([center+radius,center-radius]).T, alpha=0)


    plt.savefig("./render/{:04d}.png".format(i))
    plt.close()
    print(i)
    i+=1
