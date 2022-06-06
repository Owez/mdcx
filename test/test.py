import sys

sys.path.append("..")

from mdx import Document


def run():
    # In Python
    md = open("test.md", "r").read()
    doc = Document(md)
    doc.save("test.docx")

    # In Python (andy)
    doc.andy = True
    doc.save("test_andy.docx")

    # Command-line
    # TODO: test command-line


if __name__ == "__main__":
    print("Running test")
    run()
    print("Completed test")
