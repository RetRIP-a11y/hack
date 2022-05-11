import sqlite3
import base
from docx import Document

conn = sqlite3.connect('withOutFace.db', check_same_thread=False)
cur = conn.cursor()


def decrypts(text, keyFile):
    HM = []
    W = []
    SUM = []
    key = "'" + keyFile + "'"
    sql1 = "SELECT hash, mark FROM hashAndMark WHERE keyFile=" + key + ";"
    res1 = cur.execute(sql1)
    for r1 in res1:
        HM.append([r1[0], r1[1]])
    sql2 = "SELECT string FROM data WHERE keyFaile=" + key + ";"
    res2 = cur.execute(sql2)
    for r2 in res2:
        line = base.encrypt(r2[0], 3)
        W.append([r2[0], line])

    for i in HM:
        for j in W:
            if i[0] == j[1]:
                SUM.append([j[0], i[1]])

    for word, alias in SUM:
        text = text.replace(alias, word)

    doc = Document()
    doc.add_paragraph(text)
    doc.save('upload/decrypt.docx')
    return text
