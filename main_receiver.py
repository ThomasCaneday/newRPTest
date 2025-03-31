# main_receiver.py

import socket
import threading
from csv_handler import write_csv_row
import csv
import io

CSV_STORAGE_FILE = 'received_audio_data.csv'
PORT = 5000

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
        data = b""
        while True:
            packet = conn.recv(1024)
            if not packet:
                break
            data += packet
        # Decode and parse CSV data
        csv_data = data.decode('utf-8').strip()
        if csv_data:
            csv_reader = csv.reader(io.StringIO(csv_data))
            for row in csv_reader:
                write_csv_row(CSV_STORAGE_FILE, row)
                process_csv_row(row)
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
