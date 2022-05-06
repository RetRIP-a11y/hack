import textract


def decrypt(text):
    replace = []
    key = textract.process("upload/test/keys.txt")
    key = key.decode(encoding='utf-8')
    key = key.split('\n')
    for i in key:
        try:
            replace.append([i.split('|')[2], i.split('|')[0]])
        except:
            pass

    for j in replace:
        text = text.replace(j[0], j[1])
    return text
