from pathlib import Path
import docx
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_BREAK
from docx.shared import RGBColor, Pt, Cm

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
        # Check that run is a string; python doesn't have strong typing sadly
        if type(text) != str:
            raise Exception("Make sure this run is a string, this is a common mistake")
        # Create tuns
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
        # Justify text
        docx_para.alignment = 3  # TODO: integrate into paragraph style
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
        # Calculate justification for lines
        just = len(str(len(self.lines)))
        # Add lines
        for ind, line in enumerate(self.lines):
            # Figure out line number
            num = str(ind + 1).rjust(just)
            # Add new paragraph with code style
            docx_para = docx_doc.add_paragraph()
            docx_para.style = STYLE_CODE
            # Add line number with italics
            docx_run = docx_para.add_run(num)
            docx_run.font.italic = True
            # Add actual code
            docx_para.add_run(" " + line)

        # Add small codeblock line for formatting
        # NOTE: could be it's own style for consistency
        docx_para = docx_doc.add_paragraph()
        docx_para.paragraph_format.space_after = Pt(0)
        docx_para.paragraph_format.line_spacing = 0.7


class Quote(Paragraph):
    """Quote of something in it's own style"""

    @staticmethod
    def _md(line: str):
        # Level info
        level, line = _level_info(line)
        # Clean line from `>` starter
        line = line[1:].lstrip()
        # Parse via inheritance and convert
        para = super(Quote, Quote)._md(
            line
        )  # BODGE: python doesn't like staticmethod and inheritance
        quote = Quote(para.runs)
        # Set levelling
        quote.level = level
        return quote

    def _docx(self, docx_doc: docx.Document) -> docx.text.paragraph.Paragraph:
        # Get inherited generated paragraph
        para = super()._docx(docx_doc)
        # Reset to quote styling
        para.style = "Quote"
        para.alignment = 0  # TODO: integrate into quote style
        para.paragraph_format.left_indent = Cm(0.75)
        return para


class PointBullet(Paragraph):
    """Bullet point with content inside of it"""

    @staticmethod
    def _md(line: str):
        # Level info
        level, line = _level_info(line)
        # Clean line from `-` starter
        line = line[1:].lstrip()
        # Parse via inheritance and convert
        para = super(PointBullet, PointBullet)._md(
            line
        )  # BODGE: python doesn't like staticmethod and inheritance
        bullet = PointBullet(para.runs)
        # Set levelling
        bullet.level = level
        return bullet

    def _docx(self, docx_doc: docx.Document) -> docx.text.paragraph.Paragraph:
        # Get inherited generated paragraph
        docx_para = super()._docx(docx_doc)
        # Set bullet style according to level
        docx_para.style = (
            "List Bullet" if self.level == 0 else f"List Bullet {self.level}"
        )  # TODO: fix bullet points being weird
        return docx_para


class PointNumbered(Paragraph):
    """Numbered point with content inside of it"""

    @staticmethod
    def _md(line: str):
        # Level info
        level, line = _level_info(line)
        # Get number and clean
        splitted = line.split(".", 1)
        num = int(splitted[0])
        line = splitted[1].lstrip()
        # Parse via inheritance and convert
        para = super(PointNumbered, PointNumbered)._md(
            line
        )  # BODGE: python doesn't like staticmethod and inheritance
        numbered = PointNumbered(para.runs)
        # Set info
        numbered.level = level
        numbered.num = num
        return numbered

    def _docx(self, docx_doc: docx.Document) -> docx.text.paragraph.Paragraph:
        # TODO: use something like "start at self.num" so markdown starting at like `20.` can be used
        # Get inherited generated paragraph
        docx_para = super()._docx(docx_doc)
        # Set bullet style according to level
        docx_para.style = (
            "List Number" if self.level == 0 else f"List Number {self.level}"
        )  # TODO: fix bullet points being weird
        return docx_para


class Document:
    """High-level document abstractions for conversion"""

    FONT_HEADING = "IBM Plex Sans"
    FONT_BODY = "IBM Plex Serif"
    FONT_CODE = "IBM Plex Mono"

    elements = []
    title = None
    subtitle = None

    def __init__(self, md: str, arial: bool = False):
        # Set arial font
        if arial:
            self._arial()

        # Get and clear up lines
        lines_raw = md.splitlines()
        lines = []
        for line in lines_raw:
            # Strip anything from the rights
            line = line.rstrip()
            # Append only non-empty lines
            if line != "":
                lines.append(line)

        # Metadata
        if len(lines) > 1 and lines[0] == "---":
            # Go over lines in metadata
            skip = 0
            for ind, line in enumerate(lines[1:]):
                # Stop metadata if it's ended
                if line == "---":
                    skip = ind + 1
                    break
                # Split at `:` token
                splitted = line.split(":", 1)
                # Go to next line if its invalid
                if len(splitted) != 2:
                    continue
                # Clean left and right sections
                left = splitted[0].lstrip().lower()
                right = splitted[1].lstrip()
                # Match left section
                if left == "title":
                    self.title = right
                elif left == "subtitle":
                    self.subtitle = right
            # Skip to end of metadata if there was an open and close tag
            if skip != 0:
                lines = lines[1 + skip :]

        # TODO: get title/subtitle from metadata

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
            elif stripped.startswith(">"):
                # Quote
                self.elements.append(Quote._md(line))
            elif stripped.startswith("-"):
                # Bullet point
                self.elements.append(PointBullet._md(line))
            else:
                # Check misc
                try:
                    # Numbered point
                    if "." not in stripped:
                        raise Exception()
                    int(stripped.split(".", 1)[0])
                    self.elements.append(PointNumbered._md(line))
                except:
                    # Paragraph
                    self.elements.append(Paragraph._md(stripped))

            # TODO: image

            # Move to next line
            ind += 1

    def _arial(self):
        """Sets all fonts to Arial if you can't support IBM Plex"""

        self.FONT_HEADING = "Arial"
        self.FONT_BODY = "Arial"
        # TODO: codeblock non-plex, it goes weird without plex

    def save(self, path: Path):
        """Saves document to `path` provided"""
        # Create docx file
        docx_doc = docx.Document()

        # New styles
        style_codeblock = docx_doc.styles.add_style(STYLE_CODE, WD_STYLE_TYPE.PARAGRAPH)

        # Add title/subtitle
        if self.title or self.subtitle:
            # Create empty lines before title
            for _ in range(4):
                para = Paragraph([Run("")])
                para._docx(docx_doc)

            # Add title
            if self.title:
                docx_para = docx_doc.add_heading(self.title, 0)
                docx_para.alignment = 1  # TODO: integrate into title style
            # Add subtitle
            if self.subtitle:
                docx_para = Paragraph([Run(self.subtitle)])._docx(docx_doc)
                docx_para.style = "Subtitle"
                docx_para.alignment = 1  # TODO: integrate into subtitle style

            # Page break
            docx_para = docx_doc.add_paragraph()
            docx_run = docx_para.add_run()
            docx_run.add_break(WD_BREAK.PAGE)

        # Add elements
        for element in self.elements:
            element._docx(docx_doc)

        # Replace all fonts with body font by default
        for style in docx_doc.styles:
            if hasattr(style, "font"):
                style.font.name = self.FONT_BODY

        # Styling for title
        style_title = docx_doc.styles["Title"]
        _style_title_border(style_title)
        style_title.font.name = self.FONT_HEADING
        style_title.font.size = Pt(26)
        style_title.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        style_title.paragraph_format.space_after = Pt(3)

        # Styling for subtitle
        style_subtitle = docx_doc.styles["Subtitle"]
        style_subtitle.font.name = self.FONT_HEADING
        style_subtitle.font.size = Pt(14)
        style_subtitle.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        style_subtitle.font.italic = False

        # Styling for headings
        for h in range(1, 9):
            style_heading = docx_doc.styles[f"Heading {h}"]
            style_heading.font.name = self.FONT_HEADING
            style_heading.font.bold = False
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
        style_paragraph.font.size = Pt(12)

        # Styling for codeblocks
        style_codeblock.font.name = self.FONT_CODE
        style_codeblock.paragraph_format.line_spacing = 0.4

        # Styling for bullet points
        # TODO: left_indent and -2px vert align for bullet points

        # Styling for numbered points
        # TODO: left_indent for numbered points

        # Use docx's vanilla save
        docx_doc.save(path)


def _style_title_border(style_title):
    """Removes border style on title which is set by python-docx by default.
    This is a hack because there's no programmatic way to do this as of writing"""
    el = style_title._element
    el.remove(el.xpath("w:pPr")[0])


def _level_info(line: str) -> tuple:
    """Figures out level information and returns it and the line without spacing"""
    stripped = line.lstrip()
    num = len(line) - len(stripped)
    level = int(num / 2)
    return (level, stripped)
