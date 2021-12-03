from Socket import BaseSocket
from threading import Thread


class Client(BaseSocket):
    def __init__(self):
        super(Client, self).__init__()

    def set_up(self):
        self.connect(
            ('127.0.0.1', 4000)
        )
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
        while True:
            self.send(input('input message: ').encode('utf8'))


    def recv_data(self, recv_socket=None):
        while True:
            data = self.recv(1024)
            print(data.decode('utf8'))


if __name__ == '__main__':
    client = Client()
    client.set_up()
