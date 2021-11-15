import os
import sys
import re

extension = ".kr"


def EvalLine(InputLine: str):
    FinalLine = re.sub("    ", "/tab/", InputLine)

    # print
    print_matches = re.findall('yazdır\("*.*"*\)', FinalLine)
    if len(print_matches) > 0:
        # print_matches[0].replace("yazdır", "print")
        FinalLine = re.sub("yazdır\(", "print(", FinalLine)

    # variable decleration
    var_matches = re.findall('değişken .* = .*', FinalLine)
    if len(var_matches) == 0:
        var_matches2 = re.findall('değişken .*', FinalLine)
        if len(var_matches2) > 0:
            FinalLine = re.sub("değişken ", "", FinalLine) + " = None"
    else:
        FinalLine = str(re.sub("değişken ", "", FinalLine))

    # if
    if_matches = re.findall('eğer .*', FinalLine)
    if len(if_matches) > 0:
        FinalLine = re.sub("eğer ", "if ", FinalLine, 1) + ":"

    # elif
    elif_matches = re.findall('değilse ve .*', FinalLine)
    if len(elif_matches) > 0:
        FinalLine = re.sub("değilse ve ", "elif ", FinalLine, 1) + ":"

    # else
    else_matches = re.findall('değilse ?', FinalLine)
    if len(else_matches) > 0:
        FinalLine = re.sub("değilse ?", "else", FinalLine) + ":"

    # def fonksiyon
    def_matches = re.findall('fonksiyon .*\(.*\)', FinalLine)
    if len(def_matches) > 0:
        FinalLine = re.sub("fonksiyon ", "def ", FinalLine) + ":"
    else:
        def_matches2 = re.findall('f .*\(.*\)', FinalLine)
        if len(def_matches2) > 0:
            FinalLine = re.sub("f ", "def ", FinalLine, 1) + ":"

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
    while_matches = re.findall('.* olduğu sürece', FinalLine)
    if len(while_matches) > 0:
        while_tab_count = len(re.findall('\/tab\/', FinalLine))
        FinalLine = re.sub("\/tab\/", "", FinalLine)
        FinalLine = while_tab_count * "/tab/" + "while " + \
            re.sub(" olduğu sürece", "", FinalLine, 1) + ":"

    # return
    return_matches = re.findall('döndür .*', FinalLine)
    if len(return_matches) > 0:
        FinalLine = re.sub("döndür ", "return ", FinalLine, 1)

    # ^2
    square_matches = re.findall('kare\(.*?\)', FinalLine)
    if len(square_matches) > 0:
        FinalLine = re.sub("kare\(", "mithen.kare(", FinalLine)

    # ^3
    cube_matches = re.findall('küp\(.*?\)', FinalLine)
    if len(cube_matches) > 0:
        FinalLine = re.sub("küp\(", "mithen.kup(", FinalLine)

    # ^1/2
    squareroot_matches = re.findall('karekök\(.*?\)', FinalLine)
    if len(squareroot_matches) > 0:
        FinalLine = re.sub("karekök\(", "mithen.karekok(", FinalLine)

    # ^1/3
    cuberoot_matches = re.findall('küpkök\(.*?\)', FinalLine)
    if len(cuberoot_matches) > 0:
        FinalLine = re.sub("küpkök\(", "mithen.kupkok(", FinalLine)

    # absolute
    abs_matches = re.findall('mutlak\(.*?\)', FinalLine)
    if len(abs_matches) > 0:
        FinalLine = re.sub("mutlak\(", "mithen.mutlak(", FinalLine)

    # time.sleep()
    timesleep_matches = re.findall('bekle\(.*?\)', FinalLine)
    if len(timesleep_matches) > 0:
        FinalLine = re.sub("bekle\(", "mithen.bekle(", FinalLine)

    # Final return
    FinalLine = re.sub("\/tab\/", "    ", FinalLine)
    return FinalLine


def Compile(_filename: str, _run: bool):
    global extension

    outputLines = []

    outputLines.append("from mithen import mithen")

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
        outputLines.append(EvalLine(_il))

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
