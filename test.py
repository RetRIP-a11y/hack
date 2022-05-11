import textract
from docx import Document
import os
import zipfile

document = 'upload/finaly.docx'

doc = Document(document)
paragraphs = doc.paragraphs
for i in paragraphs:
    i.text = None
doc.save(document)