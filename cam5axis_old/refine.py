import numpy as np
from cam5axis.Machine import Machine
from cam5axis.utils import *

# TODO: finish this....

def refine(m:Machine, solve, error,):

    max_limit = np.array([[m.x.max, m.y.max, m.z.max, m.a.max, m.b.max]])
    min_limit = np.array([[m.x.min, m.y.min, m.z.min, m.a.min, m.b.min]])

    error0 = np.logical_or(solve[0]>max_limit, solve[0]<min_limit)
    error1 = np.logical_or(solve[1]>max_limit, solve[1]<min_limit)


