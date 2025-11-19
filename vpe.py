import numpy as np
import math
import pygame



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

def K_matrice(f,u0,v0):
    return np.array([
        [f,0,u0],
        [0,f,v0],
        [0,0,1]
    ])    
# function de transformation
def WTC(M, R, t):
    return np.dot(R, M) + t

def project_point_camera(x, y, z, K):
    if z <= 0:
        return None
    homog = np.array([x/z, y/z, 1])
    m = np.dot(K, homog)
    return int(m[0]), int(m[1])

def project_point_world(M, K, R, t):
    X_cam = WTC(M, R, t)      
    return project_point_camera(          
        X_cam[0], X_cam[1], X_cam[2], K
    )

def rotation_x(angle):
    return np.array([
        [1,0,0],
        [0,np.cos(angle),-np.sin(angle)],
        [0,np.sin(angle),np.cos(angle)]
    ])

def rotation_y(angle):
    return np.array([
        [np.cos(angle),0,np.sin(angle)],
        [0,1,0],
        [-np.sin(angle),0,np.cos(angle)]
    ])

def rotation_z(angle):
    return np.array([
        [np.cos(angle),-np.sin(angle),0],
        [np.sin(angle),np.cos(angle),0],
        [0, 0, 1]
    ])





def rotation_combinee(angle_x, angle_y, angle_z):

    Rx = rotation_x(angle_x)  
    Ry = rotation_y(angle_y)  
    Rz = rotation_z(angle_z)   
    
    return np.dot(Rz, np.dot(Ry, Rx))  
