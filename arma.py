import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront
import numpy as np


def load_model(path):
    return pywavefront.Wavefront(path, collect_faces=True)


def load_texture(texture_path):
    texture_surface = pygame.image.load(texture_path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)

    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_surface.get_width(), texture_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    
   
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
    return texture_id


def set_silver_material_with_contrast():
    silver_ambient = [0.1, 0.1, 0.1, 1.0]  
    silver_diffuse = [0.7, 0.7, 0.7, 1.0]  
    silver_specular = [0.8, 0.8, 0.8, 1.0]  
    silver_shininess = [100.0]  

    glMaterialfv(GL_FRONT, GL_AMBIENT, silver_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, silver_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, silver_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, silver_shininess)


class Weapon:
    def __init__(self, model_path, texture_path):
        self.model = load_model(model_path)
        self.texture = load_texture(texture_path)  
        self.rotation_x = 0
        self.rotation_y = 0

    def draw(self):
        glPushMatrix()
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        glBindTexture(GL_TEXTURE_2D, self.texture)  

        
        glBegin(GL_TRIANGLES)
        for mesh in self.model.mesh_list:
            for face in mesh.faces:
                for vertex_index in face:
                    vertex = self.model.vertices[vertex_index]
                    glTexCoord2f(0.0, 0.0)  
                    glVertex3fv(vertex)
        glEnd()
        glPopMatrix()


def init_pygame():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -15)

def main():
    
    init_pygame()

    
    
    weapon = Weapon("arma/arma.obj", "textures/textura.png") 

    
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    mouse_sensitivity = 0.2
    clock = pygame.time.Clock()

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        
        mouse_movement = pygame.mouse.get_rel()
        weapon.rotation_y += mouse_movement[0] * mouse_sensitivity
        weapon.rotation_x -= mouse_movement[1] * mouse_sensitivity

        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        weapon.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
