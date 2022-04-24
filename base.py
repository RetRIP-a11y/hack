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
import re

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
    text = text.split('\n')
    for page in text:
        doc = Doc(page)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.tag_ner(ner_tagger)

        line = doc.text
        greps_name = ['\w\.\w\. \w*', '\w* \w\.\w\.', '\w\.\w\.\w.*', '\w.*\W']
        greps_date = ['\d{2}\.\d{2}\.\d{4}', '\d{2} \w* \d{4}']
        for grep in greps_name:
            if re.search(grep, line) != None:
                print('NAME  --  ', re.search(grep, line).group(0))
                print('-'*30)
        for grep in greps_date:
            if re.search(grep, line) != None:
                print('DATE  --  ', re.search(grep, line).group(0))
                print('-'*30)