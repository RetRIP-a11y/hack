with open('upload/fin.txt', 'r') as file_text:
    with open('upload/key.txt', 'r') as file_key:
        key = file_key.read()
        text = file_text.read()
        line = key.split('\n')
        for i in reversed(range(0, len(line) - 1)):
            change = line[i]
            change = change.split('|')
            word = change[0]
            hash = change[1]
            alias = change[2]
            text = text.replace(alias, word)
with open('upload/translate.txt', 'w') as file:
    file.write(text)
