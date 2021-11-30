import os
import sys
import re

extension = ".kr"


def EvalLine(InputLine: str):
    FinalLine = re.sub("    ", "/tab/", InputLine)

    # print
    print_matches = re.findall('yazdır\("*.*"*\)', str(FinalLine))
    if len(print_matches) > 0:
        # print_matches[0].replace("yazdır", "print")
        FinalLine = re.sub("yazdır\(", "print(", str(FinalLine))

    # variable decleration
    var_matches = re.findall('değişken .* = .*', str(FinalLine))
    if len(var_matches) == 0:
        var_matches2 = re.findall('değişken .*', str(FinalLine))
        if len(var_matches2) > 0:
            FinalLine = re.sub("değişken ", "", str(FinalLine)) + " = None"
    else:
        FinalLine = str(re.sub("değişken ", "", str(FinalLine)))

    # if
    if_matches = re.findall('eğer .*', FinalLine)
    if len(if_matches) > 0:
        FinalLine = re.sub("eğer ", "if ", str(FinalLine), 1) + ":"

    # elif
    elif_matches = re.findall('değilse ve .*', str(FinalLine))
    if len(elif_matches) > 0:
        FinalLine = re.sub("değilse ve ", "elif ", str(FinalLine), 1) + ":"

    # else
    else_matches = re.findall('değilse ?', str(FinalLine))
    if len(else_matches) > 0:
        FinalLine = re.sub("değilse ?", "else", str(FinalLine)) + ":"

    # def fonksiyon
    def_matches = re.findall('fonksiyon .*\(.*\)', str(FinalLine))
    if len(def_matches) > 0:
        FinalLine = re.sub("fonksiyon ", "def ", str(FinalLine)) + ":"
    else:
        def_matches2 = re.findall('f .*\(.*\)', str(FinalLine))
        if len(def_matches2) > 0:
            FinalLine = re.sub("f ", "def ", str(FinalLine), 1) + ":"

    # for
    for_matches = re.findall('.* içindeki herbir .* için', FinalLine)
    if len(for_matches) > 0:
        for_tab_count = len(re.findall('\/tab\/', FinalLine))
        FinalLine = re.sub("\/tab\/", "", FinalLine)
        FinalLine = re.sub(" içindeki herbir", "", FinalLine, 1)
        FinalLine = re.sub(" için", "", FinalLine, 1)
        FinalLine = re.split('\s+', FinalLine)
        FinalLine = for_tab_count * "/tab/" + "for " + \
            FinalLine[1] + " in " + FinalLine[0] + ":"

    # while
    while_matches = re.findall('.* olduğu sürece', str(FinalLine))
    if len(while_matches) > 0:
        while_tab_count = len(re.findall('\/tab\/', str(FinalLine)))
        FinalLine = re.sub("\/tab\/", "", str(FinalLine))
        FinalLine = while_tab_count * "/tab/" + "while " + \
            re.sub(" olduğu sürece", "", str(FinalLine), 1) + ":"

    # return
    return_matches = re.findall('\\bdöndür ?.*\\b', str(FinalLine))
    if len(return_matches) > 0:
        FinalLine = re.sub("döndür", "return", str(FinalLine), 1)

    # ^2
    square_matches = re.findall('kare\(.*?\)', str(FinalLine))
    if len(square_matches) > 0:
        FinalLine = re.sub("kare\(", "mithen.kare(", str(FinalLine))

    # ^3
    cube_matches = re.findall('küp\(.*?\)', str(FinalLine))
    if len(cube_matches) > 0:
        FinalLine = re.sub("küp\(", "mithen.kup(", str(FinalLine))

    # ^1/2
    squareroot_matches = re.findall('karekök\(.*?\)', str(FinalLine))
    if len(squareroot_matches) > 0:
        FinalLine = re.sub("karekök\(", "mithen.karekok(", str(FinalLine))

    # ^1/3
    cuberoot_matches = re.findall('küpkök\(.*?\)', str(FinalLine))
    if len(cuberoot_matches) > 0:
        FinalLine = re.sub("küpkök\(", "mithen.kupkok(", str(FinalLine))

    # absolute
    abs_matches = re.findall('mutlak\(.*?\)', str(FinalLine))
    if len(abs_matches) > 0:
        FinalLine = re.sub("mutlak\(", "mithen.mutlak(", str(FinalLine))

    # time.sleep()
    timesleep_matches = re.findall('bekle\(.*?\)', str(FinalLine))
    if len(timesleep_matches) > 0:
        FinalLine = re.sub("bekle\(", "mithen.bekle(", str(FinalLine))

    # class
    class_matches = re.findall('sınıf .*', str(FinalLine))
    if len(class_matches) > 0:
        _line = re.sub("sınıf ", "class ", str(FinalLine)) + ":"
        FinalLine = ["@dataclass", _line]

    # input()
    input_matches = re.findall('girdi\("?.*"?\)', str(FinalLine))
    if len(input_matches) > 0:
        FinalLine = re.sub("girdi\(", "input(", str(FinalLine))

    # break
    break_matches = re.findall("\\bkır\\b", str(FinalLine))
    if len(break_matches) > 0:
        FinalLine = re.sub("kır", "break", str(FinalLine), 1)

    # list
    list_matches = re.findall("liste\(.?\)", str(FinalLine))
    if len(list_matches) > 0:
        FinalLine = re.sub("liste\(", "list(", str(FinalLine))

    # str
    str_matches = re.findall("karakter\(.?\)", str(FinalLine))
    if len(str_matches) > 0:
        FinalLine = re.sub("karakter\(", "str(", str(FinalLine))

    # Final return
    if isinstance(FinalLine, str):
        FinalLine = re.sub("\/tab\/", "    ", str(FinalLine))
    elif isinstance(FinalLine, list):
        for i in FinalLine:
            FinalLine[FinalLine.index(i)] = re.sub("\/tab\/", "    ", i)
    return FinalLine


def Compile(_filename: str, _run: bool):
    global extension

    outputLines = []

    outputLines.append("from mithen import mithen")
    outputLines.append("from dataclasses import dataclass")

    filename_output = _filename.replace(extension, ".py").strip()

    inputFile = open(_filename, "r", encoding="utf-8")
    inputLines = [x.rstrip("\n") for x in inputFile.readlines()]

    for _il in inputLines:
        # because of the dynamic declaring any python code will be valid in krypton.
        # ? another aproach for the defs would be adding them to a global list then interpreting them.
        #_el = EvalLine(_il)
        #newLine = _el if _el != "" else _il
        # delete ( and newLine != "") if you want an exact translation in terms of spaces and line breaks.
        # if newLine != None and newLine != "":
        _newLine = EvalLine(_il)
        if isinstance(_newLine, str):
            outputLines.append(_newLine)
        elif isinstance(_newLine, list):
            for _i in _newLine:
                outputLines.append(_i)
    #outputLines.append('input("Devam etmek için bir tuşa basınız. ")')
    outputFile = open(filename_output, "w+", encoding="utf-8")
    for line in outputLines:
        outputFile.write(str(line) + "\n")

    outputFile.close()
    inputFile.close()

    if _run == True:
        os.system("cls")
        os.system("python3 " + filename_output)
        os.remove(filename_output)


if __name__ == "__main__":
    # compile()
    if len(sys.argv) > 1:
        filename_raw = sys.argv[1:][0]
        dont_run = not (False if len(
            sys.argv) <= 2 else True if sys.argv[1:][1] == "çalıştırma" else False)
        filename = filename_raw.replace(".\\", "")
    else:
        filename = input("Dosya ismi giriniz: ")
        dont_run = False
    Compile(filename, dont_run)
