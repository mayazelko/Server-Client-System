#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """

    # (3)
    command = data.split()
    if command[0] == 'TAKE_SCREENSHOT':
        return True
    if command[0] == 'SEND_PHOTO':
        return True
    if command[0] == 'DIR' and len(command) > 1:
        return True
    if command[0] == 'DELETE' and len(command) > 1:
        return True
    if command[0] == 'COPY' and len(command) == 3:
        return True
    if command[0] == 'EXECUTE' and len(command) > 1:
        return True
    if command[0] == 'EXIT':
        return True
    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """

    # (4)
    length = str(len(data))
    zfill_length = length.zfill(4)
    data = zfill_length + str(data)

    return data.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """

    # (5)
    return True, "OK"


