import io
import sys
import re


class SrtSyntaxError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'SrtSyntaxError: ' + self.msg


class TimeStamp:
    def __init__(self):
        self.hour = None
        self.min = None
        self.sec = None
        self.milli_sec = None

    def from_str(self, index, string):
        if string[2] == ':' and string[5] == ':' and string[8] == ',':
            try:
                self.hour = int(string[0:2])
                self.min = int(string[3:5])
                self.sec = int(string[6:8])
                self.milli_sec = int(string[9:12])
            except ValueError:
                raise SrtSyntaxError('line %d "%s", not a time stamp' % (index, string))
        else:
            raise SrtSyntaxError('line %d "%s", not a time stamp' % (index, string))
        return self

    def __str__(self):
        return '%02d:%02d:%02d.%03d' % (self.hour, self.min, self.sec, self.milli_sec)

    def __eq__(self, other):
        if other is TimeStamp:
            if self.hour == other.hour and self.min == other.min and self.sec == other.sec:
                return True
        return False


class Text:
    def __init__(self):
        self.chs = None
        self.eng = None

    def from_list(self, list):
        # removing tags
        for num, str in enumerate(list):
            flag = 0
            tags = [0]
            for index, char in enumerate(str[1]):
                if char == '{' or char == '<':
                    if flag == 0:
                        start = index
                    flag += 1
                if char == '}' or char == '>':
                    flag -= 1
                    if flag == 0:
                        tags += [start, index + 1]
            tags.append(len(str[1]))
            no_tags_str = ''
            for index in range(int(len(tags) / 2)):
                no_tags_str += str[1][tags[index * 2]:tags[index * 2 + 1]]
            list[num] = no_tags_str

        # merge chs or eng in different lines
        zh = re.compile('[\u4e00-\u9fa5]')
        self.chs = []
        self.eng = []
        chs_str = ''
        eng_str = ''
        for str in list:
            flag = None
            if zh.search(str) is not None:
                if flag is None or flag:
                    chs_str += str + ' '
                else:
                    self.chs.append(chs_str)
                    chs_str = str
                flag = True
            else:
                if flag is None or not flag:
                    eng_str += str + ' '
                else:
                    self.chs.append(eng_str)
                    eng_str = str
                flag = False
        if len(chs_str) > 0:
            self.chs.append(chs_str)
        if len(eng_str) > 0:
            self.eng.append(eng_str)

        chs_tmp = []
        for line in self.chs:
            token = line.split()
            tmp = ''
            for each in token:
                tmp += each + ' '
            chs_tmp.append(tmp[:-1])
        self.chs = chs_tmp
        eng_tmp = []
        for line in self.eng:
            token = line.split()
            tmp = ''
            for each in token:
                tmp += each + ' '
            eng_tmp.append(tmp[:-1])
        self.eng = eng_tmp

        return self

    def __str__(self):
        string = ''
        for line in self.chs:
            string += line + '\n'
        for line in self.eng:
            string += line + '\n'
        return string


class TimeAxis:
    def __init__(self, line):
        axis = line[1].split()
        if len(axis) < 3:
            raise SrtSyntaxError('line %d "%s", missing necessary information for time axis' % (line[0], line[1]))
        if axis[1] != '-->':
            raise SrtSyntaxError('line %d "%s", missing necessary information for time axis' % (line[0], line[1]))
        self.start = TimeStamp().from_str(line[0], axis[0])
        self.end = TimeStamp().from_str(line[0], axis[2])

    def __str__(self):
        return str(self.start) + ' --> ' + str(self.end)


class SubItem:
    def __init__(self, sub_lines):
        if len(sub_lines) < 2:
            raise SrtSyntaxError('from line %d to line %d, missing necessary information for subtitle' % (
                sub_lines[0][0], sub_lines[-1][0]))
            exit(1)
        if sub_lines[0][1].isdigit():
            self.serial_num = int(sub_lines[0][1])
        else:
            raise SrtSyntaxError('line %d "%s", no serial number' % (sub_lines[0][0], sub_lines[0][1]))
            exit(1)
        self.time_axis = TimeAxis(sub_lines[1])
        self.text = Text().from_list(sub_lines[2:])

    def __str__(self):
        #return str(self.serial_num) + '\n' + str(self.time_axis) + '\n' + str(self.text)
        return str(self.time_axis) + '\n' + str(self.text)


class SrtSubFile:
    def __init__(self):
        self.sub_items = None

    def from_file(self, file_name):
        file = open(file_name, encoding='utf-8')
        sub_lines = []
        self.sub_items = []
        for index, line in enumerate(file):
            if index == 0:
                line = line[1:]  # delete the BOM head
            tokens = line.split()
            if len(tokens) == 0:
                if len(sub_lines) != 0:
                    self.sub_items.append(SubItem(sub_lines))
                    sub_lines = []
            else:
                sub_lines.append([index, line[:-1]])
        if len(sub_lines) != 0:
            self.sub_items.append(SubItem(sub_lines))
        return self

    def __str__(self):
        string = ''
        for item in self.sub_items:
            string += str(item) + '\n'
        return string

    def re_num(self):
        for index, item in enumerate(self.sub_items):
            item.serial_num = index + 1


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    try:
        sub_file = SrtSubFile().from_file(sys.argv[1])
    except SrtSyntaxError as e:
        print(e)
        exit(1)

    print(sub_file)
    """
    for item in sub_file.sub_items:
        if len(item.text.eng) != 1 and len(item.text.chs) != 1:
            print(item.serial_num)
    sub_file.re_num()

    scope = [None, None, None]
    for num, item in enumerate(sub_file.sub_items):
        scope[2] = item
        memo = []
        mv = []
        if scope[1] is not None and (len(scope[1].text.chs) != 1 or len(scope[1].text.eng) != 1):
            flag = None
            if len(scope[1].text.chs) == 0:
                flag = True
                print('missing chinese subtitle: ', end='')
            if len(scope[1].text.eng) == 0:
                flag = False
                print('missing english subtitle: ', end='')
            for each in scope:
                print(each)
            command = input().split()
            if command[0] == 'del':
                mv.append(index - 1)
            elif command[0] == 'mv':
                if command[1] == 'fo':
                    index = int(command[2])
                    if flag:
                        sub = scope[0].text.chs[0].split()
                    else:
                        sub = scope[0].text.eng[0].split()
                    sub1 = ''
                    sub2 = ''
                    for i, each in enumerate(sub):
                        if i < index - 1:
                            sub1 += each + ' '
                        else:
                            sub2 += each + ' '
                    if flag:
                        sub_file.sub_items[num - 2].text.chs = [sub1]
                        sub_file.sub_items[num - 1].text.chs = [sub2]
                    else:
                        sub_file.sub_items[num - 2].text.eng = [sub1]
                        sub_file.sub_items[num - 1].text.eng = [sub2]
            elif command[0] == 'ltr':
                memo.append(item)
            for each in scope:
                print(each)
        scope[0] = scope[1]
        scope[1] = scope[2]

        #for count, i in enumerate(mv):


    sub_file.re_num()

    print(sub_file)
    """
