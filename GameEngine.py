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

    return screen, bg_color

def UpdateWindow(screen, bg_color):
    # main game cycle
    screen.fill(bg_color)
    pygame.display.flip()


if __name__ == '__main__':
    screen, bg_color = InitPygame()
    while True:
        UpdateWindow(screen, bg_color)
