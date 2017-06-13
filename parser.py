import rules as rules
import polyline as polyline
from decimal import *

import tkinter as tk
from tkinter import filedialog

from os import listdir
from os.path import isfile, join


def checkIfInRuleTab(line, rulesTab):
    for tmp in rulesTab:
        if tmp[0] == line[0] and tmp[1] == line[1]:
            return tmp[3]  # Rule value
    return None


def writeCoord(file, ordCoord, absCoord):
    print("VERTEX\n  8\n1\n  10\n" + str(absCoord) + "\n  20\n" + str(ordCoord) + "\n  0")
    # file.write("VERTEX\n  8\n1\n  10\n" + str(absCoord) + "\n  20\n" + str(ordCoord) + "\n  0\n")


def printToFile(pieceIdx, grade, points, ruleObj, outPath, outFileName):
    # todo 3 digit and check open
    file = None
    # file = open(outPath + "/output/" + outFileName + "_" + str(piece) + "_" + str(grade) + ".dxf", "rw")
    # todo write header
    # file.write("POLYLINE:\n")
    print("POLYLINE:")
    i = 0
    while i < len(points.polyVertex[pieceIdx]):
        pathBeginruleValue = checkIfInRuleTab(points.polyVertex[pieceIdx][i], points.ruleTab)
        if pathBeginruleValue is not None:
            pathBegin = points.polyVertex[pieceIdx][i]
            stop = True
            r = i + 1
            while r < len(points.polyVertex[pieceIdx]) and stop is True:
                pathEndruleValue = checkIfInRuleTab(points.polyVertex[pieceIdx][r], points.ruleTab)
                if pathEndruleValue is not None:
                    stop = False
                pathEnd = points.polyVertex[pieceIdx][r]
                r += 1
            if r >= len(points.polyVertex[pieceIdx]):  # todo go to end
                writeCoord(file, points.polyVertex[pieceIdx][i][0], points.polyVertex[pieceIdx][i][1])
            else:
                x1 = pathBegin[0]
                x2 = pathEnd[0]
                y1 = pathBegin[1]
                y2 = pathEnd[1]
                # TODO APPLY RULE
                ruleAbs = ruleObj.rules[grade][0]
                ruleOrd = ruleObj.rules[grade][1]
                x1p = x1 + ruleAbs
                x2p = x2 + ruleAbs
                y1p = y1 + ruleOrd
                y2p = y2 + ruleOrd
                xFinal = (points.polyVertex[pieceIdx][i][0] - x1) * (x2p - x1p) / (x2 - x1)
                yFinal = (points.polyVertex[pieceIdx][i][1] - y1) * (y2p - y1p) / (y2 - y1)
                writeCoord(file, xFinal, yFinal)
        else:
            writeCoord(file, points.polyVertex[pieceIdx][i][0], points.polyVertex[pieceIdx][i][1])
        i += 1
        # file.close()


def work(dxf, rul, outPath, outFileName):
    points = polyline.Polyline(dxf)
    points.parse()
    # print(points)
    r = rules.Rules(rul)
    r.parse()
    # print(r)
    grade = 0
    while grade < int(r.sample_size):
        print("New grade")
        piece = 0
        while piece < len(points.polyVertex):
            printToFile(piece, grade, points, r, outPath, outFileName)
            piece += 1
        grade += 1


def selectFolder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory()


def getAllFileInFolder(path):
    return [f[:len(f) - 4] for f in listdir(path) if isfile(join(path, f)) and ".dxf" in f]


def main():
    path = selectFolder()
    print(path)
    listFiles = getAllFileInFolder(path)
    print(listFiles)
    for current in listFiles:
        work(current + ".dxf", current + ".rul", path, path + current)


main()
