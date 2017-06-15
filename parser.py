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


def writeCoord(file, absCoord, ordCoord):
    # print(str(absCoord), str(ordCoord))
    # print("VERTEX\n  8\n1\n  10\n" + str(absCoord) + "\n  20\n" + str(ordCoord) + "\n  0")
    file.write("VERTEX\n  8\n1\n 10\n" + str(absCoord) + "\n 20\n" + str(ordCoord) + "\n  0\n")


def printToFile(pieceIdx, grade, points, ruleObj, outPath, outFileName):
    # todo 3 digit and check open
    file = None
    filename = outPath + "/output/" + outFileName + "_" + "{0:0=3d}".format(int(pieceIdx)) + "_" + "{0:0=3d}".format(
        int(grade)) + ".dxf"
    try:
        file = open(filename, "w")
    except:
        raise Exception("Can't open file: " + filename)
    # todo write header
    file.write("0\nSECTION\n  2\nHEADER  9\n$ACADVER\n  1\nAC1009\n  0\nENDSEC\n  0SECTION\n  2\nTABLES\n  0\nTABLE\n "
               " 2\nSTYLE\n  0\nSTYLE\n  \n2\nSTANDARD\n 70\n64\n 40\n0\n 41\n1\n 50\n0\n 71\n0\n 42\n\n0\n 3\ntxt\n  "
               "4\n\n  0\nENDTAB\n  0\nENDSEC\n  0\nSECTION\n  2\nENTITIES\n  0\nPOLYLINE\n  8\n1\n 10\n0\n 20\n0\n "
               "66\n1\n  0\n")
    i = 0
    while i < len(points.polyVertex[pieceIdx]):
        pathBeginRuleValue = checkIfInRuleTab(points.polyVertex[pieceIdx][i], points.ruleTab)
        # print("begin", pathBeginRuleValue)
        if pathBeginRuleValue is not None:
            pathBegin = points.polyVertex[pieceIdx][i]
            r = i + 1
            while r < len(points.polyVertex[pieceIdx]):
                pathEndRuleValue = checkIfInRuleTab(points.polyVertex[pieceIdx][r], points.ruleTab)
                pathEnd = points.polyVertex[pieceIdx][r]
                if pathEndRuleValue is not None:
                    break
                r += 1
            # print("end", pathEndRuleValue)
            # if r >= len(points.polyVertex[pieceIdx]):  # todo go to end
            #     writeCoord(file, points.polyVertex[pieceIdx][i][ABS], points.polyVertex[pieceIdx][i][ORD])
            #     i += 1
            if True:
                x1 = pathBegin[ABS]
                x2 = pathEnd[ABS]
                y1 = pathBegin[ORD]
                y2 = pathEnd[ORD]
                # TODO APPLY RULE
                # TODO -1 because stored as abs value but list of rules sytart at 0 so rules[X] = rule X - 1 in reality
                ruleAbsBegin = ruleObj.rules[int(pathBeginRuleValue - 1)][grade][ABS]
                ruleOrdBegin = ruleObj.rules[int(pathBeginRuleValue - 1)][grade][ORD]
                ruleAbsEnd = ruleObj.rules[int(pathEndRuleValue - 1)][grade][ABS]
                ruleOrdEnd = ruleObj.rules[int(pathEndRuleValue - 1)][grade][ORD]
                # print("Rules: ", ruleAbsBegin, ruleAbsEnd, ruleOrdBegin, ruleOrdEnd)
                x1p = x1 + ruleAbsBegin
                x2p = x2 + ruleAbsEnd
                y1p = y1 + ruleOrdBegin
                y2p = y2 + ruleOrdEnd

                # print("FROM - TO ", end="")
                # print(i, r)
                # print("First rule: ", end="")
                writeCoord(file, x1p, y1p)
                # if x2 - x1 != 0 and x2p - x1p != 0:
                    # print("scale mult x= ", Decimal(x2p - x1p) / Decimal(x2 - x1))
                    # print("x2p: ", x2p, " x1p: ", x1p, " x2: ", x2, " x1: ", x1)
                    # print(points.polyVertex[pieceIdx][i][ABS], x1, y1, x2, y2, x1p, x2p, Decimal(x2p - x1p),
                    #       Decimal(x2 - x1))

                i += 1
                while i < len(points.polyVertex[pieceIdx]) and i < r:
                    if x2 - x1 == 0 or x2p - x1p == 0:
                        xFinal = x1p
                    else:
                        xFinal = (points.polyVertex[pieceIdx][i][ABS]-x1) * (Decimal(x2p - x1p) / (Decimal(x2 - x1)))+x1p
                    # print(xFinal)
                    if y2 - y1 == 0 or y2p - y1p == 0:
                        yFinal = y1p
                    else:
                        yFinal = (points.polyVertex[pieceIdx][i][ORD]-y1) * (Decimal(y2p - y1p) / (Decimal(y2 - y1)))+y1p
                    writeCoord(file, xFinal, yFinal)
                    i += 1
                # print("End rule: ", end="")
                writeCoord(file, x2p, y2p)
        else:
            print("souldnt be there")
            writeCoord(file, points.polyVertex[pieceIdx][i][ABS], points.polyVertex[pieceIdx][i][ORD])
            i += 1
            # print(i)
            # print(len(points.polyVertex[pieceIdx]))
    file.write("SEQEND\n  0\nENDSEC\n  0\nEOF")
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
    # return "/home/dimitri/projets/scott_parser/sample"
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory()


def getAllFileInFolder(path):
    return [f[:len(f) - 4] for f in listdir(path) if isfile(join(path, f)) and (".dxf" or ".DXF") in f]


def main():
    path = selectFolder()
    # print(path)
    try:
        if not os.path.exists(path + "/output"):
            makedirs(path + "/output")
    except:
        raise "Can't create output directory at " + path
    listFiles = getAllFileInFolder(path)
    # print(listFiles)
    for current in listFiles:
        if ".dxf in current":
            work(path + "/" + current + ".dxf", path + "/" + current + ".rul", path + "/", current)
        else:
            work(path + "/" + current + ".DXF", path + "/" + current + ".RUL", path + "/", current)


main()
