# main_receiver.py

import socket
import threading
from csv_handler import write_csv_row
import csv
import io
import time

CSV_STORAGE_FILE = 'received_audio_data.csv'
PORT = 5200

def process_csv_row(row):
    """
    Check if the frequency in the row is less than 50 Hz and print an alert.
    """
    try:
        timestamp, frequency, amplitude = row
        frequency = float(frequency)
        if frequency < 50:
            print(f"Alert: Frequency {frequency} Hz below 50 Hz at {timestamp}")
    except Exception as e:
        print("Error processing row:", e)

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        start_time = time.time()
        data = b""
        while True:
            packet = conn.recv(1024)
            if not packet:
                break
            data += packet
        end_time = time.time()

        latency = end_time - start_time
        bytes_received = len(data)
        data_rate = bytes_received / latency if latency > 0 else 0

        print(f"Received {bytes_received} bytes in {latency:.4f}s ({data_rate:.2f} B/s)")

        # Decode and process the received CSV row
        csv_data = data.decode('utf-8').strip()
        if csv_data:
            row = next(csv.reader([csv_data]))
            write_csv_row(CSV_STORAGE_FILE, row)
            process_csv_row(row)

        # Optional: log network metrics to file
        with open("receiver_network_log.csv", "a") as log_file:
            log_file.write(f"{time.time()},{addr[0]},{bytes_received},{latency:.6f},{data_rate:.2f}\n")

    except Exception as e:
        print("Error handling client:", e)
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', PORT))
        s.listen()
        print(f"Server listening on port {PORT}...")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.daemon = True
            client_thread.start()

if __name__ == '__main__':
    start_server()
