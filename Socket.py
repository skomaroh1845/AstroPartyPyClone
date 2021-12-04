import socket


class BaseSocket(socket.socket):

    # инициализирует сокет
    def __init__(self):
        super(BaseSocket, self).__init__(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self.run = False  # True когда сокет работает

    # настройки подключения
    def set_up(self):
        raise NotImplementedError()

    # отправляет данные
    def send_data(self, data):
        raise NotImplementedError()

    # получает данные
    def recv_data(self, recv_socket=None):
        raise NotImplementedError()
