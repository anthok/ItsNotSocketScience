import socket


class Port(object):

    def __init__(self, number, type):
        self.number = int(number)
        if type.lower() == "udp":
            self.type = socket.SOCK_DGRAM
        else:
            self.type = socket.SOCK_STREAM
