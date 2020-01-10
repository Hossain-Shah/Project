from nltk.corpus import wordnet,stopwords
syn=wordnet.synsets('love')
print(syn)
antonyms=[]
for syn in wordnet.synsets('depressed'):
    for l in syn.lemmas():
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())
print(antonyms)
synonyms=[]
for syn in wordnet.synsets('AI'):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())
print(synonyms)
print(stopwords.words('english'))
