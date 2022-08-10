import sys

sys.path.append("..")

from mdx import Document, Style


def constructs():
    # In Python
    md = open("constructs.md", "r").read()
    doc = Document(md)
    doc.save("constructs.docx")

    # In Python (foxtrot)
    doc = Document(md, Style.foxtrot())
    doc.save("constructs_foxtrot.docx")

    # Command-line
    # TODO: test command-line


def airbnb():
    # In Python
    md = open("airbnb.md", "r").read()
    doc = Document(md)
    doc.save("airbnb.docx")

    # In Python (foxtrot)
    doc = Document(md, Style.foxtrot())
    doc.save("airbnb_foxtrot.docx")

    # Command-line
    # TODO: test command-line


if __name__ == "__main__":
    print("Running tests")
    constructs()
    airbnb()
    print("Completed tests")
