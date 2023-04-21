# Video Calling LAN
A simple Server-Client model that uses TCP Connection for streaming Live Grayscale Video from one device's camera to another device's screen on the same LAN (Local Area Network).

## Requirements
Language Used = Python3<br />
Modules/Packages used:
* socket
* cv2
* numpy
* json
* sys
* datetime
* time
* colorama

## Input
Both the programs "server.py" and "client.py" takes the same arguments from the command that is used to run the Python Program.
1. Address
2. Port
<!-- -->
For example:
```bash
python server.py 0.0.0.0 2626
```
Here '0.0.0.0' is the address on which to start the server and this specific address means that we can accept connections from any device on the LAN (Local Area Network). And 2626 is the port.<br />
For client to connect to this server, the client should type the LAN IP Address of the Device that runs "server.py".

## Output
After successful connection, the Device that runs "server.py" can see the Live Grayscale Video captured by the camera of the device that runs "client.py".

### Note
The video stream is too slow, even though its in Grayscale, because this program uses TCP Connection instead of UDP.<br />