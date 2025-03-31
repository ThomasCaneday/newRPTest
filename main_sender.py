# main_sender.py

import time
from datetime import datetime
from audio_recorder import AudioRecorder
from audio_processor import process_audio
from csv_handler import create_csv_row, write_csv_row
from transmitter import send_data

# --- Configuration ---
RECEIVER_IP = '192.168.0.218'  # Replace with the actual IP address of the receiver Pi
PORT = 5200
CSV_FILE = 'audio_data.csv'
RECORD_SECONDS = 1
SAMPLE_RATE = 44100

def main():
    recorder = AudioRecorder(rate=SAMPLE_RATE, record_seconds=RECORD_SECONDS)
    print("Starting audio recording. Press Ctrl+C to stop.")
    try:
        while True:
            # Timestamp for the current recording
            timestamp = datetime.now().isoformat()
            # Record audio for 1 second
            audio_data = recorder.record_audio()
            # Process the audio to extract features
            dominant_freq, amplitude = process_audio(audio_data, SAMPLE_RATE)
            row = create_csv_row(timestamp, dominant_freq, amplitude)
            # Write the row locally to a CSV file
            write_csv_row(CSV_FILE, row)
            # Prepare a CSV formatted row for transmission
            csv_row_str = f"{timestamp},{dominant_freq},{amplitude}\n"
            # Log latency and data rate
            latency, bytes_sent = send_data(csv_row_str, RECEIVER_IP, PORT)
            if latency is not None:
                data_rate = bytes_sent / latency  # bytes per second
                print(f"Sent {bytes_sent} bytes in {latency:.4f}s ({data_rate:.2f} B/s)")
            else:
                print("Transmission failed.")
    except KeyboardInterrupt:
        print("Stopping recording...")
    finally:
        recorder.terminate()

if __name__ == '__main__':
    main()
