# Вспомогательные функции для работы сервера
from pygame.sprite import collide_mask
from pygame.math import Vector2
from BaseClasses import Bullet
from BaseClasses import Ship
from time import time
from random import randint
'''from BaseClasses import Lichinus'''


# обновляет игровую информацию
def update_positions(users, ship_sprites, bullet_sprites, map_sprites):
    # обновление позиций
    ship_sprites.update()
    bullet_sprites.update()
    '''lichinus_sprites.update()'''

    # перезарядка орудий и респаун
    for user in users:
        if user.ship.num_bullets < 3 and user.reload_start is None:
            user.reload_start = time()
        if user.reload_start is not None:
            if time() - user.reload_start > user.bull_timer:
                user.ship.num_bullets += 1
                user.reload_start = None
        if not user.alive:
            if time() - user.respawn_timer > user.bull_timer:
                user.alive = True
                player_init(user, user.index, ship_sprites, user.color)


    # столкновения
    # пули c остальным
    for bullet in bullet_sprites:
        # удалим улетевшие за карту пули
        if (bullet.position.x > 900 + 40) or (
                bullet.position.x < 0 - 40) or (
                bullet.position.y > 720 + 40) or (
                bullet.position.y < 0 - 40):
            bullet_sprites.remove(bullet)
            continue

        # проверим столкновения с пулями на карте
        hit = False
        for ship in ship_sprites:
            if collide_mask(bullet, ship):
                # удаление попавшей пули
                bullet_sprites.remove(bullet)
                hit = True

                if ship.protected:
                    ship.protected = False
                else:
                    if bullet.owner == ship.owner:
                        users[bullet.owner].score -= 1
                        users[bullet.owner].alive = False
                        if users[bullet.owner].score < 0:
                            users[bullet.owner].score = 0
                    else:
                        users[bullet.owner].score += 1
                        users[ship.owner].alive = False
                        users[ship.owner].respawn_timer = time()

                    # удаление подбитого корабля
                    ship_sprites.remove(ship)


                    '''# появление пилота
                    users[ship.owner].lichinus = True
                    lichinus_sprites.add(Lichinus())'''
                break
        if hit:
            continue

        '''for lichinus in lichinus_sprites:
            if collide_mask(bullet, lichinus):
                # очки за попадание
                if bullet.owner == lichinus.owner:
                    users[bullet.owner].score -= 1
                    if users[bullet.owner].score < 0:
                        users[bullet.owner].score = 0
                else:
                    users[bullet.owner].score += 1

                # удаление попавшей пули
                bullet_sprites.remove(bullet)
                # удаление убитого личинуса
                lichinus_sprites.remove(lichinus)
                users[lichinus.owner].alive = False
                break
        if hit:
            continue'''

        for map_obj in map_sprites:
            if collide_mask(bullet, map_obj):
                # удаление попавшей пули
                bullet_sprites.remove(bullet)
                break



# обработка нажатий
def write_down_data(user, data, bullet_sprites):
    if data == '+':
        user.ship.rotate = True
    if data == '-':
        user.ship.rotate = False
    if data == 'fire':
        if user.ship.num_bullets > 0:
            bullet_sprites.add(Bullet(user.ship.position, user.ship.velocity, user.ship.owner))
            user.ship.num_bullets -= 1



def player_init(user, index, ship_sprites, color=None):
    pos = Vector2(randint(100, 800), randint(100, 620))
    map_center = Vector2(450, 360)
    dir = 5 * (map_center - pos) / (map_center - pos).length()  # смотрит всегда в центр
    if color is None:
        color = randint(1, 4)
    user.ship = Ship(
        pos,
        dir,
        color,
        index
    )
    user.color = color
    ship_sprites.add(user.ship)
