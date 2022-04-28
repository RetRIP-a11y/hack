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
            result = '!NAME!'
            replaceDic.update({paragraph[i.start:i.stop]: result})
    date = date_ex(paragraph)
    for j in date:
        line = doc.text[j.start:j.stop]
        result = ' !DATA! '
        replaceDic.update({line: result})
    addr = ad_ex(paragraph)
    for q in addr:
        line = doc.text[q.start:q.stop]
        result = ' !ADDR! '
        replaceDic.update({line: result})



text = textract.process("upload/01.01.2021.doc")
text = text.decode(encoding='utf-8')
#
for key, val in replaceDic.items():
    text = text.replace(key, val)

with open('upload/fin.doc', 'w') as f:
    f.write(text)
