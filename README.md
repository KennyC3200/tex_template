# LaTex Template

# TODO
- Option (0) to create new project
- Better tables?
- `production` and `remote` branches? The production branch will include the `/tests` folder. The tests will include:
    - Driving academy glossary terms
- [Shell Scripts](https://helpful.wiki/zsh/)
    1. Creates a new `unit_##` folder
        - Add: Python script that appends the new unit to the end of `main.tex`
    2. Creates a new `lesson_##.tex` file in the `unit_##` folder
        - Add: Python script that appends the new lesson to the end of the `unit_##.tex` in the `unit_##` folder
    3. `nvim` into the current `unit_##/lesson_##.tex`
- CLI in Python that parses a select `lesson_##.tex` and shuffles the questions. Consider two scenarios:
    1. Multiple choice: generate the choices (A), (B), (C), ...
    2. Response: generate the answer once the user has input
    - Add:
    - Issue: how are we going to parse the LaTex? Might be better to use a JS thing then
