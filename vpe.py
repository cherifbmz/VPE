import numpy as np
import math



class Representation3D:
    def __init__(self, sommets, aretes):
        self.sommets = np.array(sommets, dtype=float) 
        self.aretes = aretes  

cube_sommets = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1]
]
cube_aretes = [
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,6),(6,7),(7,4),
    (0,4),(1,5),(2,6),(3,7)
]
CUBE = Representation3D(cube_sommets, cube_aretes)


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
# function de transformation
def WTC(M, R, t):
    return np.dot(R, M) + t






