from decimal import *


# def getCoord(lines, i, to_find):
#     while i < len(lines) and to_find not in lines[i]:
#         i += 2
#     if i + 1 < len(lines):
#         return lines[i + 1]
#     return -1


class Polyline(object):
    def __init__(self, filename):
        self.filename = filename
        self.shapes = 0
        self.polyVertex = []
        self.ruleTab = []

    def __str__(self):
        out = "Polyline: " + str(self.shapes) + "\n"
        i = 0
        while i < len(self.polyVertex):
            out += "\tPolyline " + str(i + 1) + "\n"
            for coord in self.polyVertex[i]:
                out += "x: " + str(coord[0]) + " y: " + str(coord[1]) + "\n"
            i += 1
        out += "\nRules\n"
        for coord in self.ruleTab:
            out += "x: " + str(coord[0]) + " y: " + str(coord[1]) + " rule: " + str(coord[2]) + "\n"
        return out

    def getPolyInfo(self, lines, i):
        if lines[i + 2] != "1":
            return i + 2
        self.shapes += 1
        self.polyVertex.append(None)
        self.polyVertex[self.shapes - 1] = []
        while i < len(lines) and "VERTEX" not in lines[i]:
            i += 1
        while i < len(lines) and "VERTEX" in lines[i]:
            absPoint = lines[i + 4]
            ordPoint = lines[i + 6]
            self.polyVertex[self.shapes - 1].append((Decimal(absPoint), Decimal(ordPoint)))
            i += 8
        return i

    def getTextInfo(self, lines, i):
        bckpI = i + 1
        if lines[i + 2] != "1":
            return i + 2
        ordPoint = lines[i + 6]
        absPoint = lines[i + 4]
        while i < len(lines) and "  1" not in lines[i]:
            i += 1
        if i >= len(lines):
            return bckpI
        if "#" in lines[i + 1]:
            rule = lines[i + 1].replace("# ", "")
            print("New rule: " + str(rule))
        else:
            return bckpI
        self.ruleTab.append(None)
        self.ruleTab[len(self.ruleTab) - 1] = (Decimal(ordPoint), Decimal(absPoint), Decimal(rule))
        i += 2
        return i

    def parse(self):
        i = 0
        lines = [line.rstrip('\n') for line in open(self.filename)]
        while i < len(lines):
            curLine = lines[i]
            if "POLYLINE" in curLine:
                i = self.getPolyInfo(lines, i)
            elif "TEXT" in curLine:
                i = self.getTextInfo(lines, i)
            else:
                i += 1
