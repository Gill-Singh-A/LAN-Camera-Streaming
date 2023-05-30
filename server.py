import socket, cv2, numpy, json, threading
from datetime import date
from optparse import OptionParser
from time import strftime, localtime
from colorama import Fore, Back, Style

status_color = {
    '+': Fore.GREEN,
    '-': Fore.RED,
    '*': Fore.YELLOW,
    ':': Fore.CYAN,
    ' ': Fore.WHITE
}

HOST = "0.0.0.0"
PORT = 2626
BUFFER_SIZE = 1024
TIMEOUT = 1

def display(status, data):
    print(f"{status_color[status]}[{status}] {Fore.BLUE}[{date.today()} {strftime('%H:%M:%S', localtime())}] {status_color[status]}{Style.BRIGHT}{data}{Fore.RESET}{Style.RESET_ALL}")

def get_arguments(*args):
    parser = OptionParser()
    for arg in args:
        parser.add_option(arg[0], arg[1], dest=arg[2], help=arg[3])
    return parser.parse_args()[0]

class Server:
    def __init__(self, host, port, buffer_size=1024, timeout=1, verbose=False):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.timeout = timeout
        self.verbose = verbose
        self.clients = {}
        self.accept_clients = False
        self.acceptClientThread = threading.Thread(target=self.acceptClient, daemon=True)
        self.lock = threading.Lock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.socket.bind((host, port))
    def listen(self):
        self.socket.listen()
        if self.verbose:
            display(':', f"Started listening on {Back.MAGENTA}{self.host}:{self.port}{Back.RESET}")
    def acceptClient(self):
        while self.accept_clients:
            try:
                client_socket, client_address = self.socket.accept()
                self.clients[client_address] = client_socket
                if self.verbose:
                    with self.lock:
                        display('+', f"Client Connected = {Back.RESET}{client_address[0]}:{client_address[1]}{Back.MAGENTA}")
            except:
                pass
    def acceptClients(self, mode):
        self.accept_clients = mode
        if mode:
            self.acceptClientThread.start()
        elif self.acceptClientThread.is_alive():
            self.acceptClientThread.join()
            self.acceptClientThread = threading.Thread(target=self.acceptClient, daemon=True)
    def send(self, client_address, data):
        serealized_data = json.dumps(data)
        self.clients[client_address].send(serealized_data.encode())
    def receive(self, client_address):
        data = b""
        while True:
            try:
                data += self.clients[client_address].recv(self.buffer_size)
                data = json.loads(data)
                break
            except ValueError:
                pass
        return data
    def close(self):
        for client_socket in self.clients.values():
            client_socket.close()
        self.socket.close()

if __name__ == "__main__":
    data = get_arguments(('-H', "--host", "host", f"IPv4 Address on which to start the Server (Default Value={HOST})"),
                         ('-p', "--port", "port", f"Port on which to start the Server (Default Value={PORT})"),
                         ('-b', "--buffer-size", "buffer_size", f"Buffer Size for Receiving Data from the Clients (Default Value={BUFFER_SIZE})"),
                         ('-t', "--timeout", "timeout", "timeout", f"Timeout for accepting connection from Clients (Default Value={TIMEOUT})"))
    if not data.host:
        data.host = HOST
    if not data.port:
        data.port = PORT
    else:
        data.port = int(data.port)
    if not data.buffer_size:
        data.buffer_size = BUFFER_SIZE
    else:
        data.buffer_size = int(data.buffer_size)
    if not data.timeout:
        data.timeout = TIMEOUT
    else:
        data.timeout = int(data.timeout)
    server = Server(data.host, data.port, data.buffer_size, data.timeout, True)
    display('+', f"Starting the sever on {Back.MAGENTA}{data.host}:{data.port}{Back.RESET}")
    server.listen()
    server.acceptClients(True)
    display(':', "Listening for Connections....")
    while len(server.clients) == 0:
        pass
    server.acceptClients(False)
    client_address = list(server.clients.keys())[0]
    display('+', "Starting the Live Video Stream")
    while cv2.waitKey(1) != 113:
        data = server.receive(client_address)
        if data == "0":
            break
        data = data.split(';')
        image = []
        for row in data:
            temp = []
            row = row.split(':')
            for pixel in row:
                temp.append(int(pixel))
            image.append(temp)
        image = numpy.uint8(numpy.around(image))
        cv2.imshow("Image", image)
        server.send(client_address, "1")
    else:
        server.receive(client_address)
        server.send(client_address, "0")
        display('*', f"Disconnecting from {Back.MAGENTA}{client_address[0]}:{client_address[1]}{Back.RESET}")
    server.close()
    display('*', f"Server Closed!")