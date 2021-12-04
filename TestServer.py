from Socket import BaseSocket
from threading import Thread
import math
import sys

class Server(BaseSocket):
    def __init__(self):
        super(Server, self).__init__()
        self.users = []
        self.x = 0
        self.phi = 0
        self.turning = False
        self.bullets = 10

    def set_up(self):
        self.bind(
            ('127.0.0.1', 4000)
        )
        self.run = True
        self.listen()
        self.accept_sockets()

    def send_data(self, data):
        for user in self.users:
            user.send(data.encode('utf8'))

    def recv_data(self, recv_socket=None):
        print('listening user')
        while self.run:
            data = recv_socket.recv(1024)
            data = data.decode('utf8')
            if data == 'exit':
                self.run = False
                sys.exit()
            #print(f'User send {data}')
            mess = self.update_positions(data)
            self.send_data(mess)


    def accept_sockets(self):
        print('Server is running')
        # server cycle
        while self.run:
            user_socket, user_address = self.accept()  # get connection
            print(f'New user {user_address} connected')
            self.users.append(user_socket)  # add new user

            recv_accepted_user = Thread(
                target=self.recv_data,
                args=(user_socket,)
            )
            recv_accepted_user.start()

    def update_positions(self, data):
        if data == '+':
            self.turning = True
        if data == '-':
            self.turning = False
        if data == 'fire':
            self.bullets -= 1
            print('fire')
        if self.turning:
            self.phi += 0.01
            print('n')

        self.x += 0.01*math.cos(self.phi)
        return f'x:{round(self.x, 1)}; phi:{round(self.phi,2)}; bullets:{self.bullets}'


if __name__ == '__main__':
    server = Server()
    server.set_up()
