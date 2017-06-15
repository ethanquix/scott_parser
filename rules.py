from decimal import *


class Rules(object):
    def __init__(self, filename):
        self.filename = filename
        self.rules = []
        self.size_list = []
        self.sample_size = 0
        self.content = ""

    def __str__(self):
        i = 0
        out = "Number of Sizes: " + str(self.sample_size) + "\nSize List: " + str(self.size_list) + "\n\n"
        while i < len(self.rules):
            out += "\tRule " + str(i + 1) + "\n"
            for coord in self.rules[i]:
                out += "x: " + str(coord[0]) + " y: " + str(coord[1]) + "\n"
            i += 1
        return out

    def getInfoSize(self, src):
        tmp = src[10:].split(" ")[1:]
        # TODO check if value is good int
        for val in tmp:
            self.size_list.append(int(val))

    def parse(self):
        # todo try and except
        try:
            lines = [line.rstrip('\n') for line in open(self.filename)]
        except:
            raise "Can't open file: " + self.filename
        i = 0
        ruleNumber = 0
        while i < len(lines):
            curLine = lines[i]
            if "SIZE LIST:" in curLine:
                self.getInfoSize(curLine)
                i += 1
            elif "NUMBER OF SIZES:" in curLine:
                self.sample_size = curLine[17:]
                # todo check if is int or throw
                i += 1
            elif "RULE:" in curLine:
                i += 1
                ruleNumber += 1
                tmp = ""
                while ("RULE:" not in lines[i]) and ("END" not in lines[i]):
                    tmp += lines[i]
                    i += 1
                tmp = tmp.replace(',', '')
                tmp = tmp.split('     ')[1:]
                if len(tmp) % 2 != 0:
                    raise Exception("Invalid number of mult for rule " + str(ruleNumber) + " : mult : " + str(tmp))
                j = 0
                self.rules.append(None)
                self.rules[ruleNumber - 1] = []
                while j < len(tmp):
                    # Todo check if convert good
                    self.rules[ruleNumber - 1].append((Decimal(tmp[j]), Decimal(tmp[j + 1])))
                    j += 2
            else:
                i += 1
