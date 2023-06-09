# LAN Camera Streaming
A simple Server-Client model that uses TCP Connection for streaming Live Video from one device's camera to another device's screen on the same LAN (Local Area Network).

## Requirements
Language Used = Python3<br />
Modules/Packages used:
* socket
* cv2
* pickle
* sys
* datetime
* time
* colorama
<!-- -->
Install the dependencies:
```bash
pip install -r requirements.txt
```

## Input
# server.py
* '-H', "--host": IPv4 Address on which to start the Server (Default=0.0.0.0)
* '-p', "--port": Port on which to start the Server (Default=2626)
* '-b', "--buffer-size": Buffer Size for Receiving Data from the Clients (Default=1024)
* '-t', "--timeout": Timeout for accepting connection from Clients (Default=1)
# client.py
* '-H', "--host": IPv4 Address of the Server
* '-p', "--port": Port of the Server
* '-b', "--buffer_size": Buffer Size for Receiving Data from the Server (Default=1024)
<!-- -->
For example:
```bash
python server.py --host 0.0.0.0 --port 2626
```
Here **0.0.0.0** is the address on which to start the server and this specific address means that we can accept connections from any device on the LAN (Local Area Network). And **2626** is the port.<br />
For client to connect to this server, the client should type the LAN IP Address of the Device that runs "server.py".

## Output
After successful connection, the Device that runs "server.py" can see the Live Grayscale Video captured by the camera of the device that runs "client.py".