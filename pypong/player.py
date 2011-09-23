import pygame

class BasicAIPlayer (object):

    def update (self, paddle, game):
        if (paddle.x < game.bounds.centerx and game.ball.x < game.bounds.centerx) or (paddle.x > game.bounds.centerx and game.ball.x > game.bounds.centerx):
            if paddle.y > game.ball.bottom:
                paddle.direction = -1
            elif paddle.bottom < game.ball.y:
                paddle.direction = 1
            else:
                paddle.direction = 0
        else:
            paddle.direction = 0

class KeyboardPlayer (object):
    
    def __init__ (self, input_state, up_key=None, down_key=None):
        self.input_state = input_state
        self.up_key = up_key
        self.down_key = down_key
        
    def update (self, paddle, game):
        if self.input_state['key'][self.up_key]:
            paddle.direction = -1
        elif self.input_state['key'][self.down_key]:
            paddle.direction = 1
        else:
            paddle.direction = 0
        
class MousePlayer (object):
    
    def __init__ (self, input_state):
        self.input_state = input_state
        pygame.mouse.set_visible(False)
        
    def update (self, paddle, game):
        centery = (paddle.y+paddle.height/2)/int(paddle.velocity)
        mousey = self.input_state['mouse'][1]/int(paddle.velocity)
        if centery > mousey:
            paddle.direction = -1
        elif centery < mousey:
            paddle.direction = 1
        else:
            paddle.direction = 0
        