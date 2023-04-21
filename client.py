import socket, cv2, json
from sys import argv
from datetime import date
from time import strftime, localtime
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
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    display(':', f"Connecting to {Back.MAGENTA}{argv[1]}:{argv[2]}{Back.RESET}")
    client.connect((argv[1], int(argv[2])))
    display('+', f"Connected to {Back.MAGENTA}{argv[1]}:{argv[2]}{Back.RESET}")
    video_capture = cv2.VideoCapture(0)
    display(':', "Sending Live Video Stream")
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        send_str = ""
        for row in frame:
            send_str += f"{':'.join([str(item) for item in row])};"
        serealized_data = json.dumps(send_str[:-1])
        client.send(serealized_data.encode())
        serealized_data = json.dumps(send_str[:-1]+"E")
        status = client.recv(1).decode()
        if status == "0":
            display('*', "Exit Message received")
            break
    client.close()
    video_capture.release()
    display('*', "Disconnected from Server!")