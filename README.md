# LaTex Template
This is a template used for LaTeX note taking. Run `Python3 make.py` to get started.

# TODO
- **Creating a new lesson in a unit doesn't work in the template.tex** because it inserts at the
  end of the file
- **Decorate the samples**
- **Rewrite in RUST?**
- Using arrow keys to navigate the CLI
- CLI in Python that parses a select `lesson_##.tex` and shuffles the questions. Consider two scenarios:
    1. Multiple choice: generate the choices (A), (B), (C), ...
    2. Response: generate the answer once the user has input
    - Add:
    - Issue: how are we going to parse the LaTex? Might be better to use a JS thing then
