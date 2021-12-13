# Вспомогательные функции для работы сервера
from pygame.sprite import collide_mask
'''from BaseClasses import Lichinus'''


# обновляет игровую информацию
def update_positions(users, ship_sprites, bullet_sprites, map_sprites):
    # обновление позиций
    ship_sprites.update()
    bullet_sprites.update()
    '''lichinus_sprites.update()'''

    # столкновения
    # пули c остальным
    for bullet in bullet_sprites:
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




def write_down_data():
    pass