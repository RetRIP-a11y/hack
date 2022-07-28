import zipfile
import textract
import os
from docx import Document
import secrets
import string


def generate_alphanum_crypt_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    crypt_rand_string = ''.join(secrets.choice(
        letters_and_digits) for i in range(length))
    return crypt_rand_string


def add_id_files(documents):
    os.chdir('./upload')
    # Перезапись док в докикс
    try:

        text = textract.process(documents)
        text = text.decode('utf-8')
        doc = Document()
        doc.add_paragraph(text)
        doc.save('start.docx')
    except:
        os.rename(documents, 'start.docx')
    ######################################################
    # Разархивирование докикс
    if 'out' not in os.listdir('.'):
        os.mkdir('./out')

    with zipfile.ZipFile('start.docx') as zip_file:
        zip_file = zipfile.ZipFile('start.docx', 'r', allowZip64 = False)
        zip_file.extractall('./out/')


    #########################################
    with open('out/word/theme/theme1.xml', 'a') as f:
        key = '\n\n<!--' + generate_alphanum_crypt_string(64) + '-->'
        f.write(key)


    os.chdir('./out')
    with zipfile.ZipFile('new.docx', 'w') as z:
        paths = os.walk('.')
        for path in paths:
            for file in path[2]:
                z.write(path[0] + '/' + file)

    os.system('cp new.docx /home/user/PycharmProjects/hack/upload/fin.docx')
    os.chdir('/home/user/Загрузки/бутов/hack/upload')
    try:
        os.system('rm -r /home/user/PycharmProjects/hack/upload/out')
    except:
        pass

    os.system('rm -r /home/user/PycharmProjects/hack/upload/'+documents)
    os.system('rm -r /home/user/PycharmProjects/hack/upload/start.docx')
    os.chdir('/home/user/Загрузки/бутов/hack')
    return key


def show_id_files():
    with zipfile.ZipFile('upload/decrypt.docx', 'r') as z:
        filesInArchive = z.infolist()
        for fileArch in filesInArchive:
            if fileArch.filename == 'word/theme/theme1.xml':
                with z.open(fileArch.filename) as secret:
                    line = secret.read().decode('utf-8').split('\n')
                    line = line[len(line)-1]
                    return line[4:len(line)-3]
