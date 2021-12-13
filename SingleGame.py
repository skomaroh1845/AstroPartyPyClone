import pygame
import random
import os
import math
import time
import threading
import sys


# константы
WIDTH = 700
HEIGHT = 540
FPS = 60
SPEED = 5
ROTATE_SPEED = 5
ACCEL = 1

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG_COLOR = (0, 68, 102)
def RANDOME_COLOR():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# настройка папки ассетов
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')


# пуля
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        super(Bullet, self).__init__()
        self.image = pygame.image.load(os.path.join(img_folder, 'bullet.png')).convert_alpha()
        self.speed = 2
        x = float(direction.x)
        y = float(direction.y)
        self.velocity = pygame.math.Vector2(x, y)
        self.position = position + direction * 15  # чтоб появился на носу коробля


        angle = self.velocity.angle_to((1, 0))  # расчет текущего угла
        self.image = pygame.transform.rotate(self.image, angle)  # поворот изображения по направлению движения
        self.mask = pygame.mask.from_surface(self.image)  # снятие маски с нового спрайта
        self.rect = self.image.get_rect(center=self.position)


    def update(self):
        self.position += self.velocity * self.speed
        self.rect.center = self.position





# спрайт
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        ship_choice = random.randint(1, 4)  # выбор корабля
        self.image = pygame.image.load(os.path.join(img_folder, f'star_ship{ship_choice}.png')).convert_alpha()  # начальное изображение, не меняется
        self.mask = pygame.mask.from_surface(self.image)  # маска текущего изображения, обновляется при повороте
        self.position = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)  # координита центра спрайта
        self.rect = self.image.get_rect(center=self.position)
        self.velocity = pygame.math.Vector2(SPEED, 0)
        self.acceleration = pygame.math.Vector2(ACCEL, 0)
        self.rotate = False
        self.no_rotated_image = self.image
        self.score = 0
        self.visible = True
        self.collide_with_ship = None
        self.num_bullets = 3



    def update(self):
        # закольцовка координат
        if self.position.x > WIDTH + 40:
            self.position.x = 0 - 40
        if self.position.x < 0 - 40:
            self.position.x = WIDTH + 40
        if self.position.y > HEIGHT + 40:
            self.position.y = 0 - 40
        if self.position.y < 0 - 40:
            self.position.y = HEIGHT + 40

        # движение
        if self.rotate:
            self.acceleration.rotate_ip(ROTATE_SPEED)  # поворот против часовой стрелки

        self.velocity += self.acceleration

        if self.velocity.length() > SPEED:
            self.velocity -= self.velocity / self.velocity.length() * self.acceleration.length()

        self.position += self.velocity  # движение коробля



        # ререндер спрайта
        angle = self.velocity.angle_to((1, 0))  # расчет текущего угла
        self.image = pygame.transform.rotate(self.no_rotated_image, angle)  # поворот изображения по направлению движения
        self.mask = pygame.mask.from_surface(self.image)  # снятие маски с нового спрайта
        self.rect = self.image.get_rect(center=(self.position-self.velocity*6))



def add_enemy(all_sprites, enemy):
    time.sleep(5)
    all_sprites.add(enemy)

def print_num_bullets(screen, all_sprites):
    for sprite in all_sprites.copy():
        font = pygame.font.Font(None, 30)
        text = font.render(f'{sprite.num_bullets}', 1, WHITE)
        text_position = sprite.position-sprite.velocity*5 - pygame.math.Vector2(text.get_rect().center)
        screen.blit(text, text_position)

def game_cycle(screen, clock, player, bullets, all_sprites):
    # Цикл игры
    running = True
    while running:
        # Держим цикл на правильной скорости
        clock.tick(FPS)

        # Ввод процесса (события)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            # управление
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    # активация поворота
                    player.rotate = True
                if event.key == pygame.K_SPACE:
                    # выстрел
                    if len(bullets) < 3:
                        new_bullet = Bullet(player.position, player.velocity)
                        bullets.add(new_bullet)
                        player.num_bullets -= 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    # деактивация поворота
                    player.rotate = False

        # Обновление
        all_sprites.update()
        bullets.update()

        # Удаление улетевших пуль
        for bullet in bullets.copy():
            if (bullet.position.x > WIDTH + 400) or (
                    bullet.position.x < 0 - 400) or (
                    bullet.position.y > HEIGHT + 400) or (
                    bullet.position.y < 0 - 400):
                bullets.remove(bullet)
                player.num_bullets += 1

        # столкновения
        to_break = False  # для завершения раунда
        for sprite in all_sprites.copy():
            # с пулями
            for bullet in bullets.copy():
                if pygame.sprite.collide_mask(sprite, bullet):
                    # очки за попадание
                    if sprite == player:
                        player.score -= 1
                    else:
                        player.score += 1
                    print(player.score)
                    bullets.remove(bullet)
                    player.num_bullets += 1
                    all_sprites.remove(sprite)
                    to_break = True
            # с кораблями
            for another_sprite in all_sprites.copy():
                if another_sprite != sprite:
                    if pygame.sprite.collide_mask(sprite, another_sprite):
                        joint_direction = sprite.velocity + another_sprite.velocity
                        angle = another_sprite.velocity.angle_to(joint_direction)
                        # реализация отталкивания




        # Рендеринг
        screen.fill(BG_COLOR)
        bullets.draw(screen)
        all_sprites.draw(screen)
        print_num_bullets(screen, all_sprites)

        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
        if to_break:
            break
    return running



if __name__ == '__main__':

    # Создаем игру и окно
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    # спрайты
    all_sprites = pygame.sprite.Group()  # группа спрайтов
    player = Player()
    all_sprites.add(player)
    enemy = Player()
    enemy.velocity = pygame.math.Vector2(SPEED, 0)
    enemy.position = pygame.math.Vector2(WIDTH-100, HEIGHT-100)


    # пули
    bullets = pygame.sprite.Group()


    # цикл раундов
    for i in range(5):
        print(f'Round {i}')
        add_enemy_thread = threading.Thread(
            target=add_enemy,
            args=(all_sprites, enemy)
        )
        add_enemy_thread.start()

        if not game_cycle(screen, clock, player, bullets, all_sprites):
            break

    # завершение программы
    pygame.quit()