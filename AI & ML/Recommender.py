import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
metadata = pd.read_csv('D:/Pycharm/Program/AI_Stat_ANN/AttractionScoringDataset/ratings.csv', low_memory=False)
print(metadata.head(13))
C = metadata['Rating'].mean()
print(C)
m = metadata['Attractive'].quantile(0.9)
print(m)
n = metadata['Average'].quantile(0.9)
print(n)
l = metadata['Non-attractive'].quantile(0.9)
print(l)
a = metadata.copy().loc[metadata['Rating'] >= C]
print(a.shape)
print(metadata.shape)


def weighted_rating(x, m=m, n=n, l=l, C=C):
    u = x['Attractive']
    v = x['Average']
    w = x['Non-attractive']
    R = x['Rating']
    return ((u+v+w)/(u+v+w+m+n+l) * R) + ((m+n+l)/(m+n+l+u+v+w) * C)


a['score'] = a.apply(weighted_rating, axis=1)
a = a.sort_values('score', ascending=False)
print(a[['Filename', 'Attractive', 'Average', 'Non-attractive', 'Rating', 'score']].head(13))
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(metadata['Filename'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(metadata.index, index=metadata['Filename']).drop_duplicates()
print(indices[:13])


def get_recommendations(Filename, cosine_sim=cosine_sim):
    idx = indices[Filename]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:13]
    d = [i[0] for i in sim_scores]
    return metadata['Filename'].iloc[d]


print(get_recommendations('Md Shahnawaz Hossain.jpg'))



