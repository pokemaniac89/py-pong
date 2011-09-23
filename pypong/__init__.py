import pygame, math, random, sprite

def load_image (path):
    surface = pygame.image.load(path)
    surface.convert()
    pygame.surfarray.pixels3d(surface)[:,:,0:1:] = 0
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
        self.ball = sprite.Ball(ball_image, self.sprites)
        self.bounds = pygame.Rect(20, 0, configuration['screen_size'][0]-ball_image.get_width()-20, configuration['screen_size'][1]-ball_image.get_height())
        self.sound_missed = pygame.mixer.Sound(configuration['sound_missed'])
        self.sound_paddle = pygame.mixer.Sound(configuration['sound_paddle'])
        self.sound_wall = pygame.mixer.Sound(configuration['sound_wall'])
        self.reset_game(True)
        self.running = True
        
    def play_sound (self, sound):
        sound.play()
        
    def reset_game (self, reset_paddles=False):
        if reset_paddles:
            self.paddle_a.position = (self.configuration['paddle_a_position'], (self.configuration['screen_size'][1]-self.paddle_a.height)/2)
            self.paddle_b.position = (self.configuration['paddle_b_position'], (self.configuration['screen_size'][1]-self.paddle_a.height)/2)
        self.ball.position = ((self.configuration['screen_size'][0]-self.ball.width)/2, (self.configuration['screen_size'][1]-self.ball.height)/2)
        a = random.random() * math.pi / 2. - math.pi / 4.
        self.ball.velocity[0] = self.configuration['ball_velocity'] * math.cos(a)
        self.ball.velocity[1] = self.configuration['ball_velocity'] * math.sin(a)
        if random.random() < 0.5:
            self.ball.velocity[0] = -self.ball.velocity[0]
        
    def update (self):
        # Collision check
        if self.ball.y < self.bounds.top:
            self.ball.y = self.bounds.top
            self.ball.velocity[1] = -self.ball.velocity[1]
            self.play_sound(self.sound_wall)
        elif self.ball.y > self.bounds.bottom:
            self.ball.y = self.bounds.bottom
            self.ball.velocity[1] = -self.ball.velocity[1]
            self.play_sound(self.sound_wall)
        # Update sprites and players
        self.sprites.update()
        self.player_a.update(self.paddle_a, self)
        self.player_b.update(self.paddle_b, self)
        
        if self.ball.x < self.bounds.centerx:
            # Left paddle
            if self.paddle_a.rect.colliderect(self.ball.rect) and self.ball.right > self.paddle_a.right:
                self.ball.x = self.paddle_a.right
                self.ball.velocity[0] = -self.ball.velocity[0]
                #~ delta = (self.ball.centery - self.paddle_a.centery) / (self.paddle_a.height / 2.0)
                self.ball.angle -= math.pi / 6.0 * random.random() * 0.5
                self.play_sound(self.sound_paddle)
        else:
            # Right paddle
            if self.paddle_b.rect.colliderect(self.ball.rect) and self.ball.x < self.paddle_b.x:
                self.ball.x = self.paddle_b.x - self.ball.width
                self.ball.velocity[0] = -self.ball.velocity[0]
                #~ delta = (self.ball.centery - self.paddle_b.centery) / (self.paddle_b.height / 2.0)
                self.ball.angle += math.pi / 6.0 * random.random() * 0.5
                self.play_sound(self.sound_paddle)
        # Check the ball is still in play
        if self.ball.x < self.bounds.x:
            self.score_b.score += 1
            self.reset_game()
            self.play_sound(self.sound_missed)
        if self.ball.x > self.bounds.right:
            self.score_a.score += 1
            self.reset_game()
            self.play_sound(self.sound_missed)
        
    def draw (self, display_surface):
        self.sprites.clear(display_surface, self.background)
        return self.sprites.draw(display_surface)
