# основные классы проекта
from BaseObject import BaseSpriteObject
import pygame
import os

ROTATE_SPEED = 5

class Bullet(BaseSpriteObject):
    def __init__(self, position, direction, ship_owner):  # предполагается, что pos указывает на нос корабля
        bullet_pos = position + direction * 2
        self.bull_speed = 2  # во сколько раз пуля быстрее корабля
        super(Bullet, self).__init__(bullet_pos.x, bullet_pos.y,
                                     direction.x, direction.y, 'bullet.png')
        self.owner = ship_owner  # для идентификации пули

    def update(self):
        super(Bullet, self).update()
        self.position += self.velocity * (self.bull_speed - 1)
        self.rect.center = self.position



class Ship(BaseSpriteObject):
    def __init__(self, position, direction, ship_color, user_index, protected=True):
        if ship_color == 'red' or ship_color == 1:
            ship_choice = 1
        elif ship_color == 'purple' or ship_color == 2:
            ship_choice = 2
        elif ship_color == 'green' or ship_color == 3:
            ship_choice = 3
        else:
            ship_choice = 4
        if protected:
            protected = '_prot'
        else:
            protected = ''
        super(Ship, self).__init__(
            position.x, position.y,
            direction.x, direction.y,
            f'star_ship{ship_choice}{protected}.png'
        )
        self.num_bullets = 3  # число пуль выпущенных за раз
        self.protected = True
        self.ship_index = ship_choice
        self.owner = user_index  # для идентификации корабля
        # ставим pos на нос корабля для смещения центра вращения
        self.rect.center = self.position-self.velocity*6


    def update(self):
        # движение
        if self.rotate:
            self.acceleration.rotate_ip(ROTATE_SPEED)  # поворот против (+) или по (-) часовой стрелке
        super(Ship, self).update()
        # ставим pos на нос корабля для смещения центра вращения
        self.rect.center = self.position - self.velocity * 6

        # закольцовка координат
        if self.position.x > 1200 + 40:
            self.position.x = 0 - 40
        if self.position.x < 0 - 40:
            self.position.x = 1200 + 40
        if self.position.y > 1000 + 40:
            self.position.y = 0 - 40
        if self.position.y < 0 - 40:
            self.position.y = 1000 + 40

    def update_skin(self, ship_choice=None, protected=None):
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'img')
        if protected is not None:
            if protected:
                protected = '_prot'
            else:
                protected = ''
            image_name = f'star_ship{ship_choice}{protected}.png'
        else:
            if self.protected:
                protected = '_prot'
            else:
                protected = ''
            image_name = f'star_ship{self.ship_index}{protected}.png'

        self.image = pygame.image.load(os.path.join(img_folder, image_name)).convert_alpha()
        self.no_rotated_image = self.image
        self.image = pygame.transform.rotate(self.no_rotated_image, self.get_angle())




'''class Lichinus(BaseSpriteObject):
    def __init__(self, position, direction, img_folder):

        super(Lichinus, self).__init__(position.x, position.y,
                                       direction.x, direction.y,
                                       image=(img_folder, f'star_ship{ship_choice}_def.png')) '''



class User():

    def __init__(self, user_socket=None, user_address=None):
        self.name = ''
        self.ship = None
        self.socket = user_socket
        self.address = user_address
        self.score = 0
        self.alive = True
        #self.lichinus = False
        self.index = None


class Wall():
    def __init__(self):
        pass


class GameMap():
    def __init__(self):
        pass






