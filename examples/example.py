from mdx import Document, Style

# AirBnB
md = open("airbnb.md", "r").read()
doc = Document(md)
doc.save("airbnb.docx")

# AirBnB with alternate theme
doc = Document(md, Style.foxtrot())
doc.save("airbnb_foxtrot.docx")

# Constructs
md = open("constructs.md", "r").read()
doc = Document(md)
doc.save("constructs.docx")

# Constructs with alternate theme
doc = Document(md, Style.foxtrot())
doc.save("constructs_foxtrot.docx")
