# Графический движок игры
# Также здесь находиться функция обрабоки нажатий
import pygame
import os
from pygame.math import Vector2

# константы
# Задаем цвета
WHITE = (255, 255, 255)


# обработка нажатий
# формирует сообщение с данными о нажатиях
def game_events():
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
def UpdateWindow(screen, bg_color, ship_sprites=None, bullet_sprites=None, map_sprites=None):

    # отрисовка фона
    screen.fill(bg_color)
    # добавить звездное небо
    # ...


    # отрисовка игровых спрайтов
    if ship_sprites is not None:
        # обновление спрайтов
        for ship in ship_sprites:
            ship.update_sprite_graphics()
        for bullet in bullet_sprites:
            bullet.update_sprite_graphics()

        # отрисовка спрайтов
        map_sprites.draw(screen)
        bullet_sprites.draw(screen)
        ship_sprites.draw(screen)
        print_num_bullets(screen, ship_sprites)
        print_score(screen, ship_sprites)

    # переворот кадра
    pygame.display.flip()


def print_num_bullets(screen, ship_sprites):
    for ship in ship_sprites:
        font = pygame.font.Font(None, 30)
        text = font.render(f'{ship.num_bullets}', 1, WHITE)
        text_position = ship.position - ship.velocity*6 - Vector2(text.get_rect().center)
        screen.blit(text, text_position)


def print_score(screen, ship_sprites):
    i = 0
    for ship in ship_sprites:
        font = pygame.font.Font(None, 35)
        text = font.render(f'{ship.color}: {ship.score}', 1, WHITE)
        text_position = Vector2(10, 10+40*i)
        screen.blit(text, text_position)
        i += 1


def print_starry_sky(screen):
    pass


def start_screen(screen):
    headline = 'Welcome to the AstroPartyPyClone!'
    button_text = ["Sit in the captain's chair",
                   "(press Enter)"]
    help_text = ['You took the wheel in your hands for the first time, you are careful and',
                 'do not touch unfamiliar buttons, but what a pity that you only know how to',
                 'turn in one direction (key "D") and how to shoot (key SPACE)...']
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    background = pygame.image.load(os.path.join(img_folder, 'OuterSpaceShip1.jpg'))
    screen.blit(background, (0, 0))
    # рисуем заголовок
    font = pygame.font.Font(None, 60)
    text = font.render(headline, 1, WHITE)
    text_pos = Vector2(screen.get_rect().center) - Vector2(text.get_rect().center)
    text_pos += Vector2(0, -280)
    screen.blit(text, text_pos)

    # рисуем текст-кнопку
    font = pygame.font.Font(None, 40)
    for i in range(2):
        text = font.render(button_text[i], 1, WHITE)
        text_pos = Vector2(screen.get_rect().center) - Vector2(text.get_rect().center)
        text_pos += Vector2(0, 140 + 50*i)
        screen.blit(text, text_pos)

    # рисуем подсказку
    font = pygame.font.Font(None, 30)
    for i in range(3):
        text = font.render(help_text[i], 1, WHITE)
        text_pos = Vector2(screen.get_rect().center) - Vector2(text.get_rect().center)
        text_pos += Vector2(0, 240 + 40*i)
        screen.blit(text, text_pos)

    pygame.display.flip()

def Quit():
    pygame.quit()

