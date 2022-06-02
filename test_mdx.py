from mdx import Document

md = """
# My document

Hello, there.

```
Woo
```

bahaha
"""

doc = Document(md)
doc.save("woo.docx")
