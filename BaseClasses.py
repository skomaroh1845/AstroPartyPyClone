from BaseObject import BaseObject
from random import randint


class Bullet(BaseObject):
    def __init__(self):
        super(Bullet, self).__init__()




class Ship(BaseObject):
    def __init__(self):
        super(Ship, self).__init__()
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.alive = True



class User():

    def __init__(self, user_socket, user_address):
        self.name = ''
        self.ship = Ship()
        self.bullets = []
        self.socket = user_socket
        self.address = user_address
        self.score = 0
        self.index = 0








