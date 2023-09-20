import sys

class console_param:
    def __init__(self):
        self.encrypt = True
        self.in_filename = ""
        self.out_filename = ""
        self.key = ""

def reduce_key(key):
    unique  = []
    for char in key:
        if char not in unique:
            unique.append(char)
    return unique

def fill_console(args):
    console = console_param()
    console.out_filename = args[-1]
    console.in_filename = args[-2]
    console.key = reduce_key(args[-3])
    for param in args[:-3]:
        if param == "-d":
            console.encrypt = False
    return console

def main(args):
    console = fill_console(args)
    with open(console.out_filename, 'w', encoding="utf-8") as fout:
        with open(console.in_filename, 'r', encoding="utf-8") as fin:
            crypt(fin, fout, console.encrypt, console.key)  

def crypt(fin, fout, flag, key):
    for line in fin:
        new_line = ""
        if flag:
            new_line = encrypt(line, key)
        else:
            new_line = decrypt(line, key)
        fout.write(new_line + '\n')

def order(char, key):
    if char in key:
        return key.index(char)
    else:
        less_sum = 0
        for c in key:
            if ord(c) > ord(char):
                less_sum += 1
        return ord(char) + less_sum

def char(code, key):
    codes = list(map(ord, key))
    if code in codes:
        return key[codes.index(code)]
    else:
        less_sum = 0
        for c in codes:
            if c > code:
                less_sum += 1
        return chr(code - less_sum)

def trim_line(line):
    if line[-1] == '\n':
        line = line[:-1]
    if len(line) % 2 == 1:
        line += " "
    return line 

def make_pair(line):
    pairs = []
    for pair in [line[i:i+ 2] for i in range(0, len(line), 2)]:
        if pair[0] == pair[1]:
            pairs.append(pair[0] + " ")
            pairs.append(" " + pair[1])
        else:
            pairs.append(pair)
    return pairs

def encrypt(line, key):
    line = trim_line(line)
    pairs = make_pair(line)
    new_pairs = []
    for pair in pairs:
        index = [order(char, key) for char in pair]
        rows = [int(i / 16) for i in index]
        column = [i % 16 for i in index]
        if rows[0] == rows[1]:
            column = [(column[0] + 1) % 16, (column[1] + 1) % 16]
        elif column[0] == column[1]:
            rows = [rows[0] + 1, rows[1] + 1]
        else:
            column = [column[1], column[0]]
        new_pairs.append("".join([char(rows[0] * 16 + column[0], key), char(rows[1] * 16 + column[1], key)]))
    return "".join(new_pairs)
     
def decrypt(line, key):
    line = trim_line(line)
    pairs = make_pair(line)
    new_pairs = []
    for pair in pairs:
        index = [order(char, key) for char in pair]
        rows = [int(i / 16) for i in index]
        column = [i % 16 for i in index]
        if rows[0] == rows[1]:
            column = [(column[0] - 1) % 16, (column[1] - 1) % 16]
        elif column[0] == column[1]:
            rows = [rows[0] - 1, rows[1] - 1]
        else:
            column = [column[1], column[0]]
        new_pairs.append("".join([char(rows[0] * 16 + column[0], key), char(rows[1] * 16 + column[1], key)]))
    return "".join(new_pairs)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("недостаточно аргументов")
    else:
        main(sys.argv[1:])
