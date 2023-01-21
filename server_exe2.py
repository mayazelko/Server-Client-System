#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020

import socket
import protocol_exe2
import glob
import os
import shutil
import subprocess
import pyautogui
from PIL import Image

IP = '_______' # your IP is here
# PHOTO_PATH = ????  # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd):
    # cmd = 'DIR c:\Users\User\Desktop\יב2'
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol_exe2.check_cmd first
    # if protocol_exe2.check_cmd(cmd):

    # Then make sure the params are valid

    list_params = cmd.split()

    if list_params[0] == 'TAKE_SCREENSHOT':
        return True, 'TAKE_SCREENSHOT', None

    if list_params[0] == 'SEND_PHOTO':
        return True, 'SEND_PHOTO', 'c:\\users\\user\\desktop\\screen.jpg'

    if list_params[0] == 'SEND_PHOTO_2':
        return True, 'SEND_PHOTO_2', 'c:\\users\\user\\desktop\\screen.jpg'

    if list_params[0] == 'DIR' and len(list_params) > 1:
        return True, 'DIR', list_params[1]

    if list_params[0] == 'DELETE' and len(list_params) > 1:
        return True, 'DELETE', list_params[1]

    if list_params[0] == 'COPY' and len(list_params) == 3:
        params_dict = dict()
        params_dict['COPY'] = list_params[1]
        params_dict['DESTINATION'] = list_params[2]
        return True, 'COPY', params_dict

    if list_params[0] == 'EXECUTE' and len(list_params) > 1:
        return True, 'EXECUTE', list_params[1]

    if list_params[0] == 'EXIT':
        return True, 'EXIT', None


    # (6)

    return False, 'NO_COMMAND', None


def handle_client_request(command, params):
    # Command: 'DIR'     Params: 'c:\Users\User\Desktop\יב2'
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """

    if command == 'DIR':
        params += '\\*.*'
        files_list = glob.glob(params)
        response = files_list
        return response # Returns the files_list

    if command == 'DELETE':
        os.remove(params)
        response = "The file in path: " + params + " was removed!"
        return response

    if command == 'COPY':
        shutil.copy(params['COPY'], params['DESTINATION'])
        response = "The file was copied!"
        return response

    if command == 'EXECUTE':
        # params = 'c:\\windows\\system32\\' + params
        for root, dir, files in os.walk('c:\\users\\user'):
            if params in files:
                params = os.path.join(root, params)
                break
        try:
            subprocess.call(params)
            response = "The process is running!"
        except:
            response = "Can't execute this process!"
        return response

    if command == 'TAKE_SCREENSHOT':
        image = pyautogui.screenshot()
        image.save('c:\\users\\user\\desktop\\screen.jpg')
        # image_size = os.path.getsize('c:\\users\\user\\desktop\\screen.jpg')
        # response = image_size
        response = "The server took a screenshot!"
        return response

    if command == 'SEND_PHOTO':
        global image_size
        image_size = os.path.getsize(params)
        response = image_size
        print("The image size: ", response)
        return response

    if command == 'SEND_PHOTO_2':
        image = open(params, 'rb')
        data = image.read(image_size)
        image.close()
        response = data
        return response


    # (7)


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol_exe2.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    # (1)

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol_exe2.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:

                # (6)

                # prepare a response using "handle_client_request"
                response = handle_client_request(command, params) # Response = files_list
                # add length field using "create_msg"
                if command == 'SEND_PHOTO_2':
                    client_socket.send(response)
                else:
                    packet = protocol_exe2.create_msg(str(response)) # Packet = '0099files_list'
                    # send to client
                    client_socket.send(packet)
                # Send the data itself to the client

                # (9)

                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                # send to client
                client_socket.send(response.encode())

        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            # send to client
            client_socket.send(response.encode())

            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
