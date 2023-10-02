from mdcx import Document, Style

# AirBnB
md_path = "airbnb.md"
md = open(md_path, "r").read()
doc = Document(md, md_path)
doc.save("airbnb.docx")

# AirBnB with alternate theme
doc = Document(md, md_path, Style.foxtrot())
doc.save("airbnb_foxtrot.docx")

# Constructs
md_path = "constructs.md"
md = open(md_path, "r").read()
doc = Document(md, md_path)
doc.save("constructs.docx")

# Constructs with alternate theme
doc = Document(md, md_path, Style.foxtrot())
doc.save("constructs_foxtrot.docx")
