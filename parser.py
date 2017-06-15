import rules as rules  # Rules Parser (RUL)
import polyline as polyline  # Polyline Parser (DXF)
from decimal import *  # Precision

import os  # Filesystem handling
import sys  # Exit

# MessageBox and File Selector
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Set to True for usefull logging
DEBUG = False

# Location of ABS and ORD in Array to be more readable
ABS = 0
ORD = 1


def checkIfInRuleTab(line, rulesTab):
    """
    Check if a Rule is needed for the given coordinate
    :param line: Line to check
    :param rulesTab: Tab of Rules
    :return: None if not, Rule Value if there is a rule
    """
    for tmp in rulesTab:
        if tmp[ABS] == line[ABS] and tmp[ORD] == line[ORD]:
            return tmp[2]  # Rule value
    return None


def writeCoord(file, absCoord, ordCoord):
    """
    Write the coordinates of the vector in the file at a DXF format
    :param file: File to write coord
    :param absCoord: Abs coord
    :param ordCoord: Ord coord
    """
    file.write("VERTEX\n  8\n1\n 10\n" + str(absCoord) + "\n 20\n" + str(ordCoord) + "\n  0\n")


def printToFile(pieceIdx, grade, points, ruleObj, outPath, outFileName):
    """
    Main Loop
    :param pieceIdx: Shape number
    :param grade: Grade
    :param points: Points object (containing all polylines and vector)
    :param ruleObj: Rules object containing all rules
    :param outPath: Path to write output
    :param outFileName: Name of the file to write output
    """

    #  First we try to open the output file -> PATH/output/FILE_NAME_SHAPE-NUMBER_GRADIENT-NUMBER.dxf
    filename = outPath + "/output/" + outFileName + "_" + "{0:0=3d}".format(int(pieceIdx)) + "_" + "{0:0=3d}".format(
        int(grade)) + ".dxf"
    try:
        file = open(filename, "w")
    except:
        raise RuntimeError("Can't open file: " + filename)

    # We write the header
    file.write("0\nSECTION\n  2\nHEADER  9\n$ACADVER\n  1\nAC1009\n  0\nENDSEC\n  0SECTION\n  2\nTABLES\n  0\nTABLE\n "
               " 2\nSTYLE\n  0\nSTYLE\n  \n2\nSTANDARD\n 70\n64\n 40\n0\n 41\n1\n 50\n0\n 71\n0\n 42\n\n0\n 3\ntxt\n  "
               "4\n\n  0\nENDTAB\n  0\nENDSEC\n  0\nSECTION\n  2\nENTITIES\n  0\nPOLYLINE\n  8\n1\n 10\n0\n 20\n0\n "
               "66\n1\n  0\n")

    # We loop on all the Vertex of the given shape
    i = 0
    while i < len(points.polyVertex[pieceIdx]):
        # We check if the current vertex got a Rule, if yes we get it
        pathBeginRuleValue = checkIfInRuleTab(points.polyVertex[pieceIdx][i], points.ruleTab)
        # In fact, this will never return None because we jump from Rule to Rule
        if pathBeginRuleValue is not None:
            # We save the begin vertex
            pathBegin = points.polyVertex[pieceIdx][i]
            r = i + 1
            # We search the next vertex with a Rule
            while r < len(points.polyVertex[pieceIdx]):
                pathEndRuleValue = checkIfInRuleTab(points.polyVertex[pieceIdx][r], points.ruleTab)
                pathEnd = points.polyVertex[pieceIdx][r]
                if pathEndRuleValue is not None:
                    break
                r += 1
            # The next Vertex with a rule is stored in pathEnd, and the value of the rule in pathEndRuleValue
            x1 = pathBegin[ABS]
            x2 = pathEnd[ABS]
            y1 = pathBegin[ORD]
            y2 = pathEnd[ORD]

            # We apply the rule to the vertex (-1 is there because a list start at 0 so Rule 1 = List[0])
            x1p = x1 + ruleObj.rules[int(pathBeginRuleValue - 1)][grade][ABS]
            x2p = x2 + ruleObj.rules[int(pathBeginRuleValue - 1)][grade][ORD]
            y1p = y1 + ruleObj.rules[int(pathBeginRuleValue - 1)][grade][ORD]
            y2p = y2 + ruleObj.rules[int(pathEndRuleValue - 1)][grade][ORD]

            # We write the coord of the origin point
            writeCoord(file, x1p, y1p)

            i += 1
            # We loop all the point between the begin and end point, we compute their coord and write them
            while i < len(points.polyVertex[pieceIdx]) and i < r:
                if x2 - x1 == 0 or x2p - x1p == 0:
                    xFinal = x1p
                else:
                    xFinal = (points.polyVertex[pieceIdx][i][ABS] - x1) * (Decimal(x2p - x1p) / (Decimal(x2 - x1))) + x1p
                if y2 - y1 == 0 or y2p - y1p == 0:
                    yFinal = y1p
                else:
                    yFinal = (points.polyVertex[pieceIdx][i][ORD] - y1) * (
                        Decimal(y2p - y1p) / (Decimal(y2 - y1))) + y1p
                writeCoord(file, xFinal, yFinal)
                i += 1
            writeCoord(file, x2p, y2p)
        else:
            raise RuntimeError("No custom rule found !")
    # We write the footer
    file.write("SEQEND\n  0\nENDSEC\n  0\nEOF")
    # We close the file and go on next gradient or shape
    file.close()


def work(dxf, rul, outPath, outFileName):
    points = polyline.Polyline(dxf)
    # We parse the vertex / polyline / shape
    points.parse()
    if DEBUG:
        print(points)
    # We parse the rules
    r = rules.Rules(rul)
    r.parse()
    if DEBUG:
        print(r)
    grade = 0
    # We loop all the grades and call printToFile with each grade
    while grade < int(r.sample_size):
        piece = 0
        # We loop all the piece and call printToFile with each piece
        while piece < len(points.polyVertex):
            printToFile(piece, grade, points, r, outPath, outFileName)
            piece += 1
        grade += 1


def selectFolder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory()


def getAllFileInFolder(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and ((".dxf" in f) or (".DXF" in f))]


def main():
    # We ask the user for a folder
    path = selectFolder()
    # We try to create an output folder inside
    try:
        if not os.path.exists(path + "/output"):
            os.makedirs(path + "/output")
    except:
        raise RuntimeError("Can't create output directory at " + path)
    # We fetch all .dxf or .DXF files inside the folder
    listFiles = getAllFileInFolder(path)
    # If none found then error
    if len(listFiles) == 0:
        raise RuntimeError("No file found (.dxf or .DXF)")
    # We loop all these files and call the work function with each one
    for current in listFiles:
        if ".dxf" in current:
            current = current[:len(current) - 4]
            work(path + "/" + current + ".dxf", path + "/" + current + ".rul", path + "/", current)
        else:
            current = current[:len(current) - 4]
            work(path + "/" + current + ".DXF", path + "/" + current + ".RUL", path + "/", current)


# START of the program
try:
    main()
except Exception as e:
    print(e)
    messagebox.showerror("Error", e)
    sys.exit(1)
