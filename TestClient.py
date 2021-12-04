from Socket import BaseSocket
from threading import Thread
import GameEngine
import time
import sys

class Client(BaseSocket):
    def __init__(self):
        super(Client, self).__init__()

    def set_up(self,):
        self.connect(
            ('127.0.0.1', 4000)
        )
        self.run = True

        recv_server = Thread(
            target=self.recv_data
        )
        recv_server.start()

        send_server = Thread(
            target=self.send_data,
            args=(None,)
        )
        send_server.start()

    def send_data(self, data):
        Screen, BG_color = GameEngine.InitPygame()
        while self.run:
            GameEngine.UpdateWindow(Screen, BG_color)
            time.sleep(0.02)
            mess = GameEngine.events()
            self.send(mess.encode('utf8'))
            if mess == 'exit':
                self.run = False
                sys.exit()


    def recv_data(self, recv_socket=None):
        while self.run:
            data = self.recv(1024)
            print(data.decode('utf8'))


if __name__ == '__main__':
    client = Client()
    client.set_up()

