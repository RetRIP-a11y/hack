import zipfile

with zipfile.ZipFile('upload/decrypt.docx', 'r') as z:
    filesInArchive = z.infolist()
    for fileArch in filesInArchive:
        if fileArch.filename == 'word/theme/theme1.xml':
            with z.open(fileArch.filename) as secret:
                line = secret.read().decode('utf-8').split('\n')
                print(line[len(line)-1])

