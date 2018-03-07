import os
import zipfile
import rarfile


def decompress(file_name, expect=None):
    if expect is None:
        flag = True
        ext_name = ['.zip', '.rar']
    else:
        flag = False
        ext_name = expect + ['.zip', '.rar']

    path_name, f_n = os.path.split(file_name)
    _, ext = os.path.splitext(f_n)
    if ext == '.zip':
        sub_file = zipfile.ZipFile(file_name)
    elif ext == '.rar':
        sub_file = rarfile.RarFile(file_name)
    else:
        return
    for name in sub_file.namelist():
        try:
            utf8_name = name.decode('utf-8')
        except UnicodeDecodeError:
            utf8_name = name.decode('gbk').encode('utf-8')

        _, extension = os.path.splitext(utf8_name)
        skip = False
        for each in ext_name:
            if extension == each:
                skip = True

        if flag or skip:
            utf8_name = path_name + '/' + utf8_name
            pathname = os.path.dirname(utf8_name)
            if not os.path.exists(pathname) and pathname != '':
                os.makedirs(pathname)
            data = sub_file.read(name)
            if not os.path.exists(utf8_name):
                fo = open(utf8_name, "w")
                fo.write(data)
                fo.close()
            decompress(utf8_name, expect)
    sub_file.close()
    os.remove(file_name)
