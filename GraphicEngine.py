# Графический движок игры
# Также здесь находиться функция обрабоки нажатий
from random import randint
import pygame

# константы
# Задаем цвета
WHITE = (255, 255, 255)


# обработка нажатий
# формирует сообщение с данными о нажатиях
def events():
    mess = ''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'exit'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                mess = '+'
            if event.key == pygame.K_SPACE:
                mess = 'fire'
            if event.key == pygame.K_RETURN:
                mess = 'Enter'
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                mess = '-'
    return mess

# инициализация графического движка
def InitGraphic(WIDTH, HEIGHT):

    # window init
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('AstroPartyPyClone')
    clock = pygame.time.Clock()

    return screen, clock

# обновление кадра
def UpdateWindow(screen, bg_color, ship_sprites, bullet_sprites, map_sprites):

    # отрисовка фона
    screen.fill(bg_color)
    # добавить звездное небо
    # ...
    # обновление спрайтов
    ship_sprites.update()
    bullet_sprites.update()

    # отрисовка спрайтов
    map_sprites.draw(screen)
    bullet_sprites.draw(screen)
    ship_sprites.draw(screen)
    print_num_bullets(screen, ship_sprites)

    # переворот кадра
    pygame.display.flip()


def print_num_bullets(screen, ship_sprites):
    for ship in ship_sprites:
        font = pygame.font.Font(None, 30)
        text = font.render(f'{ship.num_bullets}', 1, WHITE)
        text_position = ship.position - ship.velocity*6 - pygame.math.Vector2(text.get_rect().center)
        screen.blit(text, text_position)

def print_starry_sky(screen):
    pass

def Quit():
    pygame.quit()


def RANDOME_COLOR():
    return (randint(0, 255), randint(0, 255), randint(0, 255))
