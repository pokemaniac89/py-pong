import pygame, math, random, entity

def load_image(path):
    surface = pygame.image.load(path)
    surface.convert()
    pygame.surfarray.pixels3d(surface)[:,:,0:1:] = 0
    return surface

class Game(object):
    
    def __init__(self, player_left, player_right, configuration):
        self.player_left = player_left
        self.player_right = player_right
        self.configuration = configuration
        self.background = pygame.Surface(configuration['screen_size'])
        self.sprites = pygame.sprite.OrderedUpdates()
        line = entity.Line(load_image(configuration['line_image']), self.sprites)
        line.rect.topleft = ((configuration['screen_size'][0]-line.rect.width)/2, 0)
        paddle_image = load_image(configuration['paddle_image'])
        bounds_y = configuration['screen_size'][1] - paddle_image.get_height()
        self.paddle_left = entity.Paddle(configuration['paddle_velocity'], paddle_image, bounds_y, self.sprites)
        self.paddle_right = entity.Paddle(configuration['paddle_velocity'], paddle_image, bounds_y, self.sprites)
        self.paddle_left.rect.topleft = (self.configuration['paddle_left_position'], (self.configuration['screen_size'][1]-self.paddle_left.rect.height)/2)
        self.paddle_right.rect.topleft = (self.configuration['paddle_right_position'], (self.configuration['screen_size'][1]-self.paddle_left.rect.height)/2)
        digit_images = [load_image(configuration['digit_image'] % n) for n in xrange(10)]
        self.score_left = entity.Score(digit_images, self.sprites)
        self.score_left.rect.topleft = configuration['score_left_position']
        self.score_right = entity.Score(digit_images, self.sprites)
        self.score_right.rect.topleft = configuration['score_right_position']
        ball_image = load_image(configuration['ball_image'])
        self.ball = entity.Ball(ball_image, self.sprites)
        self.bounds = pygame.Rect(20, 0, configuration['screen_size'][0]-ball_image.get_width()-20, configuration['screen_size'][1]-ball_image.get_height())
        self.sound_missed = pygame.mixer.Sound(configuration['sound_missed'])
        self.sound_paddle = pygame.mixer.Sound(configuration['sound_paddle'])
        self.sound_wall = pygame.mixer.Sound(configuration['sound_wall'])
        self.reset_game(True)
        self.running = True
        
    def play_sound(self, sound):
        sound.play()
        
    def reset_game(self, serveLeft=True):
        self.ball.rect.topleft = ((self.configuration['screen_size'][0]-self.ball.rect.width)/2, (self.configuration['screen_size'][1]-self.ball.rect.height)/2)
        a = random.random() * math.pi / 2. - math.pi / 4.
        self.ball.velocity[0] = self.configuration['ball_velocity'] * math.cos(a)
        self.ball.velocity[1] = self.configuration['ball_velocity'] * math.sin(a)
        if random.random() < 0.5:
            self.ball.velocity[1] = -self.ball.velocity[1]
        if serveLeft:
            self.ball.velocity[0] *= -1
        
    def update(self):
        
        # Update sprites and players
        self.sprites.update()
        self.player_left.update(self.paddle_left, self)
        self.player_right.update(self.paddle_right, self)
        
        # Paddle collision check
        if self.ball.rect.x < self.bounds.centerx:
            # Left paddle
            if self.paddle_left.rect.colliderect(self.ball.rect) and self.ball.rect.right > self.paddle_left.rect.right:
                self.ball.rect.x = self.paddle_left.rect.right
                velocity = self.paddle_left.calculate_bounce((self.ball.rect.y - self.paddle_left.rect.y) / float(self.paddle_left.rect.height))
                self.ball.velocity[0] = -self.ball.velocity[0]
                self.play_sound(self.sound_paddle)
        else:
            # Right paddle
            if self.paddle_right.rect.colliderect(self.ball.rect) and self.ball.rect.x < self.paddle_right.rect.x:
                self.ball.rect.x = self.paddle_right.rect.x - self.ball.rect.width
                velocity = self.paddle_right.calculate_bounce((self.ball.rect.y - self.paddle_right.rect.y) / float(self.paddle_right.rect.height))
                self.ball.velocity[0] = -self.ball.velocity[0]
                self.play_sound(self.sound_paddle)
        
        # Bounds collision check
        if self.ball.rect.y < self.bounds.top:
            self.ball.rect.y = self.bounds.top
            self.ball.velocity[1] = -self.ball.velocity[1]
            self.play_sound(self.sound_wall)
        elif self.ball.rect.y > self.bounds.bottom:
            self.ball.rect.y = self.bounds.bottom
            self.ball.velocity[1] = -self.ball.velocity[1]
            self.play_sound(self.sound_wall)

        # Check the ball is still in play
        if self.ball.rect.x < self.bounds.x:
            self.score_right.score += 1
            self.reset_game(False)
            self.play_sound(self.sound_missed)
        if self.ball.rect.x > self.bounds.right:
            self.score_left.score += 1
            self.reset_game(True)
            self.play_sound(self.sound_missed)

        
    def draw(self, display_surface):
        self.sprites.clear(display_surface, self.background)
        return self.sprites.draw(display_surface)
