import sys
import socket
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor

#set basic logging
logging.basicConfig(level=logging.INFO)
def send_data():
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('172.16.16.101', 45000)
        #logging.info(f"connecting to {server_address}")
        sock.connect(server_address)

        # Send data
        message = 'TIMEINI ADALAH DATA YANG DIKIRIM\r\n'
        logging.info(f"sending {message}")
        sock.sendall(message.encode('utf-8'))
        # Look for the response
        amount_received = 0
        amount_expected = 5
        while amount_received < amount_expected:
            data = sock.recv(64)
            amount_received += len(data)
            logging.info(f"{data.decode('utf-8')}")

    except Exception as ee:
        logging.info(f"ERROR: {str(ee)}")
        exit(0)
    finally:
        logging.info("closing")
        sock.close()

count = 0
time_test = 5
loop = 0
with ThreadPoolExecutor() as executor:
    start = time.perf_counter()
    container = set()
    while time.perf_counter() - start < time_test:
        future = executor.submit(send_data)
        container.add(future)
        completed = {x for x in container if x.done()}
        count = count + len(completed)
        container -= completed
        loop +=1

print(f"Total perulangan (loop) yang terjadi adalah {loop} perulangan")
print(f"Total successfull requests dalam {time_test} detik adalah {count} requests")
