# transmitter.py

import socket
import time

def send_data(data, receiver_ip, port=5200):
    """
    Send a string of data to the receiver via TCP.
    Returns latency (in seconds) and bytes sent.
    """
    start_time = time.time()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((receiver_ip, port))
            data_bytes = data.encode('utf-8')
            s.sendall(data_bytes)
        end_time = time.time()
        latency = end_time - start_time
        return latency, len(data_bytes)
    except Exception as e:
        print("Error sending data:", e)
        return None, 0
