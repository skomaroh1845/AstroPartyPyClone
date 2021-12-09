import pygame

def events():
    mess = ' '
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'exit'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                mess = '+'
            if event.key == pygame.K_b:
                mess = 'fire'
            if event.key == pygame.K_RETURN:
                mess = 'Enter'
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_n:
                mess = '-'
    return mess

def InitPygame():

    # window init
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption('AstroPartyPyClone')
    bg_color = (0, 0, 0)
    clock = pygame.time.Clock()

    return screen, bg_color, clock

def UpdateWindow(screen, bg_color, users=None):
    # main game cycle
    screen.fill(bg_color)
    # отрисовка всего и вся


    pygame.display.flip()


def Quit():
    pygame.quit()


if __name__ == '__main__':
    screen, bg_color = InitPygame()
    while True:
        UpdateWindow(screen, bg_color)
