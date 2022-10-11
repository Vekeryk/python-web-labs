import socket
import threading

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def recieve():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except: 
            print("An error occured!")
            client.close()
            break

def write():
        while True:
            try:
                message = f'{nickname}: {input("")}'
                client.send(message.encode('ascii'))
            except: 
                print("An error occured!")
                client.close()
                break

receive_thread = threading.Thread(target=recieve)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()