import os
import re


def file_str_replace(path, str_replacements):
    with open(path, "r") as file:
        lines = file.read().rstrip()
        for str_replacement in str_replacements:
            _lines = lines.split(str_replacement["str"])
            if len(_lines) == 2:
                lines = "".join([_lines[0], str_replacement["replacement"], _lines[1]])
            elif len(_lines) == 1:
                lines = "".join([lines[0], str_replacement["replacement"]])

    return lines


def new_template(name):
    str_replacements = [
        {"str": "\\title{Template}", "replacement": "\\title{" + name + "}"}
    ]
    lines = file_str_replace("./src/main/main.tex", str_replacements)
    with open("./src/main/main.tex", "w") as file:
        file.write(lines)


def set_unit(number):
    name = "unit_" + (str(number) if number > 10 else "0" + str(number))
    dir = "./src/" + name + "/"
    return {
        "name": name,
        "directory": dir,
        "path": dir + name + ".tex",
        "number": number
    }


def current_unit():
    dirs = [x[0] for x in os.walk("./src")]
    unit = 0

    for dir in dirs:
        if "unit_" in dir:
            if (x := int(dir.split("unit_")[1])) > unit:
                unit = x

    return set_unit(unit)


def preprocess_unit(number, name):
    path = "./src/.unit/.unit.tex"
    str_replacements = [
        {"str": "{../.unit\\}", "replacement": "{../unit\\_" + (str(number) if number > 10 else "0" + str(number)) + "}"},
        {"str": "\\title{Unit 0}", "replacement": "\\title{" + name + "}"}
    ]
    lines = file_str_replace(path, str_replacements)

    return lines


def new_unit(name):
    unit = set_unit(current_unit()["number"] + 1)
    os.mkdir(unit["directory"])

    # create new lesson_##.tex file
    with open(unit["path"], "a") as file:
        lines = preprocess_unit(unit["number"], name)
        file.write(lines)
        open(unit["directory"] + unit["name"] + ".tex.latexmain", "a")
    new_lesson(input("Lesson Name: "))

    # append \unit{unit_name_here} to main.tex
    str_replacements = [
        {"str": "\\end{document}", "replacement": "\\unit{" + name + "}\n\\end{document}"}
    ]
    lines = file_str_replace("./src/main/main.tex", str_replacements)
    with open("./src/main/main.tex", "w") as file:
        file.write(lines)


def set_lesson(unit, number, lesson_name):
    # lol, so in set_unit the name doesn't have .tex but in this one it does
    # wtf is my code man
    name = "lesson_" + (str(number) if number > 10 else "0" + str(number)) + ".tex"
    return {
        "directory": unit["directory"],
        "path": unit["directory"] + name,
        "name": name,
        "number": int(number),
        "lesson_name": lesson_name
    }


def current_lesson(unit, lesson_name):
    dir = unit["directory"]
    files = [x for x in os.listdir(dir) if os.path.isfile(dir + x)]
    lesson = 0
    for file in files:
        match = re.search(r"\d+", file)
        if "lesson_" in file and match and int(match.group()) > lesson:
            lesson = int(match.group())

    return set_lesson(unit, int(lesson), lesson_name)


def preprocess_lesson(unit, lesson):
    # append the lesson_##.tex to the end of unit_##.tex
    path = unit["path"]
    str_replacements = [
        {"str": "\\end{document}", "replacement": "\\include{\\UnitPath/" + lesson["name"] + "}\n\\end{document}"}
    ]
    lines = file_str_replace(unit["path"], str_replacements)
    with open(path, "w") as file:
        file.write(lines)

    # use the .unit/lesson.tex as template
    path = "./src/.unit/lesson.tex"
    str_replacements = [
        {"str": "lesson\\", "replacement": lesson["lesson_name"]}
    ]
    lines = file_str_replace(path, str_replacements)

    return lines


def new_lesson(name):
    unit = current_unit()
    lesson = current_lesson(unit, name)
    lesson = set_lesson(unit, lesson["number"] + 1, name)

    # create lesson_##.tex file
    with open(lesson["path"], "w") as file:
        lines = preprocess_lesson(unit, lesson)
        file.write(lines)

    # append \input{../unit_##/lesson_##.tex} to main.tex
    str_replacements = [
        {"str": "\\end{document}", "replacement": "\\input{../" + unit["name"] + "/" + lesson["name"] + "}\n\\end{document}"}
    ]
    lines = file_str_replace("./src/main/main.tex", str_replacements)
    with open("./src/main/main.tex", "w") as file:
        file.write(lines)


command = input("""Commands
(n) New Template
(0) New Unit
(1) New Lesson
""")

if command == "n":
    new_template(input("Template Name: "))
    new_unit(input("Unit Name: "))
elif command == "0":
    new_unit(input("Unit Name: "))
elif command == "1":
    new_lesson(input("Lesson Name: "))
