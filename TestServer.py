from Socket import BaseSocket
from threading import Thread
import math
import sys
from BaseClasses import User


class Server(BaseSocket):
    def __init__(self):
        super(Server, self).__init__()
        self.users = []


    # запуск сервера
    def set_up(self):
        self.bind(
            ('172.20.10.3', 4000)
        )
        self.listen()
        self.accept_sockets()


    def send_data(self, data):
        # отправка данных пользователям
        for user in self.users:
            user.socket.send(data.encode('utf8'))


    def recv_data(self, recv_socket=None):
        # принимает данные от пользователей в реальном времени
        data = recv_socket.recv(1024)
        return data.decode('utf8')


    def user_host(self, index):
        # занимается обработкой пользователя
        # инициализация клиента пользователя
        # загрузка карты
        self.send_data('Welcome to the best game ever!')
        # обмен данными
        user = self.users[index]
        while True:
            data = self.recv_data(user.socket)
            # запись и обработка данных
            if data == 'exit':
                self.close()
                sys.exit()
            data = self.update_game(data, index)
            self.send_data(data)


    def accept_sockets(self):
        print('Server is running')
        # server cycle
        # принимает новых пользователей и выделяет под них потоки
        while True:
            try:
                user_socket, user_address = self.accept()  # get connection
                print(f'New user {user_address} connected')

                # add new user
                new_user = User(user_socket, user_address)
                self.users.append(new_user)
                index = len(self.users) - 1  # номер пользователя в списке
                self.users[index].index = index

                # выделение потока под пользователя
                host_accepted_user = Thread(
                    target=self.user_host,
                    args=(index, )
                )
                host_accepted_user.start()

            except:
                break

    def update_game(self, data, index):
        return 'data arrived'



if __name__ == '__main__':
    server = Server()
    server.set_up()
