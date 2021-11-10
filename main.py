import os
import sys

extension = ".kr"


def listToString(_list: list):

    string = ""

    for char in _list:
        string += char

    return string


def ArrangeTabs(_line: str):
    _list = list(_line)
    # print(_list)

    for i in _list:
        if _list.index(i) == 0 and i == "?":
            _list[_list.index(i)] = "    "
        elif _list[_list.index(i) - 1] == "    " and i == "?":
            _list[_list.index(i)] = "    "

    return listToString(_list)


def EvalLine(_line: str):
    line = ""
    _line = _line.replace("    ", "?")

    #
    if _line[:8] == "değişken":
        temp_list = list(_line)
        temp_list[:8] = ""

        line = listToString(temp_list)

    # print ()
    if _line[:6] == "yazdır":
        temp_list = list(_line)
        temp_list[:6] = "print"

        line = listToString(temp_list)

    # if
    if _line[:4] == "eğer":
        temp_list = list(_line)
        temp_list[:4] = "if"
        temp_list.append(":")

        line = listToString(temp_list)
        line = line.replace(" ve ", " and ")
        line = line.replace(" veya ", " or ")

    # else
    if _line[:7] == "değilse":
        temp_list = list(_line)
        temp_list[:7] = "else"
        temp_list.append(":")

        line = listToString(temp_list)

    # elif
    if _line[:10] == "değilse ve":
        temp_list = list(_line)
        temp_list[:10] = "elif"
        temp_list.append(":")

        line = listToString(temp_list)
        line = line.replace(" ve ", " and ")
        line = line.replace(" veya ", " or ")

    # for
    if "içindeki herbir" in _line and "için" in _line:
        temp_list = _line.split()
        if (temp_list.index("içindeki") == 1) and (temp_list.index("herbir") == 2) and (temp_list.index("için") == 4):
            temp_list.remove("içindeki")
            temp_list.remove("herbir")
            temp_list.remove("için")

        line = "for " + str(temp_list[1]) + " in " + str(temp_list[0]) + ":"

    # def
    if _line[:9] == "fonksiyon":
        temp_list = list(_line)
        temp_list[:9] = "def"

        line = listToString(temp_list)

    # #
    if _line[:2] == "//":
        temp_list = list(_line)
        temp_list[:2] = "#"

        line = listToString(temp_list)

    # "    "
    if _line[:1] == "?":
        temp_list = list(_line)
        temp_list[:1] = ""
        temp_line = listToString(temp_list)
        line = "?" + EvalLine(temp_line)

    # ** 2
    line = line.replace("kare(", "libs.karesi(")

    # ** 3
    line = line.replace("küp(", "libs.kupu(")

    # ** 1/2
    line = line.replace("karekök(", "libs.karekok(")

    # ** 1/3
    line = line.replace("küpkök(", "libs.kupkok(")

    # abs
    line = line.replace("mutlak(", "libs.mutlak(")

    # time.sleep ()
    if _line[:5] == "bekle":
        temp_list = list(_line)
        temp_list[:5] = "libs.bekle"

        line = listToString(temp_list)

    return ArrangeTabs(line.strip())


def Compile(_filename: str, _run: bool):
    global extension

    os.system("cls")

    outputLines = []

    # TODO create a pip package
    outputLines.append("from src import libs")

    filename_output = _filename.replace(extension, ".py").strip()

    inputFile = open(_filename, "r", encoding="utf-8")
    inputLines = [x.rstrip("\n") for x in inputFile.readlines()]

    for _il in inputLines:
        newLine = ""
        newLine = EvalLine(_il)
        # delete ( and newLine != "") if you want an exact translation
        if newLine != None and newLine != "":
            outputLines.append(newLine)

    outputFile = open(filename_output, "w+", encoding="utf-8")
    for line in outputLines:
        outputFile.write(str(line) + "\n")

    outputFile.close()
    inputFile.close()

    if _run == True:
        os.system("python " + filename_output)
        os.remove(filename_output)


if __name__ == "__main__":
    # compile()
    filename_raw = sys.argv[1:][0]
    dont_run = not (False if len(
        sys.argv) <= 2 else True if sys.argv[1:][1] == "çalıştırma" else False)
    filename = filename_raw.replace(".\\", "")
    Compile(filename, dont_run)
