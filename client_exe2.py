#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020
import io
import socket
import time
import PIL.Image as Image

import protocol_exe2


IP = '10.0.0.18'
# SAVED_PHOTO_LOCATION = ???? # The path + filename where the copy of the screenshot at the client should be saved

def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """

    if cmd == 'SEND_PHOTO':
        length = my_socket.recv(4).decode()
        global image_size
        image_size = my_socket.recv(int(length)).decode() # 2000000
        packet = protocol_exe2.create_msg('SEND_PHOTO_2')
        my_socket.send(packet) # SEND_PHOTO_2
        handle_server_response(my_socket, 'SEND_PHOTO_2')

    if cmd == 'SEND_PHOTO_2':
        # length = my_socket.recv(1).decode()
        data = my_socket.recv(int(image_size))
        file = open('client_image.jpg', 'wb')
        file.write(data)
        file.close()
        print("The image is in your project")
        cmd = input("Please enter command:\n")
        packet = protocol_exe2.create_msg(cmd)
        my_socket.send(packet)

    else:
        length = my_socket.recv(4).decode()
        data = my_socket.recv(int(length)).decode()
        print(data)

    # (8) treat all responses except SEND_PHOTO

    # (10) treat SEND_PHOTO


def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, 8820))

    # (2)

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n") # e.g DIR c:\Users\User\Desktop\יב2
        if protocol_exe2.check_cmd(cmd):
            packet = protocol_exe2.create_msg(cmd)
            my_socket.send(packet) # The server received: '0029DIR c:\Users\User\Desktop\יב2' encoded
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()

if __name__ == '__main__':
    main()