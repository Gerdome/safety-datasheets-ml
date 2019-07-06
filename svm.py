import pandas as pd
from sklearn_crfsuite import CRF
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn import svm


data = pd.read_pickle("data_model_fwe.pkl")

#data.fillna(0)

# Separating out the features
X = data.loc[:, features]
# Separating out the target (+ doc for split)
y = data.loc[:,'chapter':'usecase_pro']

#split by documents so that either all of one document is train or test 
#train_inds, test_inds = GroupShuffleSplit().split(X, y, goups).next()
#X_train, X_test, y_train, y_test = X[train_inds], X[test_inds], y[train_inds], y[test_inds]

docs = list(X.doc.unique())

print(docs)

docs_train, docs_test = train_test_split(docs)

print(len(docs_train))
print(len(docs_test))

#train test split
X_train, X_test, y_train, y_test  = X[X['doc'].isin(docs_train)], X[X['doc'].isin(docs_test)], y[y['doc'].isin(docs_train)], y[y['doc'].isin(docs_test)]

y_train = y_train.loc[:,['label']]
y_test = y_test.loc[:,['label']]

y_pred = classifier.predict(X_test)

pd.DataFrame(y_pred).to_csv("pred.csv")
pd.DataFrame(y_test).to_csv("y_test.csv")

print(y_pred)

score = classifier.score(X_test, y_test)
print(score)

cm = metrics.confusion_matrix(y_test, y_pred)
print(cm)

'''
plt.figure(figsize=(9,9))
sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r');
plt.ylabel('Actual label');
plt.xlabel('Predicted label');
all_sample_title = 'Accuracy Score: {0}'.format(score)
plt.title(all_sample_title, size = 15);
'''

# Use sckit classification report for showing accuracy
print(classification_report(y_pred=y_pred, y_true=y_test))