# transmitter.py

import socket

def send_data(data, receiver_ip, port=5000):
    """
    Send a string of data to the receiver via TCP.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((receiver_ip, port))
            data_bytes = data.encode('utf-8')
            s.sendall(data_bytes)
    except Exception as e:
        print("Error sending data:", e)
