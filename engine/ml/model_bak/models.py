from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC, SVC


def do_logistic_regression(x_train, y_train):
    classifier = LogisticRegression()
    classifier.fit(x_train, y_train)
    return classifier


def do_random_forest(x_train, y_train):
    classifier = RandomForestClassifier()
    classifier.fit(x_train, y_train)
    return classifier


def do_svm(x_train, y_train):
    classifier = SVC()
    classifier.fit(x_train, y_train)
    return classifier


def test_predictor(classifier, x_test, y_test):
    pred = classifier.predict(x_test)

    hit_count = 0
    total_count = len(y_test)
    for index in range(total_count):
        if (pred[index]) == (y_test[index]):
            hit_count = hit_count + 1

    hit_ratio = hit_count / total_count
    score = classifier.score(x_test, y_test)
    # print "hit_count=%s, total=%s, hit_ratio = %s" % (hit_count,total_count,hit_ratio)

    return hit_ratio, score
