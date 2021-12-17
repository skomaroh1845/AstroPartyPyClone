from Socket import BaseSocket
from threading import Thread
import GraphicEngine
import sys
import ClientControls
import pygame


class Client(BaseSocket):
    def __init__(self):
        super(Client, self).__init__()
        # графические настройки
        self.FPS = 60
        self.WIDTH = 1200
        self.HEIGHT = 1000
        self.BG_COLOR = (0, 50, 77)
        self.screen, self.clock = GraphicEngine.InitGraphic(self.WIDTH, self.HEIGHT)

        # создание локальной базы данных
        self.bullet_sprites = pygame.sprite.Group()
        self.map_sprites = pygame.sprite.Group()
        self.ship_sprites = pygame.sprite.Group()
        self.running = True


    # запуск клиента
    def set_up(self,):
        self.connect(
            ('127.0.0.1', 10101)
        )

        # выделение потока на прием данных и обработку данных
        recv_server = Thread(
            target=self.recv_data
        )
        recv_server.start()

        self.game_loop()  # запуск игры

    # закрытие клиента
    def quit(self):
        self.running = False
        self.close()

# игровой цикл (в рамках одного раунда)
    def game_loop(self):

        running = True
        while running:
            self.clock.tick(self.FPS)  # FPS

            GraphicEngine.UpdateWindow(
                self.screen, self.BG_COLOR,
                self.ship_sprites,
                self.bullet_sprites,
                self.map_sprites
            )

            # обработка нажатий
            mess = GraphicEngine.events()
            # отправка на сервер
            if mess != '':
                self.send_data(mess)
            # завершение игры
            if mess == 'exit':
                GraphicEngine.Quit()
                self.close()
                self.running = False
                #sys.exit()
                running = False

    # отправка данных на сервер
    def send_data(self, data):
        self.send(data.encode('utf8'))

    # получение данных с сервера
    def recv_data(self, recv_socket=None):
        while self.running:
            # получение данных
            try:
                data = self.recv(1024)
            except:
                break
            data = data.decode('utf8')
            # обработка данных с сервера
            if data.startswith('GAME_DATA'):
                ClientControls.data_processing(
                    data,
                    self.ship_sprites,
                    self.bullet_sprites
                )
            else:
                print(data)


if __name__ == '__main__':
    client = Client()
    client.set_up()


