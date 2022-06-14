from pathlib import Path
import re
import docx
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_BREAK
from docx.shared import RGBColor, Pt, Cm
import sys

STYLE_CODE = "Code"
CLI_HELP = "Usage: mdx [in] [out]\n\n  Seemless markdown to docx converter\n\nArguments:\n  --andy    Alternate high-clarity document format"


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
        # Parse through runs
        runs = []
        ind = 0
        flipflop = False
        bold = False
        italic = False
        buf = ""
        add = True
        # Go through each character
        while ind < len(line):
            # Get character
            c = line[ind]
            # Bold/italics
            if c == "*":
                # Calculate flipflop
                add = flipflop
                if flipflop:
                    flipflop = False
                    continue
                # Add previous buffer
                runs.append(Run(buf, bold, italic))
                buf = ""
                # Get star length
                stars = len(line[ind:]) - len(line[ind:].lstrip("*"))
                # Italics if theres a non-even amount
                if stars % 2 == 1:
                    italic = not italic
                # Bold if theres two or more
                if stars > 1:
                    bold = not bold
                ind += stars - 1
            # Heading link
            match = re.search(" \[.*\]\(.*\)", line[ind:])  # TODO: better pattern
            # TODO: parse match
            # External link
            # TODO
            # Add to ind/buf
            if add:
                buf += c
            else:
                add = True
            ind += 1

        # Create and return paragraph
        runs.append(Run(buf, bold, italic))
        return Paragraph(runs)

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
        self, lines: list, lang: str = None, heading_after: bool = False
    ):  # TODO: use `lang` somewhere in docx
        self.lines = lines
        self.lang = lang
        self.heading_after = heading_after

    @staticmethod
    def _md(lines: list) -> tuple:
        # Get language after ``` designator
        lang = (
            lines[0].lstrip()[3:].lstrip()
        )  # first `lstrip()` used in document parsing
        lang = lang if lang != "" else None

        # Read lines
        heading_after = False
        code = []
        for ind, line in enumerate(lines[1:]):
            if line.lstrip() == "```":
                # Check if there's a heading afterwards
                if len(lines[1:]) > ind and lines[ind + 2].lstrip().startswith("#"):
                    heading_after = True
                # Stop codeblock
                break
            else:
                code.append(line)

        # Get skip
        skip = len(code) + 1
        return (Codeblock(code, lang, heading_after), skip)

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

        # Add small codeblock line for formatting if there's not a heading afterwards
        if not self.heading_after:
            docx_para = docx_doc.add_paragraph()
            docx_para.style = STYLE_CODE


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
            "List Bullet" if self.level == 0 else f"List Bullet {self.level+1}"
        )  # TODO: fix `KeyError: "no style with name 'List Bullet 1'"`
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
        # TODO: use something like "start at self.num" so markdown starting at like `20.` can be used, it fucks up otherwise
        # Get inherited generated paragraph
        docx_para = super()._docx(docx_doc)
        # Set bullet style according to level
        docx_para.style = (
            "List Number" if self.level == 0 else f"List Number {self.level}"
        )
        return docx_para


class Document:
    """High-level document abstractions for conversion"""

    FONT_HEADING = "IBM Plex Sans"
    FONT_BODY = "IBM Plex Serif"
    FONT_CODE = "IBM Plex Mono"

    elements = []
    title = None
    subtitle = None

    def __init__(self, md: str, andy: bool = False):
        # Set andy format
        self.andy = andy
        # Remove toc and clear up lines
        lines_raw = _rm_toc(md)
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

            # TODO: images

            # Move to next line
            ind += 1

    def save(self, path: Path):
        """Saves document to `path` provided"""
        # Create docx file
        docx_doc = docx.Document()

        for s in docx_doc.styles:
            if "bullet" in s.name.lower():
                print(s)

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
            # Add subtitle
            if self.subtitle:
                docx_para = Paragraph([Run(self.subtitle)])._docx(docx_doc)
                docx_para.style = "Subtitle"

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
                style.font.name = self.FONT_BODY if not self.andy else "Arial"

        # Styling for title
        style_title = docx_doc.styles["Title"]
        _style_title_border(style_title)
        style_title.font.name = self.FONT_HEADING if not self.andy else "Arial"
        style_title.font.size = Pt(26)
        style_title.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        style_title.paragraph_format.space_after = Pt(3)
        style_title.paragraph_format.alignment = 1

        # Styling for subtitle
        style_subtitle = docx_doc.styles["Subtitle"]
        style_subtitle.font.name = self.FONT_HEADING if not self.andy else "Arial"
        style_subtitle.font.size = Pt(14)
        style_subtitle.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        style_subtitle.font.italic = False
        style_subtitle.paragraph_format.alignment = 1

        # Styling for headings
        for h in range(1, 9):
            style_heading = docx_doc.styles[f"Heading {h}"]
            style_heading.font.name = self.FONT_HEADING if not self.andy else "Arial"
            style_heading.font.bold = self.andy
            style_heading.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

            # Per-level styling
            if h == 1:
                style_heading.font.size = Pt(22)
                style_heading.paragraph_format.space_after = Pt(2)
            elif h == 2:
                style_heading.font.size = Pt(17)
            elif h <= 4:
                style_heading.font.size = Pt(13)
            # Italics for small headings
            if h > 3:
                style_heading.font.italic = True

        # Styling for paragraphs
        style_paragraph = docx_doc.styles["Normal"]
        style_paragraph.paragraph_format.alignment = 3
        if self.andy:
            style_paragraph.font.size = Pt(12)
            style_paragraph.paragraph_format.line_spacing = 1.5

        # Styling for codeblocks
        style_codeblock.font.name = (
            self.FONT_CODE
        )  # TODO: andy mono font; plex goes weird
        style_codeblock.paragraph_format.space_after = Pt(0)
        style_codeblock.paragraph_format.line_spacing = 1

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


def _err_exit(msg: str):
    """Prints error message to console and exits program, used for command-line"""
    print(f"{CLI_HELP}\n\nError: {msg}", file=sys.stderr)
    sys.exit(1)


def _rm_toc(md: str) -> list:
    """Removes first table of contents section from a markdown string, returning list of lines"""
    # Don't check if there isn't one
    check = md.lower()
    if "table of contents" not in check and "contents" not in check:
        return md
    # Parse through
    in_toc = False
    removed_toc = False
    keep = []
    for line in md.splitlines():
        clean = line.lstrip()
        # Title, so either start/end toc removal
        if clean.startswith("#") and not removed_toc:
            # Stop removing toc
            if in_toc:
                in_toc = False
                keep.append(line)
                continue
            # Start removing toc
            title = clean.lstrip("#").strip().lower()
            if title in ["table of contents", "contents"]:
                in_toc = True
            else:
                keep.append(line)
        # Add like normal
        elif not in_toc:
            keep.append(line)
    return keep


# Command-line
if __name__ == "__main__":
    # Get and clean arguments
    args = sys.argv[1:]
    # Make sure theres at least an input and output or show help
    if len(args) == 0:
        _err_exit("Please provide [in]")
    elif "--help" in args[2:]:
        print(CLI_HELP)
        sys.exit(0)
    # Get andy setting
    andy = "--andy" in args[2:]
    # Get markdown from file
    md = ""
    try:
        with open(args[0], "r") as file:
            md = file.read()
    except Exception as e:
        _err_exit(f"Invalid file, {e}")
    # Create and save document to defined parts
    try:
        Document(md, andy).save(args[1])
    except:
        _err_exit("Couldn't convert document")  # TODO: better errors
