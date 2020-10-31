from threading import Thread
from socket import AF_INET, socket, SOCK_STREAM
import time
from user import User

# TODO: change encryption
# TODO: deploy on raspberry pi


#Global constants
HOST = 'localhost'
PORT = 5000
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 24
BUFSIZE = 1024

#Global variables
users = []

#setup server
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def broadcast(msg, name):
    '''Send messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return:
    '''
    for user in users:
        client = user.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION broadcast]", e)


def handle_client(user):
    '''Handles all messages from a client
    :param user: User
    :return None'''
    client = user.client

    #get user name
    name = client.recv(BUFSIZE).decode("utf8")
    user.set_name(name)

    #broadcast welcome msg
    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "")

    while True:
        try:
            msg = client.recv(BUFSIZE)

            #if user wants to leave, send exit and then remove user
            if msg == bytes("exit", "utf8"):
                client.close()
                users.remove(user)
                broadcast(bytes(f"{name}: has left the chat...", "utf8"), '')
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:
                broadcast(msg, name + ": ")
                print(f"{name}: ", msg.decode("utf8"))

        except Exception as e:
            print("[EXCEPTION handling]", e)
            break

def wait_connection(SERVER):
    '''Server waits for connections and adds them
    :param SERVER: socket
    :return None'''

    while True:
        try:
            client, addr = SERVER.accept()      # wait for connections
            user = User(addr, client)           # create new user for connection
            users.append(user)

            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target= handle_client, args= (user,)).start()
        except Exception as e:
            print("[EXCEPTION connection]", e)
            break

    print("SERVER crashed")



if __name__ == '__main__':
    #listen for connections
    try:
        SERVER.listen(MAX_CONNECTIONS)
    except Exception as e:
        print("[EXCEPTION before_connection]")

    print("[Start] Waiting for connections...")
    ACCEPT_THREAD = Thread(target=wait_connection, args= (SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()