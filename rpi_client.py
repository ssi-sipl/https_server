import serial
import requests
import time

# UART setup
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

# HTTP server details
server_url = 'http://192.168.1.4:8080'

while True:
    # Read data from UART
    uart_data = ser.readline().decode('utf-8').strip()
    
    if uart_data:
        # Send data to HTTP server
        try:
            response = requests.post(
                server_url,
                data={'uart_data': uart_data}
            )
            print(f"Server response: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to server: {e}")
    
    time.sleep(1)  # Wait for 1 second before reading again
