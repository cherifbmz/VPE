import numpy as np
import math
import pygame
import cv2




class Representation3D:
    def __init__(self, sommets, aretes,faces):
        self.sommets = np.array(sommets, dtype=float) 
        self.aretes = aretes
        self.faces = faces  

cube_sommets = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1]
]
cube_aretes = [
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,6),(6,7),(7,4),
    (0,4),(1,5),(2,6),(3,7)
]
cube_faces = [
    (0, 1, 2, 3),  
    (4, 5, 6, 7),  
    (0, 1, 5, 4),  
    (2, 3, 7, 6),  
    (0, 3, 7, 4),  
    (1, 2, 6, 5)   
]
face_colors = [
    (255, 0, 0),    
    (0, 255, 0),    
    (0, 0, 255),    
    (255, 255, 0),  
    (255, 0, 255),  
    (0, 255, 255)   
]

CUBE = Representation3D(cube_sommets, cube_aretes,cube_faces)


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



def calculate_face_depth(face_vertices_3d):
    return np.mean([v[2] for v in face_vertices_3d])



def main():
    largeur_image, hauteur_image = 800,600
    u_0,v_0 = largeur_image // 2,hauteur_image // 2
    pygame.init()
    fenetre=pygame.display.set_mode((largeur_image,hauteur_image))
    noir=(0,0,0)
    clock=pygame.time.Clock()
    continuer=True
    f=400
    K=K_matrice(f,u_0,v_0)
    blanc=(255,255,255)
    angle_x=0
    angle_y=0
    angle_z=0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while continuer:
        
        
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.image.frombuffer(
        frame.tobytes(), frame.shape[1::-1], "RGB")
        fenetre.blit(frame_surface, (2,2))
        
        
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                continuer=False
        
        angle_x=angle_x+ 0.01
        angle_y=angle_x+0.015
        angle_z=angle_z+0.008
        R=rotation_combinee(angle_x, angle_y, angle_z)
        t=np.array([0,0,5])     


        vertices_3d_camera=[]
        for M in CUBE.sommets:
            X_cam = WTC(M,R,t)
            vertices_3d_camera.append(X_cam)

        points_2d=[]
        for X_cam in vertices_3d_camera:
            proj = project_point_camera(X_cam[0],X_cam[1],X_cam[2],K)
            if proj is not None:
                points_2d.append(proj)
            else:
                points_2d.append((-100,-100))
        

        faces_with_depth=[]
        for i, face in enumerate(CUBE.faces):
            face_verts_3d=[vertices_3d_camera[v] for v in face]
            avg_depth=calculate_face_depth(face_verts_3d)
            faces_with_depth.append((avg_depth,i,face)) 


        faces_with_depth.sort(reverse=True,key=lambda x:x[0])
        for depth,face_idx,face in faces_with_depth:
            face_points_2d=[points_2d[v] for v in face]
            if all(p[0]>= -100 and p[1] >= -100 for p in face_points_2d):   
                pygame.draw.polygon(fenetre,face_colors[face_idx],face_points_2d)
                pygame.draw.polygon(fenetre, blanc,face_points_2d,2)

        pygame.display.flip()
        clock.tick(60)
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()


if __name__ == "__main__":
    main()
    