import pygame, pypong
from pypong.player import BasicAIPlayer, KeyboardPlayer, MousePlayer

def run ():
    configuration = {
        'screen_size': (686,488),
        'paddle_image': 'assets/paddle.png',
        'paddle_a_position': 84,
        'paddle_b_position': 594,
        'paddle_velocity': 4,
        'line_image': 'assets/dividing-line.png',
        'ball_image': 'assets/ball.png',
        'score_a_position': (141, 30),
        'score_b_position': (473, 30),
        'digit_image': 'assets/digit_%i.png',
    }
    pygame.init()
    display_surface = pygame.display.set_mode(configuration['screen_size'])
    output_surface = display_surface.copy().convert_alpha()
    output_surface.fill((0,0,0))
    clock = pygame.time.Clock()
    
    # Prepare our game
    input_state = {'key': None, 'mouse': None}
    player_a = BasicAIPlayer()
    player_b = BasicAIPlayer()
    game = pypong.Game(player_a, player_b, configuration)
    
    # Main game loop
    timestamp = 1
    while game.running:
        clock.tick(60)
        now = pygame.time.get_ticks()
        if timestamp > 0 and timestamp < now:
            timestamp = now + 5000
            print clock.get_fps()
        input_state['key'] = pygame.key.get_pressed()
        input_state['mouse'] = pygame.mouse.get_pos()
        game.update()
        game.draw(output_surface)
        pygame.surfarray.pixels_alpha(output_surface)[:,::2] = 32
        display_surface.blit(output_surface, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game.running = False
        
if __name__ == '__main__': run()