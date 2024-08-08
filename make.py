import os
import re


class FileData:
    def __init__(self, path):
        self.path = path
        self.dir = os.path.dirname(path) + "/"
        self.full_filename = os.path.basename(path)
        self.filename, self.extension = os.path.splitext(self.full_filename)

    def print(self, label=""):
        print(f"{label}\n"
              f"         path: {self.path}\n"
              f"          dir: {self.dir}\n"
              f"full_filename: {self.full_filename}\n"
              f"     filename: {self.filename}\n"
              f"    extension: {self.extension}\n")


class Unit:
    template_file_data = FileData("./src/.unit/unit.tex")

    def __init__(self, number):
        self.number = number
        self.number_str = str(number) if number >= 10 else "0" + str(number)
        self.file_data = FileData(
            f"./src/unit_{self.number_str}/"
            f"unit_{self.number_str}.tex"
        )

    @staticmethod
    def new(name):
        unit = Unit(Unit.current().number + 1)

        os.mkdir(unit.file_data.dir)
        with open(Unit.template_file_data.path, "r") as template_file, \
             open(unit.file_data.path, "a") as file:
            file_text = template_file.read().rstrip()
            token_replacements = [
                ["../unit", f"../unit\\_{unit.number_str}"],
                ["\\title{Unit}", f"\\title{{{name}}}"]
            ]
            for token, replacement in token_replacements:
                file_text = file_text.replace(token, replacement)
            file.write(file_text)

    @staticmethod
    def current():
        dirs = [x[0] for x in os.walk("./src/")]
        unit = 0

        for dir in dirs:
            if "unit_" in dir:
                if (x := int(dir.split("unit_")[1])) > unit:
                    unit = x

        return Unit(unit)


class Lesson:
    template_file_data = FileData("./src/.unit/lesson.tex")

    def __init__(self, number):
        self.number = number

        number_str = str(number) if number >= 10 else "0" + str(number)
        self.file_data = FileData(
            f"./src/unit/unit_{number_str}/"
            f"lesson_{number_str}.tex"
        )

    @staticmethod
    def new():
        Lesson.template_file_data.print("Lesson Template")

    @staticmethod
    def current():
        pass


def main():
    command = input("Commands\n"
                    "(n) New Template\n"
                    "(0) New Unit\n"
                    "(1) New Lesson\n")

    if command == "n":
        pass
    elif command == "0":
        name = input("Unit Name: ")
        Unit.new(name)
    elif command == "1":
        Lesson.new()


if __name__ == "__main__":
    main()
