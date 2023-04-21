import socket, cv2, numpy, json
from sys import argv
from datetime import date
from time import strftime, localtime, sleep
from colorama import Fore, Back, Style

status_color = {
    '+': Fore.GREEN,
    '-': Fore.RED,
    '*': Fore.YELLOW,
    ':': Fore.CYAN,
    ' ': Fore.WHITE
}

def display(status, data):
    print(f"{status_color[status]}[{status}] {Fore.BLUE}[{date.today()} {strftime('%H:%M:%S', localtime())}] {status_color[status]}{Style.BRIGHT}{data}{Fore.RESET}{Style.RESET_ALL}")

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((argv[1], int(argv[2])))
    display('+', f"Starting the sever on {Back.MAGENTA}{argv[1]}:{argv[2]}{Back.RESET}")
    server.listen()
    display(':', "Listening for Connections....")
    client_socket, client_address = server.accept()
    display('+', f"Client Connected = {Back.MAGENTA}{client_address[0]}:{client_address[1]}{Back.RESET}")
    display('+', "Starting the Live Video Stream")
    while True:
        data = b""
        while True:
            try:
                data += client_socket.recv(1024)
                data = json.loads(data)
                break
            except ValueError:
                pass
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
        if cv2.waitKey(1) & 0xFF == ord('q'):
            client_socket.send("0".encode())
            display('*', f"Disconnecting from {Back.MAGENTA}{client_address[0]}:{client_address[1]}{Back.RESET}")
            break
        sleep(1)
        client_socket.send("1".encode())
    server.close()
    display('*', f"Server Closed!")