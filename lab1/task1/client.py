import socket
import threading
import time

print('Send "EXIT" for disconnect')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def recieve():
    while True:
        try:
            message = input("Enter your message: ")
            if message == '':
                continue
            client.send(message.encode('ascii'))
            message = client.recv(1024).decode('ascii')
            if message:
                now = time.localtime()
                print(f'{message} {time.strftime("%H:%M:%S", now)}')
        except: 
            print("You were disconnected!")
            client.close()
            break

receive_thread = threading.Thread(target=recieve)
receive_thread.start()
