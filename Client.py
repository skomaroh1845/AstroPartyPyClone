from Socket import BaseSocket
from threading import Thread
import GameEngine
import BaseClasses
import sys


class Client(BaseSocket):
    def __init__(self):
        super(Client, self).__init__()
        self.FPS = 1

        # создание локальной базы данных из 4 игроков с 5 пулями
        self.users = [BaseClasses.User() for i in range(4)]
        for user in self.users:
            user.bullets = [BaseClasses.Bullet for i in range(10)]

        self.game_map = ''




    # запуск клиента
    def set_up(self,):
        self.connect(
            ('127.0.0.1', 10101)
        )

        # выделение потока на прием данных
        recv_server = Thread(
            target=self.recv_data
        )
        recv_server.start()

        self.game_loop(True)  # запуск игры



    def game_loop(self, running):
        Screen, BG_color, clock = GameEngine.InitPygame()
        while running:
            clock.tick(self.FPS)  # FPS

            # main game loop
            GameEngine.UpdateWindow(Screen, BG_color, self.users)

            # обработка клавишь и отправка на сервер
            mess = GameEngine.events()
            self.send_data(mess)
            if mess == 'exit':
                GameEngine.Quit()
                self.close()
                sys.exit()
                break


    def send_data(self, data):
        self.send(data.encode('utf8'))


    def recv_data(self, recv_socket=None):
        while True:
            try:
                # получение данных
                data = self.recv(1024)
                data = data.decode('utf8')
                # запись данных
                if data.startswith('GAME_DATA'):
                    self.data_proccessing(data)
                else:
                    print(data)

            except:
                break


    def data_proccessing(self, data):
        data_list = data.split('!!')
        # обход списка
        i = 1  # первый элемент - служебное слово
        block = data_list[i]
        for user in self.users:
            if block == 'end':
                break
            if block == 'next':
                i += 1
                block = data_list[i]

            user.ship.x = block
            i += 1
            block = data_list[i]
            user.ship.y = block
            i += 1
            block = data_list[i]
            user.ship.v = block
            i += 1
            block = data_list[i]
            user.ship.angle = block
            i += 1
            block = data_list[i]
            user.ship.color = block
            i += 1
            block = data_list[i]
            for bullet in user.bullets:
                if block == 'end':
                    break
                if block == 'next':
                    break
                bullet.x = block
                i += 1
                block = data_list[i]
                bullet.y = block
                i += 1
                block = data_list[i]
                bullet.v = block
                i += 1
                block = data_list[i]
                bullet.angle = block
                i += 1
                block = data_list[i]

if __name__ == '__main__':
    client = Client()
    client.set_up()

