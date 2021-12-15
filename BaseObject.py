from abc import abstractmethod
import pygame
import os

SPEED = 5
ACCEL = 1

class BaseSpriteObject(pygame.sprite.Sprite):
    @abstractmethod
    def __init__(self, x=0, y=0, v_x=SPEED, v_y=0, image_name=''):  # image='name.png'
        super(BaseSpriteObject, self).__init__()
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(v_x, v_y)
        self.acceleration = ACCEL * self.velocity / self.velocity.length()  # ед. вектор сонаправ. скорости
        self.rotate = False
        if image_name != '':
            game_folder = os.path.dirname(__file__)
            img_folder = os.path.join(game_folder, 'img')
            self.image = pygame.image.load(os.path.join(img_folder, image_name)).convert_alpha()
            self.no_rotated_image = self.image
            angle = self.velocity.angle_to((1, 0))  # расчет текущего угла
            self.image = pygame.transform.rotate(self.no_rotated_image, angle)  # поворот изображения по направлению движения
            self.mask = pygame.mask.from_surface(self.image)  # снятие маски с нового спрайта
            self.rect = self.image.get_rect(center=self.position)  # для расчетов

    def get_angle(self):
        return self.velocity.angle_to((1, 0))  # расчет текущего угла

    @abstractmethod
    def update(self):
        old_angle = self.get_angle()

        self.velocity += self.acceleration

        if self.velocity.length() > SPEED:  # не даем скорости уходить на бесконечность
            self.velocity -= self.velocity / self.velocity.length() * self.acceleration.length()

        self.position += self.velocity

        if self.get_angle() != old_angle:  # если угол изменился - поворачиваем спрайт
            self.update_sprite_angle(self.get_angle())


    def update_sprite_angle(self, angle):
        self.image = pygame.transform.rotate(self.no_rotated_image,
                                             angle)  # поворот изображения по направлению движения
        self.mask = pygame.mask.from_surface(self.image)  # снятие маски с нового спрайта
        self.rect = self.image.get_rect(center=(self.position))