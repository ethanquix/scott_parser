import rules as rules
import polyline as polyline
from decimal import *

import tkinter as tk
from tkinter import filedialog

import os
from os import listdir, makedirs
from os.path import isfile, join


ABS = 0
ORD = 1


def checkIfInRuleTab(line, rulesTab):
    for tmp in rulesTab:
        if tmp[ABS] == line[ABS] and tmp[ORD] == line[ORD]:
            return tmp[2]  # Rule value
    return None


def writeCoord(file, ordCoord, absCoord):
    # print("VERTEX\n  8\n1\n  10\n" + str(absCoord) + "\n  20\n" + str(ordCoord) + "\n  0")
    file.write("VERTEX\n  8\n1\n 10\n" + str(absCoord) + "\n 20\n" + str(ordCoord) + "\n  0\n")


def printToFile(pieceIdx, grade, points, ruleObj, outPath, outFileName):
    # todo 3 digit and check open
    file = None
    filename = outPath + "/output/" + outFileName + "_" + "{0:0=3d}".format(int(pieceIdx)) + "_" + "{0:0=3d}".format(int(grade)) + ".dxf"
    try:
        file = open(filename, "w")
    except:
        raise Exception("Can't open file: " + filename)
    # todo write header
    file.write("POLYLINE\n  8\n1\n 10\n0\n 20\n0\n 66\n1\n  0\n")
    i = 0
    while i < len(points.polyVertex[pieceIdx]):
        pathBeginRuleValue = checkIfInRuleTab(points.polyVertex[pieceIdx][i], points.ruleTab)
        if pathBeginRuleValue is not None:
            pathBegin = points.polyVertex[pieceIdx][i]
            stop = True
            r = i + 1
            while r < len(points.polyVertex[pieceIdx]) and stop is True:
                pathEndRuleValue = checkIfInRuleTab(points.polyVertex[pieceIdx][r], points.ruleTab)
                if pathEndRuleValue is not None:
                    stop = False
                pathEnd = points.polyVertex[pieceIdx][r]
                r += 1
            if r >= len(points.polyVertex[pieceIdx]):  # todo go to end
                writeCoord(file, points.polyVertex[pieceIdx][i][ABS], points.polyVertex[pieceIdx][i][ORD])
            else:
                x1 = pathBegin[ABS]
                x2 = pathEnd[ABS]
                y1 = pathBegin[ORD]
                y2 = pathEnd[ORD]
                # TODO APPLY RULE
                ruleAbsBegin = ruleObj.rules[int(pathBeginRuleValue)][grade][ABS]
                ruleOrdBegin = ruleObj.rules[int(pathEndRuleValue)][grade][ORD]
                ruleAbsEnd = ruleObj.rules[int(pathBeginRuleValue)][grade][ABS]
                ruleOrdEnd = ruleObj.rules[int(pathEndRuleValue)][grade][ORD]
                x1p = x1 + ruleAbsBegin
                x2p = x2 + ruleAbsEnd
                y1p = y1 + ruleOrdBegin
                y2p = y2 + ruleOrdEnd
                xFinal = (points.polyVertex[pieceIdx][i][ABS] - x1) * Decimal(x2p - x1p) / (Decimal(x2 - x1) if Decimal(x2 - x1) != 0 else 1)
                yFinal = (points.polyVertex[pieceIdx][i][ORD] - y1) * Decimal(y2p - y1p) / (Decimal(y2 - y1) if Decimal(y2 - y1) != 0 else 1)
                writeCoord(file, xFinal, yFinal)
        else:
            writeCoord(file, points.polyVertex[pieceIdx][i][ABS], points.polyVertex[pieceIdx][i][ORD])
        i += 1
    file.close()


def work(dxf, rul, outPath, outFileName):
    points = polyline.Polyline(dxf)
    points.parse()
    # print(points)
    r = rules.Rules(rul)
    r.parse()
    # print(r)
    grade = 0
    while grade < int(r.sample_size):
        piece = 0
        while piece < len(points.polyVertex):
            printToFile(piece, grade, points, r, outPath, outFileName)
            piece += 1
        grade += 1


def selectFolder():
    return "/home/dimitri/projets/scott_parser/sample"
    # root = tk.Tk()
    # root.withdraw()
    # return filedialog.askdirectory()


def getAllFileInFolder(path):
    return [f[:len(f) - 4] for f in listdir(path) if isfile(join(path, f)) and ".dxf" in f]


def main():
    path = selectFolder()
    print(path)
    try:
        if not os.path.exists(path + "/output"):
            makedirs(path + "/output")
    except:
        raise "Can't create output directory at " + path
    listFiles = getAllFileInFolder(path)
    print(listFiles)
    for current in listFiles:
        work(path + "/" + current + ".dxf", path + "/" + current + ".rul", path + "/", current)


main()
