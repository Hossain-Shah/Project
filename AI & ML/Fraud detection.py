from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pandas as pd
df = pd.read_csv('D:/Pycharm/Program/AI,Stat & ANN/Credit-card-dataset/creditcard.csv')
print(df)
print(df.describe())
features = ['Amount'] + ['V%d' % number for number in range(1, 29)]
target = 'Class'
X = df[features]
y = df[target]


def normalize(X):
    for feature in X.columns:
        X[feature] -= X[feature].mean()
        X[feature] /= X[feature].std()
    return X


model = LogisticRegression()
splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.5, random_state=0)
for train_indices, test_indices in splitter.split(X, y):
    X_train, y_train = X.iloc[train_indices], y.iloc[train_indices]
    X_test, y_test = X.iloc[test_indices], y.iloc[test_indices]
    X_train = normalize(X_train)
    X_test = normalize(X_test)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
