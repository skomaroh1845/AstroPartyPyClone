# Вспомогательные функции для работы клиента
from pygame.math import Vector2
import BaseClasses


def data_processing(data, ship_sprites, bullet_sprites):
    data_list = data.split('!!')
    #print(data_list)
    # обход списка
    i = 0  # первый элемент - служебное слово
    # данные кораблей
    if len(ship_sprites) > 0:
        for ship in ship_sprites:
            if data_list[i+1] != 'bull':
                ship_index, protected, position, velocity, alive, i = read_ship_data(data_list, i)
                ship.position = position
                ship.velocity = velocity
                if ship.ship_index != ship_index or ship.protected != protected:
                    ship.ship_index = ship_index
                    ship.protected = protected
                    ship.update_skin(ship_index, protected)
            else:
                i += 1  # для дальнейшего корректного чтения
                break
    else:
        while data_list[i] != 'bull':
            ship_index, protected, position, velocity, alive, i = read_ship_data(data_list, i)
            ship = BaseClasses.Ship(
                position,
                velocity,
                ship_index,
                0,
                protected
            )
            ship_sprites.add(ship)

    # данные пуль
    i += 1
    new_len = int(data_list[i])
    if new_len > 0:
        if len(bullet_sprites) == new_len:
            for bullet in bullet_sprites:
                if data_list[i+1] != 'end':
                    position, velocity, i = read_bullet_data(data_list, i)
                    bullet.position = position
                    bullet.velocity = velocity
                else:
                    break
        else:
            while data_list[i] != 'end':
                position, velocity, i = read_bullet_data(data_list, i)
                bullet = BaseClasses.Bullet(
                    position,
                    velocity,
                    0
                )
                bullet_sprites.add(bullet)


def read_ship_data(data_list, i):  # возвращает i = число итераций внутри функции + 1
    # тип коробля
    i += 1
    ship_index = int(data_list[i])
    i += 1
    protected = bool(data_list[i])

    # положение
    i += 1
    x = float(data_list[i])
    i += 1
    y = float(data_list[i])
    position = Vector2(x, y)

    # скорость
    i += 1
    x = float(data_list[i])
    i += 1
    y = float(data_list[i])
    velocity = Vector2(x, y)

    # жив или нет
    i += 1
    alive = bool(data_list[i])

    return ship_index, protected, position, velocity, alive, i+1


def read_bullet_data(data_list, i): # возвращает i = число итераций внутри функции + 1
    # положение
    i += 1
    x = float(data_list[i])
    i += 1
    y = float(data_list[i])
    position = Vector2(x, y)

    # скорость
    i += 1
    x = float(data_list[i])
    i += 1
    y = float(data_list[i])
    velocity = Vector2(x, y)

    return position, velocity, i+1


