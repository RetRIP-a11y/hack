import textract
from ipymarkup import show_span_box_markup
from ipymarkup.palette import palette, BLUE, RED, GREEN, BROWN
from ipymarkup import format_span_box_markup
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
ner_tagger = NewsNERTagger(emb)
name_ex = NamesExtractor(morph_vocab)
ad_ex = AddrExtractor(morph_vocab)
date_ex = DatesExtractor(morph_vocab)


def one(text):
    NameList = []
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)
    name = name_ex(text)
    date = date_ex(text)
    addr = ad_ex(text)
    for i in name:
        if i.fact.first is not None and i.fact.last is not None and i.fact.middle is not None:
            NameList.append((i.start, i.stop, 'PER'))
    for q in addr:
        NameList.append((q.start, q.stop, 'LOC'))
    for j in date:
        NameList.append((j.start, j.stop, 'DATE'))
    return ', '.join(list(format_span_box_markup(text, NameList)))

# text = textract.process("upload/01.01.2021.doc")
# text = text.decode(encoding='utf-8')
# one(text)
