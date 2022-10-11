import threading
import time
import socket

host = "127.0.0.1"
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'EXIT' or not message:
                client.close()
                break
            
            now = time.localtime()
            print(f'{message} {time.strftime("%H:%M:%S", now)}')
            time.sleep(5)
            bytes = client.send(message.encode('ascii'))
            if bytes != len(message.encode('ascii')):
                client.close()
                break
        except:
            client.close()
            break

def receive():
    while True:
        client, adress = server.accept()
        thread = threading.Thread(target=handle, args=(client,), daemon=True)
        thread.start()

print('Server is listening')
receive()