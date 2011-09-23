import pygame, math, random, sprite

def load_image (path):
    surface = pygame.image.load(path)
    surface.convert()
    pygame.surfarray.pixels3d(surface)[:,:,0:1:2] = 0
    return surface

class Game (object):
    
    def __init__ (self, player_a, player_b, configuration):
        self.player_a = player_a
        self.player_b = player_b
        self.configuration = configuration
        self.background = pygame.Surface(configuration['screen_size'])
        self.sprites = pygame.sprite.OrderedUpdates()
        line = sprite.Line(load_image(configuration['line_image']), self.sprites)
        line.position = ((configuration['screen_size'][0]-line.width)/2, 0)
        paddle_image = load_image(configuration['paddle_image'])
        bounds_y = configuration['screen_size'][1] - paddle_image.get_height()
        self.paddle_a = sprite.Paddle(configuration['paddle_velocity'], paddle_image, bounds_y, self.sprites)
        self.paddle_b = sprite.Paddle(configuration['paddle_velocity'], paddle_image, bounds_y, self.sprites)
        digit_images = [load_image(configuration['digit_image'] % n) for n in xrange(10)]
        self.score_a = sprite.Score(digit_images, self.sprites)
        self.score_a.position = configuration['score_a_position']
        self.score_b = sprite.Score(digit_images, self.sprites)
        self.score_b.position = configuration['score_b_position']
        ball_image = load_image(configuration['ball_image'])
        self.bounds = pygame.Rect(0, 0, configuration['screen_size'][0]-ball_image.get_width(), configuration['screen_size'][1]-ball_image.get_height())
        self.ball = sprite.Ball(ball_image, self.bounds, self.sprites)
        self.reset_game(True)
        self.running = True
        
    def reset_game (self, reset_paddles=False):
        if reset_paddles:
            self.paddle_a.position = (self.configuration['paddle_a_position'], (self.configuration['screen_size'][1]-self.paddle_a.height)/2)
            self.paddle_b.position = (self.configuration['paddle_b_position'], (self.configuration['screen_size'][1]-self.paddle_a.height)/2)
        self.ball.position = ((self.configuration['screen_size'][0]-self.ball.width)/2, (self.configuration['screen_size'][1]-self.ball.height)/2)
        a = random.random() * math.pi / 2. - math.pi / 4.
        self.ball.velocity[0] = 3 * math.cos(a)
        self.ball.velocity[1] = 3 * math.sin(a)
        if random.random() < 0.5:
            self.ball.velocity[0] = -self.ball.velocity[0]
        
    def update (self):
        self.sprites.update()
        self.player_a.update(self.paddle_a, self)
        self.player_b.update(self.paddle_b, self)
        
        if self.ball.position[0] < self.paddle_a.position[0]:
            self.score_b.score += 1
            self.reset_game()
        if self.ball.position[0] > self.paddle_b.position[0] + self.paddle_b.rect.width:
            self.score_a.score += 1
            self.reset_game()
        
    def draw (self, display_surface):
        self.sprites.clear(display_surface, self.background)
        return self.sprites.draw(display_surface)
