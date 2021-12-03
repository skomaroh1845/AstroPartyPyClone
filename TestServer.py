from Socket import BaseSocket
from threading import Thread


class Server(BaseSocket):
    def __init__(self):
        super(Server, self).__init__()
        self.users = []

    def set_up(self):
        self.bind(
            ('127.0.0.1', 4000)
        )
        self.listen()
        self.accept_sockets()

    def send_data(self, data):
        for user in self.users:
            user.send(data.encode('utf8'))

    def recv_data(self, recv_socket=None):
        print('listening user')
        while True:
            data = recv_socket.recv(1024)
            data = data.decode('utf8')
            print(f'User send {data}')

    def accept_sockets(self):
        print('Server is running')
        # server cycle
        while True:
            user_socket, user_address = self.accept()  # get connection
            print(f'New user {user_address} connected')
            self.users.append(user_socket)  # add new user
            recv_accepted_user = Thread(
                target=self.recv_data,
                args=(user_socket,)
            )
            recv_accepted_user.start()


if __name__ == '__main__':
    server = Server()
    server.set_up()
