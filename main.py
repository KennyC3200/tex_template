import os
import re


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
    with open("./src/unit_00/unit_00.tex") as template:
        lines = template.read().rstrip()
        for buffer in [
            {"regex": "{../unit\\_00}", "replacement": "{../unit\\_" + (str(number) if number > 10 else "0" + str(number)) + "}"},
            {"regex": "\\title{Unit 0}", "replacement": "\\title{" + name + "}"}
        ]:
            _lines = lines.split(buffer["regex"])
            lines = "".join([_lines[0], buffer["replacement"], _lines[1]])

    return lines


def new_unit(name):
    unit = set_unit(current_unit()["number"] + 1)
    os.mkdir(unit["directory"])

    with open(unit["path"], "a") as file:
        lines = preprocess_unit(unit["number"], name)
        file.write(lines)
        open(unit["directory"] + unit["name"] + ".tex.latexmain", "a")
    new_lesson(input("Lesson Name: "))


def set_lesson(unit, number):
    name = "lesson_" + (str(number) if number > 10 else "0" + str(number)) + ".tex"
    return {
        "directory": unit["directory"],
        "path": unit["directory"] + name,
        "name": name,
        "number": int(number)
    }


def current_lesson(unit):
    dir = unit["directory"]
    files = [x for x in os.listdir(dir) if os.path.isfile(dir + x)]
    lesson = 0
    for file in files:
        match = re.search(r"\d+", file)
        if "lesson_" in file and match and int(match.group) > lesson:
            lesson = int(match.group)

    return set_lesson(unit, int(lesson))


def preprocess_lesson(unit, name):
    # write \input{\UnitPath/lesson_01.tex} in unit_01.tex
    with open(unit["path"], "r") as file:
        pass

    with open("./src/unit_00/lesson_01.tex", "a") as template:
        lines = template.read().rstrip()
        for buffer in [
            {"regex": "lesson\\_01", "replacement": name}
        ]:
            _lines = lines.split(buffer["regex"])
            lines = "".join([_lines[0], buffer["replacement"], _lines[1]])

    return lines


def new_lesson(name):
    unit = current_unit()
    lesson = current_lesson(unit)
    if lesson["number"] == 0:
        lesson = set_lesson(unit, lesson["number"] + 1)

    with open(lesson["path"], "w") as file:
        lines = preprocess_lesson(name)
        file.write(lines)


command = int(input("""Commands
(0) New Unit
(1) New Lesson
"""))

if command == 0:
    new_unit(input("Unit Name: "))
elif command == 1:
    new_lesson(input("Lesson Name: "))
