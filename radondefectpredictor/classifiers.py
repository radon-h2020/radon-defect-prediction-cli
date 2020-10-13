from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

classifiers_map = {
    'decision-tree':DecisionTreeClassifier(),
    'naive-bayes':GaussianNB(),
    'logistic':LogisticRegression(),
    'random-forest':RandomForestClassifier(),
    'svc':SVC()
}

