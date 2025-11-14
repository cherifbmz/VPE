import numpy as np


def projection(x,y,z,K):
    point=np.array([x/z,y/z,1])
    m=np.dot(K,point)
    u=int(m[0])
    v=int(m[1])
    return u,v

