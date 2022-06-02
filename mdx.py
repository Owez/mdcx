from pathlib import Path
from pydoc import doc
import docx
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_BREAK
from docx.shared import RGBColor, Pt, Inches

STYLE_CODE = "Code"


class Heading:
    """Heading section inside document"""

    def __init__(self, text: str, level: int) -> None:
        self.text = text
        self.level = level

    def _md(line: str):
        # Parse number of # for level
        level = 0
        while line[level] == "#":
            level += 1
        # Get and clean text
        text = line[level:].lstrip()
        return Heading(text, level)

    def _docx(self, docx_doc: docx.Document):
        docx_doc.add_heading(self.text, self.level)


class Run:
    """Run of text with styling located inside a paragraph"""

    def __init__(
        self,
        text: str,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
    ):
        self.text = text
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strikethrough = strikethrough

    def _docx(self, docx_para: docx.text.paragraph.Paragraph) -> docx.text.run.Run:
        # Add plain run text
        docx_run = docx_para.add_run(self.text)
        # Add relevant styles
        if self.bold:
            docx_run.bold = True
        if self.italic:
            docx_run.italic = True
        if self.underline:
            docx_run.underline = True
        if self.strikethrough:
            docx_run.strikethrough = True
        return docx_run


class Paragraph:
    """Paragraph consisting of many runs of text"""

    def __init__(self, runs: list = []):
        self.runs = runs

    def append(self, run: Run):
        """Appends new run to paragraph"""
        self.runs.append(run)

    @staticmethod
    def _md(line: str):
        # Make new paragraph
        para = Paragraph([])
        # Parse through runs
        para.append(Run(line))  # TODO: actually parse runs
        return para

    def _docx(self, docx_doc: docx.Document) -> docx.text.paragraph.Paragraph:
        # Add empty paragraph
        docx_para = docx_doc.add_paragraph()
        # Add runs to paragraph
        for run in self.runs:
            run._docx(docx_para)
        return docx_para


class Codeblock:
    """Codeblock containing language and monospaced code"""

    def __init__(
        self, lines: list, lang: str = None
    ):  # TODO: use `lang` somewhere in docx
        self.lines = lines
        self.lang = lang

    @staticmethod
    def _md(lines: list) -> tuple:
        # Get language after ``` designator
        lang = (
            lines[0].lstrip()[3:].lstrip()
        )  # first `lstrip()` used in document parsing
        lang = lang if lang != "" else None

        # Read lines
        code = []
        for line in lines[1:]:
            if line.lstrip() == "```":
                break
            else:
                code.append(line)

        # Get skip
        skip = len(code) + 1
        return (Codeblock(code, lang), skip)

    def _docx(self, docx_doc: docx.Document):
        # Add lines
        for line in self.lines:
            # Hijack paragraph
            para = Paragraph()
            # Add big single run for line
            para.append(Run(line))
            # Submit to docx
            docx_para = para._docx(docx_doc)
            # Change style of submitted
            docx_para.style = STYLE_CODE


class Document:
    """High-level document abstractions for conversion"""

    elements = []
    title = None
    subtitle = None

    def __init__(self, md: str):
        # Get and clear up lines
        lines_raw = md.splitlines()
        lines = []
        for line in lines_raw:
            # Strip anything from the rights
            line = line.rstrip()
            # Append only non-empty lines
            if line != "":
                lines.append(line)

        # Parse through lines
        ind = 0
        while ind < len(lines):
            # Get line
            line = lines[ind]
            stripped = line.lstrip()
            # Check start
            if stripped.startswith("#"):
                # Heading
                self.elements.append(Heading._md(stripped))
            elif stripped.startswith("```"):
                # Codeblock
                codeblock, skip = Codeblock._md(lines[ind:])
                ind += skip
                self.elements.append(codeblock)
            else:
                # Paragraph
                self.elements.append(Paragraph._md(stripped))

            # TODO: bullet point, make sure to pipe in stock `line` after detection
            # TODO: numbered point, make sure to pipe in stock `line` after detection
            # TODO: image

            # Move to next line
            ind += 1

    def save(self, path: Path):
        """Saves document to `path` provided"""
        # Create docx file
        docx_doc = docx.Document()

        # Fonts
        FONT_HEADING = "Helvetica"
        FONT_BODY = "Helvetica"
        FONT_CODE = "IBM Plex Mono"

        # Styling for headings
        for h in range(1, 9):
            style_heading = docx_doc.styles[f"Heading {h}"]
            style_heading.font.name = FONT_HEADING
            style_heading.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

            if h == 1:
                style_heading.font.size = Pt(22)
                style_heading.paragraph_format.space_after = Pt(2)
            elif h == 2:
                style_heading.font.size = Pt(17)
            elif h == 3:
                style_heading.font.size = Pt(13)

        # Styling for paragraphs
        style_paragraph = docx_doc.styles["Normal"]
        style_paragraph.font.name = FONT_BODY
        style_paragraph.font.size = Pt(12)

        # Styling for codeblocks
        style_codeblock = docx_doc.styles.add_style(STYLE_CODE, WD_STYLE_TYPE.PARAGRAPH)
        style_codeblock.font.name = FONT_CODE

        # Add title/subtitle
        if self.title or self.subtitle:
            # Create 6 empty lines
            for _ in range(6):
                para = Paragraph([Run("")])
                para._docx(docx_doc)

            # Add title
            if self.title:
                docx_doc.add_heading(self.title, 0)
            # Add subtitle
            if self.subtitle:
                docx_para = Paragraph([Run(self.subtitle)])._docx(docx_doc)
                # TODO: centre `docx_para`

            # Page break
            docx_para = docx_doc.add_paragraph()
            docx_run = docx_para.add_run()
            docx_run.add_break(WD_BREAK.PAGE)

        # Add elements
        for element in self.elements:
            element._docx(docx_doc)

        # Use docx's vanilla save
        docx_doc.save(path)
