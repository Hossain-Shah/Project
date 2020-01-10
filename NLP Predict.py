import nltk.classify.util
from nltk.corpus import names
nltk.download('names')


def gender_features(word):
    return {'last_letter': word[-1]}


names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
featuresets = [(gender_features(n), g) for (n,g) in names]
train_set = featuresets
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(classifier.classify(gender_features('Annie')))