from natasha import (
    Segmenter,
    MorphVocab,
    PER,
    NamesExtractor,
    NewsNERTagger,
    NewsEmbedding,
    Doc
)

emb = NewsEmbedding()
segmenter = Segmenter()
morph_vocab = MorphVocab()
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)

text = '12 апреля 1998 года. Номер паспорта 0000 серия 213455 Яковлев Игнат Андреевич'

doc = Doc(text)

doc.segment(segmenter)

doc.tag_ner(ner_tagger)

for span in doc.spans:
    span.normalize(morph_vocab)
{_.text: _.normal for _ in doc.spans}


for span in doc.spans:
    if span.type == PER:
        span.extract_fact(names_extractor)

# {_.normal: _.fact.as_dict for _ in doc.spans if _.fact}



print()
for i in doc.spans:
    if i.fact:
        print(i.fact.as_dict)
        if 'first' in i.fact.as_dict:
            name = i.fact.as_dict['first']
        else:
            name = ''
        if 'last' in i.fact.as_dict:
            surname = i.fact.as_dict['last']
        else:
            surname = ''
        if 'middle' in i.fact.as_dict:
            nameFather = i.fact.as_dict['middle']
        else:
            nameFather = ''
        print('Имя - ', name, '\n', 'Фамилия - ', surname, '\n', 'Отчество - ', nameFather)
print()

for i in doc.text:
    if i.isdigit():
        print(i, end=' ')
    else:
        pass
print()
