import pygame
import os


class ElementoSprite(pygame.sprite.Sprite):
    """
    Esta é a classe básica de todos os objetos do jogo.
    """

    def __init__(self, image, position, speed=None, new_size=None, new_angle=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.angle = 0
        self.uptade_ = True
        if isinstance(self.image, str):
            self.image = os.path.join('imagens', self.image)
            self.image = pygame.image.load(self.image)
        if new_size:
            self.scale(new_size)
        if new_angle:
            self.rotate_inicial(new_angle) 
            
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.set_pos(position)
        self.set_speed(speed or (0, 2))
        
    def update(self, dt):
        
        if self.uptade_ == True:
            
            move_speed = (self.speed[0] * dt / 16,
                          self.speed[1] * dt / 16)
            self.rect = self.rect.move(move_speed)
            if (self.rect.left > self.area.right) or \
                    (self.rect.top > self.area.bottom) or \
                    (self.rect.right < 0):
                self.kill()
            if (self.rect.bottom < - 40):
                self.kill()

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def get_pos(self):
        return (self.rect.center[0], self.rect.center[1])

    def set_pos(self, pos):
        self.rect.center = (pos[0], pos[1])

    def get_size(self):
        return self.image.get_size()

    def scale(self, new_size):
        self.image = pygame.transform.scale(self.image, new_size)
        
    def get_angle(self):
        return self.angle

    def rotate_inicial(self, new_angle):
        self.image = pygame.transform.rotate(self.image, new_angle)
        
    def opacidade(self, alpha):
        self.image.set_alpha(alpha)
        
    def rotate(self, old_angle, new_angle):
        angle = new_angle - old_angle
        self.image = pygame.transform.rotate(self.image, angle)
        self.angle = new_angle
        """
        if abs(angle) != 180:
            aux = self.rect.w
            self.rect.w = self.rect.h
            self.rect.h = aux
        """
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)