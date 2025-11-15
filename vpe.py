import numpy as np


def projection(x,y,z,K):
    point=np.array([x/z,y/z,1])
    m=np.dot(K,point)
    u=int(m[0])
    v=int(m[1])
    return u,v

def K(f,u0,v0):
    return np.array([
        [f,0,u0],
        [0,f,v0],
        [0,0,1]
    ])    






