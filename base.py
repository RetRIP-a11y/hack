import textract
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

text = textract.process("upload/01.01.2021.docx")
text = text.decode(encoding='utf-8')

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
ner_tagger = NewsNERTagger(emb)
# addr_extractor = AddrExtractor(morph_vocab)


name_ex = NamesExtractor(morph_vocab)
ad_ex = AddrExtractor(morph_vocab)
date_ex = DatesExtractor(morph_vocab)

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

replaceDic = {}
text = text.split('\n')
for paragraph in text:
    doc = Doc(paragraph)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)

    name = name_ex(paragraph)
    for i in name:
        if i.fact.first is not None and i.fact.last is not None and i.fact.middle is not None:
            line = doc.text[i.start:i.stop]
            result = encrypt(line, 3)
            replaceDic.update({line: result})
    date = date_ex(paragraph)
    for j in date:
        line = doc.text[j.start:j.stop]
        result = encrypt(line, 3)
        replaceDic.update({line: result})
    addr = ad_ex(paragraph)
    for q in addr:
        line = doc.text[q.start:q.stop]
        result = encrypt(line, 3)
        replaceDic.update({line: result})


text = textract.process("upload/01.01.2021.doc")
text = text.decode(encoding='utf-8')
#
for key, val in replaceDic.items():
    text = text.replace(key, val)

with open('upload/fin.txt', 'w') as f_txt:
    f_txt.write(text)

with open('upload/key.txt', 'w') as f_key:
    keys = ''
    for key, val in replaceDic.items():
        keys = keys + key + '|' + val + '\n'
    f_key.write(keys)
