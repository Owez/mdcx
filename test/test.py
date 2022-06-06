import sys

sys.path.append("..")

from mdx import Document

md = open("test.md", "r").read()


def run():
    Document(md).save("test.docx")

    # TODO: test command-line


if __name__ == "__main__":
    print("Running test")
    run()
    print("Completed test")
