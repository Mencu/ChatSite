from socket import AF_INET, socket, SOCK_STREAM
#from server.user import User
import time
from threading import Thread
from client import Client

c1 = Client('Andrei')
c2 = Client('Cristi')

def update():

    msgs = []

    while True:

        time.sleep(0.1)
        new_messages = c1.get_messages()
        msgs.extend(new_messages)

        for msg in new_messages:
            print(msg)

            if msg == "exit":
                break

recv_thread = Thread(target=update).start()


c1.send_message("Hi")
time.sleep(5)
c2.send_message("Hello World")
time.sleep(2)
c1.send_message("what are you doing?")
time.sleep(2)
c2.send_message("exit")
time.sleep(2)
c1.send_message("exit")

'''
c1.disconnect()
time.sleep(1)
c2.disconnect()

def recv_msg():
    """receive messages form server
    :return None"""
    while True:

        try:
            msg = client_socket.recv(BUFSIZE).decode("utf8")
            messages.append(msg)
            print(msg)
        except Exception as e:
            print("[EXCEPTION]", e)
            break


def send_msg(msg):
    """send messages to server
    :return None"""
    client_socket.send(bytes(msg, "utf8"))
    if msg == "exit":
        #time.sleep(1)
        client_socket.close()
'''
