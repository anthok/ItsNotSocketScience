from argparse import ArgumentParser
import socket, threading, os
import json, time
import net_objects
import pathlib
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ClientThread(threading.Thread):
    def __init__(self, log_dir, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.log_dir = log_dir
        self.csocket = clientsocket
        logger.info("New connection added: ", clientAddress)

    def run(self):
        logger("Connection from : ", clientAddress)

class SocketServer(threading.Thread):
    def __init__(self, port_obj):
        threading.Thread.__init__(self)
        self.port_obj = port_obj
        self.output_path = ""
        self.create_output_path()

    def create_output_path(self):
        if self.port_obj.type == socket.SOCK_STREAM:
            self.output_path = "logs/tcp/{}".format(self.port_obj.number)
        else:
            self.output_path = "logs/udp/{}".format(self.port_obj.number)

    def create_directory(self):
        pathlib.Path(self.output_path).mkdir(parents=True, exist_ok=True)

    def run(self):
        self.create_directory()
        server = socket.socket(socket.AF_INET, self.port_obj.type)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", self.port_obj.number))
        if self.port_obj.type == socket.SOCK_STREAM:
            logger.info("TCP: {}".format(self.port_obj.number))
            while True:
                server.listen(1)
        #         clientsock, clientAddress = server.accept()
        #         newthread = ClientThread(clientAddress, clientsock)
        #         newthread.start()
        else:
            logger.info("UDP: {}".format(self.port_obj.number))
            bytesAddressPair = server.recvfrom(1024)

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle


def main():
    parser = ArgumentParser(description="INSS")
    parser.add_argument("-c", dest="config", required=True,
                        help="config file", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser = parser.parse_args()
    j_data = json.loads(parser.config.read())

    port_list = []
    for p in j_data["tcp"]:
        port_list.append(net_objects.Port(p, "tcp"))
    for p in j_data["udp"]:
        port_list.append(net_objects.Port(p, "udp"))

    thread_keeper = []
    for port_obj in port_list:
        server = SocketServer(port_obj)
        thread_keeper.append(server)

    for thread in thread_keeper:
        thread.start()

if __name__ == "__main__":
    main()