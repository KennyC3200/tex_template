import os


def current_unit():
    dirs = [x[0] for x in os.walk("./src")]

    unit = ""
    _unit = 0
    for dir in dirs:
        if "unit_" in dir:
            if (x := int(dir.split("unit_")[1])) > _unit:
                _unit = x
    return {
        "name": unit,
        "path": "unit_" + (str(_unit) if _unit > 10 else "0" + str(_unit)),
        "number": _unit
    }


def preprocess_unit(number, name):
    with open("./src/unit_00/unit_00.tex") as template:
        lines = template.read().rstrip()
        for buffer in [
            {"regex": "newcommand*{\\UnitPath}{../unit\\_00}", "replacement": "../unit_" + (str(number) if number > 10 else "0" + str(number))},
            {"regex": "\\title{Unit 0}", "replacement": "\\title{" + name + "}"}
        ]:
            _lines = lines.split(buffer["regex"])
            lines = "".join([_lines[0], buffer["replacement"], _lines[1]])

    return lines


def new_unit(name):
    unit = current_unit()["number"] + 1
    lines = preprocess_unit(unit, name)
    print(lines)


def new_lesson():
    unit = current_unit()["number"] + 1
    print(unit)


command = int(input("""Commands
(0) New Unit
(1) New Lesson
"""))

if command == 0:
    new_unit(input("Name: "))
elif command == 1:
    new_lesson()
