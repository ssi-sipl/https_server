import serial
import threading
import time
import re
import subprocess

def read_from_port(ser):
    """ Continuously read data from the serial port. """
    while True:
        try:
            data = ser.readline().decode('utf-8').strip()
            if data:
                print(f"Received: {data}")
                if contains_numeric(data):
                    print("Numeric value detected. Executing rpi_client.py...")
                    execute_rpi_client()
        except serial.SerialException:
            print("Serial port closed")
            break
        except Exception as e:
            print(f"Error reading from port: {e}")
            break

def contains_numeric(data):
    """ Check if the data contains any numeric value. """
    return bool(re.search(r'\d', data))  # Regular expression to find any digit

def execute_rpi_client():
    """ Execute the rpi_client.py script located in the specified folder. """
    try:
        script_path = '/home/panther/Desktop/server_testing/https_server/rpi_client.py'
        subprocess.Popen(['python3', script_path])
        print("rpi_client.py executed.")
    except Exception as e:
        print(f"Error executing rpi_client.py: {e}")

def main():
    port = '/dev/ttyS0'  # Serial port should be a string
    baud_rate = 115200

    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Connected to {port} at {baud_rate} baud")

        read_thread = threading.Thread(target=read_from_port, args=(ser,))
        read_thread.daemon = True  # Allow thread to exit when main program exits
        read_thread.start()

        while True:  # Keep the main thread alive
            time.sleep(1)

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if 'ser' in locals():
            ser.close()
            print("Serial port closed")

if __name__ == "__main__":
    main()
