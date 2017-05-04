import pygame, sys, random
from pygame.locals import *

# settings
FPS = 30
REVEAL_SPEED = 8

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BOX_SIZE = 40
GAP_SIZE = 10
BOX_COLUMN = 4
BOX_ROW = 4
assert (BOX_COLUMN * BOX_ROW) % 2 == 0, "Need to have an even number for pairs of matches."
XMARGIN = int((WINDOW_WIDTH - (BOX_SIZE + GAP_SIZE) * BOX_COLUMN) / 2)
YMARGIN = int((WINDOW_HEIGHT - (BOX_SIZE + GAP_SIZE) * BOX_ROW) / 2)

GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHT_BGCOLOR = GRAY
BOX_COLOR = WHITE
HIGHLIGHT_COLOR = BLUE

DONUT = "donut"
SQUARE = "square"
DIAMOND = "diamond"
LINES = "lines"
ELLIPSE = "ellipse"

ALL_COLORS = (GRAY, WHITE, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, ELLIPSE)
assert len(ALL_COLORS) * len(ALL_SHAPES) * 2 >= BOX_COLUMN * BOX_ROW, "Not enough of colors/shapes."

def main():
    # init
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Memory Puzzle")
    FPSCLOCK = pygame.time.Clock()

    first_selection = None

    main_board = get_randomized_board()
    boxes_state = set_boxes_state(False)
    start_game_animation(main_board, boxes_state)

    # game loop
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        draw_board(main_board, boxes_state)

        mousex = 0
        mousey = 0
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouse_clicked = True

        boxx, boxy = get_box_at_pixel(mousex, mousey)
        if boxx is not None and boxy is not None:
            if not boxes_state[boxx][boxy]:
                draw_highlight_box(boxx, boxy)

            if not boxes_state[boxx][boxy] and mouse_clicked:
                reveal_boxes_animation(main_board, [(boxx, boxy)])
                boxes_state[boxx][boxy] = True

                if first_selection is None:
                    first_selection = (boxx, boxy)
                else:
                    color1 = main_board[first_selection[0]][first_selection[1]][0]
                    shape1 = main_board[first_selection[0]][first_selection[1]][1]
                    color2 = main_board[boxx][boxy][0]
                    shape2 = main_board[boxx][boxy][1]

                    if color1 != color2 or shape1 != shape2:
                        # recover
                        pygame.time.wait(1000) # wait for 2000 miliseconds
                        cover_boxes_animation(main_board, [(first_selection[0], first_selection[1]), (boxx, boxy)])
                        boxes_state[first_selection[0]][first_selection[1]] = False
                        boxes_state[boxx][boxy] = False

                    elif has_won(boxes_state):
                        game_won_animation(main_board, boxes_state)
                        # reset game
                        main_board = get_randomized_board()
                        boxes_state = set_boxes_state(False)
                        draw_board(main_board, boxes_state)
                        pygame.display.update()
                        start_game_animation(main_board, boxes_state)

                    first_selection = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)

# create game board
def get_randomized_board():
    # create a list of randomly placed icons
    icons = list()
    for color in ALL_COLORS:
        for shape in ALL_SHAPES:
            icons.append((color, shape))
    random.shuffle(icons)
    icon_used_num = int(BOX_COLUMN * BOX_ROW / 2)
    icons = icons[:icon_used_num] * 2
    random.shuffle(icons)

    # create main board(a list of lists)
    main_board = list()
    for boxx in range(BOX_COLUMN):
        column = list()
        for boxy in range(BOX_ROW):
            column.append(icons[0])
            del icons[0]
        main_board.append(column)
    return main_board

# set boxes state: revealed or not
def set_boxes_state(state):
    boxes_state = list()
    for boxx in range(BOX_COLUMN):
        boxes_state.append([state] * BOX_ROW)
    return boxes_state

def start_game_animation(main_board, boxes_state):
    boxes = list()
    for boxx in range(BOX_COLUMN):
        for boxy in range(BOX_ROW):
            boxes.append((boxx, boxy))

    reveal_boxes_animation(main_board, boxes)
    pygame.time.wait(2000)
    cover_boxes_animation(main_board, boxes)

def draw_board(main_board, boxes_state):
    for boxx in range(BOX_COLUMN):
        for boxy in range(BOX_ROW):
            left = boxx * (BOX_SIZE + GAP_SIZE) + XMARGIN
            top = boxy * (BOX_SIZE + GAP_SIZE) + YMARGIN
            if not boxes_state[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, BOX_COLOR, (left, top, BOX_SIZE, BOX_SIZE))
            else:
                color = main_board[boxx][boxy][0]
                shape = main_board[boxx][boxy][1]
                draw_icon(color, shape, left, top)

def draw_icon(color, shape, left, top):
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOX_SIZE, BOX_SIZE))

    quarter = int(BOX_SIZE * 0.25)
    half = int(BOX_SIZE * 0.5)
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOX_SIZE - half, BOX_SIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOX_SIZE - 1, top + half), (left + half, top + BOX_SIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOX_SIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOX_SIZE - 1), (left + BOX_SIZE - 1, top + i))
    elif shape == ELLIPSE:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOX_SIZE, half))


def reveal_boxes_animation(main_board, boxes):
    for coverage in range(BOX_SIZE, (-REVEAL_SPEED) - 1, -REVEAL_SPEED):
        draw_boxes_cover(main_board, boxes, coverage)

def cover_boxes_animation(main_board, boxes):
    for coverage in range(0, BOX_SIZE + REVEAL_SPEED, REVEAL_SPEED):
        draw_boxes_cover(main_board, boxes, coverage)

def draw_boxes_cover(main_board, boxes, coverage):
    for box in boxes:
        color = main_board[box[0]][box[1]][0]
        shape = main_board[box[0]][box[1]][1]
        left = box[0] * (BOX_SIZE + GAP_SIZE) + XMARGIN
        top = box[1] * (BOX_SIZE + GAP_SIZE) + YMARGIN
        draw_icon(color, shape, left, top)
        if coverage > 0:
            pygame.draw.rect(DISPLAYSURF, BOX_COLOR, (left, top, coverage, BOX_SIZE))

    pygame.display.update()
    FPSCLOCK.tick(FPS)

# calculate box coordinates from pixel coordinates
def get_box_at_pixel(mousex, mousey):
    for boxx in range(BOX_COLUMN):
        left = boxx * (BOX_SIZE + GAP_SIZE) + XMARGIN
        for boxy in range(BOX_ROW):
            top = boxy *(BOX_SIZE + GAP_SIZE) + YMARGIN
            box = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if box.collidepoint(mousex, mousey):
                return (boxx, boxy)

    return (None, None)

def draw_highlight_box(boxx, boxy):
    left = boxx * (BOX_SIZE + GAP_SIZE) + XMARGIN
    top = boxy *(BOX_SIZE + GAP_SIZE) + YMARGIN
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHT_COLOR, (left - 5, top - 5, BOX_SIZE + 10, BOX_SIZE + 10), 2)

# judge whther the player has won
def has_won(boxes_state):
    for boxx in boxes_state:
        if False in boxx:
            return False

    return True

def game_won_animation(main_board, boxes_state):
    color1 = BGCOLOR
    color2 = LIGHT_BGCOLOR
    for i in range(10):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        draw_board(main_board, boxes_state)
        pygame.display.update()
        pygame.time.wait(200)

if __name__ == "__main__":
    main()
