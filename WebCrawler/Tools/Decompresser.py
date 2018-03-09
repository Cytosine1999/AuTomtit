import os
import zipfile
import rarfile


def decompress(name, select=lambda file_name, extension: True):
    # get file path and extension name
    path_name, f_n = os.path.split(name)
    _, ext = os.path.splitext(f_n)
    # create compressed file object
    if ext == '.zip':
        sub_file = zipfile.ZipFile(name)
    elif ext == '.rar':
        sub_file = rarfile.RarFile(name)
    else:
        return

    # recode GBK as UTF-8
    for component in sub_file.namelist():
        try:
            utf8_name = component.decode('utf-8')
        except UnicodeDecodeError:
            utf8_name = component.decode('gbk').encode('utf-8')

        # filter files
        _, extension = os.path.splitext(utf8_name)
        if extension in ['.zip', '.rar'] or select(utf8_name, extension):
            utf8_name = path_name + '/' + utf8_name
            pathname = os.path.dirname(utf8_name)
            if not os.path.exists(pathname) and pathname != '':
                os.makedirs(pathname)
            data = sub_file.read(component)
            if not os.path.exists(utf8_name):
                fo = open(utf8_name, "w")
                fo.write(data)
                fo.close()
            # decompress recursively
            decompress(utf8_name, select)
    sub_file.close()
    os.remove(name)
