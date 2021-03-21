import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

col_names = ['location', 'rms_y', 'average', 'standard_deviation', 'vairance', 'label']
data = pd.read_csv("data/data.csv", header=None, names=col_names, skiprows=1)
data.head()


def feature_to_dummy(data, column, drop=False):
    tmp = pd.get_dummies(data[column], prefix=column, prefix_sep='_')
    data = pd.concat([data, tmp], axis=1)
    if drop:
        del data[column]
    return data


data = feature_to_dummy(data, 'location', False)
feature_cols = ['location', 'rms_y', 'average', 'standard_deviation', 'vairance']
x = data[feature_cols]
y = data.label

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)

clf = DecisionTreeClassifier()
clf = clf.fit(x_train,y_train)

from sklearn import tree
import pydotplus
import pydot
from io import StringIO

dot_data = StringIO()
tree.export_graphviz(clf, out_file=dot_data,
                filled=True, rounded=True,
                special_characters=True,feature_names = feature_cols,class_names=['0','1'])

graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

graph.write_png("tree.png")

from joblib import dump
dump(clf, 'handling-specialty-machine-status-detection.joblib')

