import os
import re


class FileData:
    def __init__(self, path):
        self.path = path
        self.dir = os.path.dirname(path) + "/"
        self.full_filename = os.path.basename(path)
        self.filename, self.extension = os.path.splitext(self.full_filename)

    def __str__(self, label=""):
        return (f"{label}\n"
                f"         path: {self.path}\n"
                f"          dir: {self.dir}\n"
                f"full_filename: {self.full_filename}\n"
                f"     filename: {self.filename}\n"
                f"    extension: {self.extension}\n")


class FileHelper:
    @staticmethod
    def find_and_replace(file_path, token_replacements):
        with open(file_path, "r") as file:
            file_text = file.read().rstrip()
            for token, replacement in token_replacements:
                file_text = file_text.replace(token, replacement)

        return file_text


class Template:
    @staticmethod
    def new(name):
        pass


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

        # create new unit_## directory and unit_##.tex file
        os.mkdir(unit.file_data.dir)
        with open(unit.file_data.path, "a") as file:
            token_replacements = [
                ["../unit", f"../unit\\_{unit.number_str}"],
                ["\\title{Unit}", f"\\title{{{name}}}"]
            ]
            file_text = FileHelper.find_and_replace(
                Unit.template_file_data.path,
                token_replacements)
            file.write(file_text)

        # append to template.tex file
        token_replacements = [["\\end{document}", f"\\unit{{{name}}}\n\\end{{document}}"]]
        file_text = FileHelper.find_and_replace(
            "./src/template/template.tex",
            token_replacements)
        with open("./src/template/template.tex", "w") as file:
            file.write(file_text)

    @staticmethod
    def current():
        dirs = [x[0] for x in os.walk("./src/")]
        unit_number = 0

        for dir in dirs:
            match = re.search(r"\d+", dir)
            if "unit_" in dir \
                    and match and (x := int(match.group())) > unit_number:
                unit_number = x

        return Unit(unit_number)


class Lesson:
    template_file_data = FileData("./src/.unit/lesson.tex")

    def __init__(self, unit, number):
        self.number = number
        self.number_str = str(number) if number >= 10 else "0" + str(number)
        self.file_data = FileData(
            unit.file_data.dir +
            f"lesson_{self.number_str}.tex")

    @staticmethod
    def new(unit_number, name):
        unit = Unit(unit_number)
        lesson = Lesson(unit, Lesson.current(unit).number + 1)

        # create new lesson_##.tex file
        with open(lesson.file_data.path, "a") as file:
            token_replacements = [["Lesson", name]]
            file_text = FileHelper.find_and_replace(
                Lesson.template_file_data.path,
                token_replacements)
            file.write(file_text)

        # append to unit_##.tex file
        token_replacements = [["\\end{document}", f"\\input{{\\UnitDir/{lesson.file_data.full_filename}}}\n\\end{{document}}"]]
        file_text = FileHelper.find_and_replace(
            unit.file_data.path,
            token_replacements)
        with open(unit.file_data.path, "w") as file:
            file.write(file_text)

        # append to template.tex file
        token_replacements = [["\\end{document}", f"\\input{{../{unit.file_data.filename}/{lesson.file_data.full_filename}}}\n\\end{{document}}"]]
        file_text = FileHelper.find_and_replace(
            "./src/template/template.tex",
            token_replacements)
        with open("./src/template/template.tex", "w") as file:
            file.write(file_text)

    @staticmethod
    def current(unit):
        dir = unit.file_data.dir
        files = [x for x in os.listdir(dir) if os.path.isfile(dir + x)]
        lesson_number = 0

        for file in files:
            match = re.search(r"\d+", file)
            if "lesson_" in file \
                    and match and (x := int(match.group())) > lesson_number:
                lesson_number = x

        return Lesson(unit, lesson_number)


def main():
    command = input("Commands\n"
                    "(n) New Template\n"
                    "(0) New Unit\n"
                    "(1) New Lesson\n"
                    "(2) New Lesson in Unit\n")

    if command == "n":
        pass
    elif command == "0":
        name = input("Unit Name: ")
        Unit.new(name)
        lesson_name = input("Lesson Name: ")
        Lesson.new(Unit.current().number, lesson_name)
    elif command == "1":
        unit_number = Unit.current().number
        name = input("Lesson Name: ")
        Lesson.new(unit_number, name)
    elif command == "2":
        unit_number = int(input("Unit Number: "))
        name = input("Lesson Name: ")
        Lesson.new(unit_number, name)


if __name__ == "__main__":
    main()
