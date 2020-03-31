import pandas
from sklearn import tree
from sklearn.model_selection import train_test_split
filename = 'Empowerment.csv'
names = ['type', 'title', 'percentage', 'population']
data = pandas.read_csv(filename,names=names)
print(data.head)
print(data.shape)
features = [[0,70],[1,40],[2,10],[0,65],[2,15]]
labels = [0,1,2,0,2]
algorithm = tree.DecisionTreeClassifier()
algorithm = algorithm.fit(features, labels)
newData = [[2,80]]
print(algorithm.predict(newData))
if algorithm.predict(newData)==0:
    print("liability")
elif algorithm.predict(newData)==1:
    print("empowered")
elif algorithm.predict(newData)==2:
    print("asset")
y=data.title
x=data.drop('title',axis=1)
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
print(x_train.head())
print(x_train.shape)
print(x_test.head())
print(x_test.shape)

