import pygame, random, sys
from pygame.locals import *

FPS = 30

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
assert WINDOW_WIDTH % CELL_SIZE == 0, 'Window width must be a multiple of cell size.'
assert WINDOW_HEIGHT % CELL_SIZE == 0, 'Window height must be a multiple of cell size.'
CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Wormy')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)

    while True:
        run_game()

def run_game():
    # draw the game board
    worm_coords = [get_random_location()]
    direction = None

    apple_coords = get_random_location()

    draw_board(worm_coords, apple_coords)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            else:
                direction = None

            # move the worm by adding a new head in the direction it is moving
            if direction is not None:
                if direction == UP:
                    new_head = [worm_coords[0][0], worm_coords[0][1] - 1]
                elif direction == DOWN:
                    new_head = [worm_coords[0][0], worm_coords[0][1] + 1]
                elif direction == LEFT:
                    new_head = [worm_coords[0][0] - 1, worm_coords[0][1]]
                elif direction == RIGHT:
                    new_head = [worm_coords[0][0] + 1, worm_coords[0][1]]
                worm_coords.insert(0, new_head)

                # check if the game is over
                if worm_coords[0][0] == -1 or worm_coords[0][0] == CELL_WIDTH or worm_coords[0][1] == -1 or worm_coords[0][1] == CELL_HEIGHT:
                    draw_game_over()
                    return

                for worm_body in worm_coords[1:]:
                    if worm_body[0] == worm_coords[0][0] and worm_body[1] == worm_coords[0][1]:
                        draw_game_over()
                        return

                # check if the worm ate the apple
                if worm_coords[0][0] == apple_coords[0] and worm_coords[0][1] == apple_coords[1]:
                    apple_coords = get_random_location() # set a new apple once the old one has been eaten
                else:
                    del worm_coords[-1] # fail to eat the apple

            draw_board(worm_coords, apple_coords)
            FPSCLOCK.tick(FPS)

def get_random_location():
    return [random.randint(0, CELL_WIDTH - 1), random.randint(0, CELL_HEIGHT - 1)]

def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOW_WIDTH, y))

def draw_worm(worm_coords):
    for coord in worm_coords:
        x = coord[0] * CELL_SIZE
        y = coord[1] * CELL_SIZE
        pygame.draw.rect(DISPLAYSURF, GREEN, (x, y, CELL_SIZE, CELL_SIZE))

def draw_apple(apple_coords):
    x = apple_coords[0] * CELL_SIZE
    y = apple_coords[1] * CELL_SIZE
    pygame.draw.rect(DISPLAYSURF, RED, (x, y, CELL_SIZE, CELL_SIZE))

def draw_score(score):
    score_surf = BASICFONT.render('Score:{}'.format(score), True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOW_WIDTH - 100, 10)
    DISPLAYSURF.blit(score_surf, score_rect)

def draw_board(worm_coords, apple_coords):
    DISPLAYSURF.fill(BGCOLOR)
    draw_grid()
    draw_worm(worm_coords)
    draw_apple(apple_coords)
    draw_score(len(worm_coords) - 1)
    pygame.display.update()

def draw_game_over():
    gameover_surf = pygame.font.Font('freesansbold.ttf', 100).render('GAME OVER', True, WHITE)
    gameover_rect = gameover_surf.get_rect()
    gameover_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100)
    DISPLAYSURF.blit(gameover_surf, gameover_rect)
    pygame.display.update()
    pygame.time.wait(2000)

if __name__ == '__main__':
    main()
