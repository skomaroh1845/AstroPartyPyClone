import pygame
import random
import os
import math


# константы
WIDTH = 700
HEIGHT = 540
FPS = 60
SPEED = 3
ROTATE_SPEED = 4

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
        self.direction = pygame.math.Vector2(x, y)
        self.position = position + direction * 10  # чтоб появился на носу коробля

        angle = self.direction.angle_to((1, 0))  # расчет текущего угла
        self.image = pygame.transform.rotate(self.image, angle)  # поворот изображения по направлению движения
        self.mask = pygame.mask.from_surface(self.image)  # снятие маски с нового спрайта
        self.rect = self.image.get_rect(center=self.position)


    def update(self):
        self.position += self.direction * self.speed
        self.rect.center = self.position


# спрайт
class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Player, self).__init__()
        ship_choice = random.randint(1, 4)  # выбор корабля
        self.image = pygame.image.load(os.path.join(img_folder, f'star_ship{ship_choice}.png')).convert_alpha()  # начальное изображение, не меняется
        self.mask = pygame.mask.from_surface(self.image)  # маска текущего изображения, обновляется при повороте
        self.position = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)  # координита центра спрайта
        self.rect = self.image.get_rect(center=self.position)
        self.direction = pygame.math.Vector2(SPEED, 0)
        self.rotate = False
        self.no_rotated_image = self.image



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
            self.direction.rotate_ip(ROTATE_SPEED)  # поворот против часовой стрелки

        self.position += self.direction  # движение коробля

        # ререндер спрайта
        angle = self.direction.angle_to((1, 0))  # расчет текущего угла
        self.image = pygame.transform.rotate(self.no_rotated_image, angle)  # поворот изображения по направлению движения
        self.mask = pygame.mask.from_surface(self.image)  # снятие маски с нового спрайта
        self.rect = self.image.get_rect(center=self.position)






if __name__ == '__main__':

    # Создаем игру и окно
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    # спрайты
    all_sprites = pygame.sprite.Group()  # группа спрайтов
    player = Player(screen)
    all_sprites.add(player)
    '''enemy = Player()
    enemy.direction = pygame.math.Vector2(0, 0)
    enemy.position = pygame.math.Vector2(WIDTH-100, HEIGHT-100)
    all_sprites.add(enemy)'''

    # пули
    bullets = pygame.sprite.Group()


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
                    new_bullet = Bullet(player.position, player.direction)
                    bullets.add(new_bullet)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    # деактивация поворота
                    player.rotate = False


        # Обновление
        all_sprites.update()
        bullets.update()

        # Рендеринг
        screen.fill(BG_COLOR)
        bullets.draw(screen)
        all_sprites.draw(screen)

        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()


    # завершение программы
    pygame.quit()