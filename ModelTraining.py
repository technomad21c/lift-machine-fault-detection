import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

class ModelTraining():
    def __init__(self):
        self.col_names = ['location','rms_y', 'average', 'standard_deviation', 'variance', 'label']

    def load(self):
        self.data = pd.read_csv("data/data.csv", header=None, names=self.col_names, skiprows=1)
        self.data = self.feature_to_dummy(self.data, 'location', False)

    def feature_to_dummy(self, data, column, drop=False):
        tmp = pd.get_dummies(data[column], prefix=column, prefix_sep='_')
        data = pd.concat([data, tmp], axis=1)
        if drop:
            del data[column]
        return data

    def train(self):
        self.feature_cols = ['location_motorfan', 'location_lowerbrace', 'location_upperrockerarm', 'rms_y', 'average', 'standard_deviation', 'variance']
        x = self.data[self.feature_cols]
        y = self.data.label

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)

        self.clf = DecisionTreeClassifier()
        self.clf = self.clf.fit(x_train,y_train)

        y_pred = self.clf.predict(x_test)
        print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

    def visualize(self):
        from sklearn import tree
        import pydotplus
        import pydot
        from io import StringIO

        dot_data = StringIO()
        tree.export_graphviz(self.clf, out_file=dot_data,
                        filled=True, rounded=True,
                        special_characters=True,feature_names = self.feature_cols,class_names=['0','1'])

        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.write_png("tree.png")

    def save(self):
        from joblib import dump
        dump(self.clf, 'handling-specialty-machine-status-detection.joblib')

    def detect(self):
        from joblib import load
        clf = load('handling-specialty-machine-status-detection.joblib')

        result = clf.predict([[1, 0, 0, 100.98,84.19363636363636,590.1159504132231,24.29230228721072]])
        print(result)

        # y_pred = clf.predict(x_test)
        # print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

