from natasha import (
    Segmenter,
    MorphVocab,
    PER, LOC,
    NamesExtractor,
    NewsNERTagger,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    Doc,
    DatesExtractor, AddrExtractor)
import hashlib

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)
date_extractor = DatesExtractor(morph_vocab)
addr_extractor = AddrExtractor(morph_vocab)


def encrypt(line, change: int):
    texts = hashlib.md5(line.encode()).hexdigest()
    # 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    # 'abcdefghijklmnopqrstuvwxyz'
    string = 'abcdefghijklmnopqrstuvwxyz'
    line2 = list(string)
    line3 = list(string.upper())
    result_list = list(texts)
    for i in range(0, len(result_list)):
        if result_list[i] in line2 or result_list[i] in line3:
            if i < len(string) - 1 - change:
                result_list[i] = line2[i + change]
            elif i >= len(string) - 1 - change:
                result_list[i] = line2[i - len(string) - 1 + change]
    final = ''.join(result_list)
    return final


with open('upload/temp.txt', 'r') as file:
    text = file.read()
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)

    for token in doc.tokens:
        token.lemmatize(morph_vocab)

    replaceDict = {}
    for span in doc.spans:
        span.normalize(morph_vocab)
        if span.type == PER:
            span.extract_fact(names_extractor)
            line = span.text
            result = encrypt(line, 5)
            replaceDict.update({line: result})

    date = date_extractor(text)
    for j in date:
        line = doc.text[j.start:j.stop]
        result = encrypt(line, 5)
        replaceDict.update({line: result})

    i = 0
    for key, val in replaceDict.items():
        doc.text = doc.text.replace(key, 'name' + str(i) + 'N')
        i += 1

    # ADDR
    dicADDR = {}
    test = addr_extractor(text)
    for j in test:
        line = j.fact.value
        if line != 'А':
            result = encrypt(line, 5)
            dicADDR.update({line: result})
    j = 0
    for key, val in dicADDR.items():
        doc.text = doc.text.replace(key, 'addr' + str(j) + 'N')
        j += 1
    # ADDR

with open('upload/fin.txt', 'w') as file:
    file.write(doc.text)
with open('upload/key.txt', 'w') as file:
    key_text = ''
    i = 0
    for key, val in replaceDict.items():
        key_text = key_text + str(key) + '|' + val + '|' + 'name' + str(i) + 'N' + '\n'
        i += 1
    j = 0
    for key, val in dicADDR.items():
        key_text = key_text + str(key) + '|' + val + '|' + 'addr' + str(j) + 'N' + '\n'
        j += 1
    file.write(key_text)
