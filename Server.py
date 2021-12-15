from Socket import BaseSocket
from threading import Thread
import BaseClasses
import pygame
import ServerControls


class Server(BaseSocket):
    def __init__(self):
        super(Server, self).__init__()
        self.users = []
        self.bullet_sprites = pygame.sprite.Group()
        self.map_sprites = pygame.sprite.Group()
        self.ship_sprites = pygame.sprite.Group()
        '''self.lichinus_sprites = pygame.sprite.Group()'''
        self.FPS = 60
        self.game_started = False

    # запуск сервера
    def set_up(self):
        self.bind(
            ('127.0.0.1', 10101)
        )
        self.listen()

        # запускает игровой движок
        self.game_engine_starter()

        # цикл, принимающий пользователей
        self.accept_sockets()

    # отправка данных, если сообщение не указано, оправляются служебные данные
    def send_data(self, data=None):
        if data is None:
            data = self.generate_mess()
        # отправка данных пользователям
        for user in self.users:
            try:
                user.socket.send(data.encode('utf8'))
            except:
                self.delete_user(user)

    # генератор служебных сообщений
    def generate_mess(self):
        mess = 'GAME_DATA!!'
        # информация о кораблях
        for user in self.users:
            mess += f'{user.ship.ship_index}!!'  # тип корабля
            mess += f'{user.ship.protected}!!'

            mess += f'{user.ship.position.x}!!'  # координаты корабля
            mess += f'{user.ship.position.y}!!'

            mess += f'{user.ship.velocity.x}!!'  # его направление
            mess += f'{user.ship.velocity.y}!!'

            mess += f'{user.alive}!!'            # жив или нет
        mess += 'bull!!'
        # информация о пулях
        mess +=f'{len(self.bullet_sprites)}!!'  # сообщает сколько пуль, т к их количество постоянно меняется
        for bullet in self.bullet_sprites:
            mess += f'{bullet.position.x}!!'
            mess += f'{bullet.position.y}!!'
            mess += f'{bullet.velocity.x}!!'
            mess += f'{bullet.velocity.y}!!'
        mess += 'end'
        #print(mess)
        return mess


    # принимает данные от пользователей в реальном времени
    def recv_data(self, recv_socket=None):
        try:
            data = recv_socket.recv(1024)
        except:
            return 'exit'
        return data.decode('utf8')


    # занимается обработкой пользователя (игровой процесс)
    def user_host(self, index):
        user = self.users[index]
        # инициализация клиента пользователя
        # загрузка карты
        # ...
        self.send_data('Welcome to the best game ever!')
        # работа интерфейса
        # ...
        self.send_data('press enter to start')
        data = self.recv_data(user.socket)
        if data == 'Enter':
            ServerControls.player_init(self.users[index], index, self.ship_sprites)
            self.game_started = True
        #
        # прием данных пользователя
        while True:
            data = self.recv_data(user.socket)
            if data == 'exit':
                self.delete_user(user)
                break  # пользователь вышел - цикл прерывается, поток завершается
            ServerControls.write_down_data(self.users[index],
                                           data,
                                           self.bullet_sprites)

            #для отладки
            #self.send_data(data)
            #

        print('Thread is ended')


    # принимает новых пользователей и выделяет под них потоки
    def accept_sockets(self):
        print('Server is running')
        # server cycle (main thread)
        while True:
            user_socket, user_address = self.accept()  # get connection
            print(f'New user {user_address} connected')

            # add new user
            new_user = BaseClasses.User(user_socket, user_address)
            self.users.append(new_user)
            index = len(self.users) - 1  # номер пользователя в списке
            self.users[index].index = index

            # выделение потока под пользователя
            host_accepted_user = Thread(
                    target=self.user_host,
                    args=(index, )
            )
            host_accepted_user.start()


    # игровой движок
    def game_engine_starter(self):
        # обрабатывает и рассылает данные игры
        game_engine_thread = Thread(
            target=self.game_engine
        )
        game_engine_thread.start()

    def game_engine(self):
        running = True
        pygame.init()
        pygame.display.set_mode((100, 1))
        clock = pygame.time.Clock()

        while running:
            clock.tick(self.FPS)
            #print('tick')
            if self.game_started:
                # считаем данные
                ServerControls.update_positions(
                    self.users,
                    self.ship_sprites,
                    self.bullet_sprites,
                    self.map_sprites
                )
                # отправляем данные
                self.send_data()
        pygame.quit()


    # удаление отключившегося игрока и завершение его потока
    def delete_user(self, user):
        self.users.remove(user)
        print(f'User {user.address} disconnected')
        self.game_started = False
        print('Game stopped')



# исполняющий код
if __name__ == '__main__':
    server = Server()
    server.set_up()
    server.close()

