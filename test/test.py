import sys

sys.path.append("..")

from mdx import Document, Style


def constructs():
    # In Python
    md = open("constructs.md", "r").read()
    doc = Document(md)
    doc.save("constructs.docx")

    # In Python (andy)
    doc = Document(md, Style.andy())
    doc.save("constructs_andy.docx")

    # Command-line
    # TODO: test command-line


def airbnb():
    # In Python
    md = open("airbnb.md", "r").read()
    doc = Document(md)
    doc.save("airbnb.docx")

    # In Python (andy)
    doc = Document(md, Style.andy())
    doc.save("airbnb_andy.docx")

    # Command-line
    # TODO: test command-line


if __name__ == "__main__":
    print("Running tests")
    constructs()
    airbnb()
    print("Completed tests")
