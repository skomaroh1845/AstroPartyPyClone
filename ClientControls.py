# Вспомогательные функции для работы клиента
from pygame.math import Vector2
import BaseClasses


def data_processing(data, ship_sprites, bullet_sprites):
    data_list = data.split('!!')
    #print(data_list)

    # чтение данных списка
    i = 0  # первый элемент - служебное слово
    # данные кораблей
    i += 1
    ship_num = int(data_list[i])  # сколько кораблей
    if len(ship_sprites) > 0 and len(ship_sprites) == ship_num:
        for ship in ship_sprites:
            ship_index, protected, position, velocity, alive, i = read_ship_data(data_list, i)
            ship.position = position
            ship.velocity = velocity
            if ship.ship_index != ship_index or ship.protected != protected:
                ship.ship_index = ship_index
                ship.protected = protected
                ship.update_skin()
    else:
        ship_sprites.empty()
        for j in range(ship_num):
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
    bull_num = int(data_list[i])
    #print(bull_num)
    if bull_num > 0:
        if len(bullet_sprites) == bull_num:
            for bullet in bullet_sprites:
                position, velocity, i = read_bullet_data(data_list, i)
                bullet.position = position
                bullet.velocity = velocity
        else:
            bullet_sprites.empty()
            for j in range(bull_num):
                try:
                    position, velocity, i = read_bullet_data(data_list, i)
                except:
                    break
                bullet = BaseClasses.Bullet(
                    position,
                    velocity,
                    0
                )
                bullet_sprites.add(bullet)
    else:
        bullet_sprites.empty()


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

    return ship_index, protected, position, velocity, alive, i


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

    return position, velocity, i


