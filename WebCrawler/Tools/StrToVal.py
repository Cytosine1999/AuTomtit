import time
import re


def get_time(msg):
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


def get_size(msg):
    if msg is None:
        return 0
    size_msg = msg.split()
    size_value = float(size_msg[0])
    size_unit = size_msg[1]
    size = None
    if size_unit == 'GiB':
        size = round(size_value * 1024 * 1024 * 1024)
    elif size_unit == 'MiB':
        size = round(size_value * 1024 * 1024)
    elif size_unit == 'KiB':
        size = round(size_value * 1024)
    if size is None:
        pass
    return size
