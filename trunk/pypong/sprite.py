import pygame
from pygame.sprite import Sprite

class BaseGameSprite (Sprite):
    
    def set_position (self, position):
        self.rect.topleft = position
    def get_position (self):
        return self.rect.topleft
    position = property(get_position, set_position)
    
    def set_x (self, value):
        self.rect.left = value
    x = property(lambda self: self.rect.left, set_x)
    
    def set_y (self, value):
        self.rect.top = value
    y = property(lambda self: self.rect.top, set_y)
    
    height = property(lambda self: self.rect.height)
    width = property(lambda self: self.rect.width)
    bottom = property(lambda self: self.rect.bottom)
    right = property(lambda self: self.rect.right)
    
class Paddle (BaseGameSprite):
    def __init__ (self, velocity, image, bounds_y, *groups):
        Sprite.__init__(self, *groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.direction = 0
        self.velocity = velocity
        self.bounds_y = bounds_y
        
    def update (self):
        self.rect.y = max(0, min(self.bounds_y, self.rect.y + self.direction * self.velocity))

class Line (BaseGameSprite):
    def __init__ (self, image, *groups):
        Sprite.__init__(self, *groups)
        self.image = image
        self.rect = self.image.get_rect()

class Ball (BaseGameSprite):
    def __init__ (self, image, bounds, *groups):
        Sprite.__init__(self, *groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.velocity = [0.,0.]
        self.bounds = bounds
        
    def update (self):
        self.rect.x =  self.rect.x + self.velocity[0]
        self.rect.y =  self.rect.y + self.velocity[1]
        if self.rect.y < self.bounds.top:
            self.rect.y = self.bounds.top
            self.velocity[1] = -self.velocity[1]
        elif self.rect.y > self.bounds.bottom:
            self.rect.y = self.bounds.bottom
            self.velocity[1] = -self.velocity[1]
    
class Score (BaseGameSprite):
    def __init__ (self, image_list, *groups):
        Sprite.__init__(self, *groups)
        self.image_list = image_list
        self.image = None
        self.rect = pygame.Rect(0,0,0,0)
        self.score = 0
    
    def get_score (self):
        return self.score_value
        
    def set_score (self, value):
        self.score_value = value
        digit_spacing = 8
        digit_width = self.image_list[0].get_width()
        digit_height = self.image_list[0].get_height()
        values = [int(i) for i in list(str(self.score_value))]
        values.reverse()
        surface_width = len(values) * digit_width + (len(values)-1) * digit_spacing
        if not self.image or self.image.get_width() < surface_width:
            self.image = pygame.Surface((surface_width, digit_height))
            self.image.fill((0,0,0))
            self.rect.width = self.image.get_width()
            self.rect.height = self.image.get_height()
        offset = self.image.get_width()-digit_width
        for i in values:
            self.image.blit(self.image_list[i], (offset, 0))
            offset = offset - (digit_width + digit_spacing)
        
    score = property(get_score, set_score)
