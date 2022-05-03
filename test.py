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
from ipymarkup import show_span_ascii_markup as show_markup

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
ner_tagger = NewsNERTagger(emb)
name_ex = NamesExtractor(morph_vocab)
ad_ex = AddrExtractor(morph_vocab)
date_ex = DatesExtractor(morph_vocab)

def one(text):
    dic ={}
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)
    name = name_ex(text)
    for i in name:
        if i.fact.first is not None and i.fact.last is not None and i.fact.middle is not None:
            dic.update({text[i.start:i.stop]: (i.start, i.stop)})
    for key, val in dic.items():
        text = text.replace(key, '''|'''+text[val[0]:val[1]]+'''|''')
    return text
