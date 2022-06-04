import sys

sys.path.append("..")

from mdx import Document

md = open("test.md", "r").read()


def run():
    doc = Document(md)
    doc.title = "Programming Constructs"
    doc.subtitle = "Unit 14 Assignment 1"
    doc.save("test.docx")


if __name__ == "__main__":
    print("Running test")
    run()
    print("Completed test")
