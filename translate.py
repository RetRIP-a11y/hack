import textract

text = textract.process("upload/fin.txt")
text = text.decode(encoding='utf-8')
# print(text)
with open('upload/key.txt', 'r') as f:
    txt = f.read()
    txt = txt.split('\n')
    for line in txt:
        line = line.split('|')
        try:
            text = text.replace(line[1], line[0])
        except:
            pass
with open('upload/decrypt.doc', 'w') as decrypt_t:
    decrypt_t.write(text)