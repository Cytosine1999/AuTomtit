def get(msg):
    size_msg = msg.split()
    size_value = float(size_msg[1])
    size_unit = size_msg[2]
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
