import time


def get(msg):
    time_msg = msg.split()
    upload_time = None
    if len(time_msg) == 4:
        if time_msg[2] == 'mins':
            upload_time = time.time() - time_msg[1] * 60
    elif len(time_msg) == 3:
        if time_msg[1] == 'today':
            pass
        elif time_msg[1] == 'Y-day':
            pass
        elif time_msg[1][2] == '-':
            if time_msg[2][2] == ':':
                pass
            else:
                year = int(time_msg[2])
                if year > 1970:
                    pass
    if upload_time is None:
        pass
    return upload_time
