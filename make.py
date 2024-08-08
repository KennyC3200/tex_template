import os
import re


class FileData:
    def __init__(self, path):
        self.path = path
        self.dir = os.path.dirname(path)
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

        number_str = str(number) if number >= 10 else "0" + str(number)
        self.file_data = FileData(
            f"./src/unit/unit_{number_str}/"
            f"unit_{number_str}.tex"
        )

    def new(self):
        pass

    def current(self):
        pass


class Lesson:
    template_file_data = FileData("./src/.unit/lesson.tex")

    def __init__(self, number):
        self.number = number

        number_str = str(number) if number >= 10 else "0" + str(number)
        self.file_data = FileData(
            f"./src/unit/unit_{number_str}/"
            f"lesson_{number_str}.tex"
        )

    def new(self):
        pass

    def current(self):
        pass


unit_template = FileData("./src/.unit/unit.tex")
lesson_template = FileData("./src/.unit/lesson.tex")

unit_template.print("unit_template")
lesson_template.print("lesson_template")
