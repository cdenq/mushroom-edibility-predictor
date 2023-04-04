# import libraries
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, recall_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import matplotlib.pyplot as plt
import math

# import variables from cleaner file
from main_preprocessing import preprocessing
X_train_scaled = preprocessing()[1]
X_test_scaled = preprocessing()[2]
y_train = preprocessing()[3]
y_test = preprocessing()[4]
global_random_state = preprocessing()[5]

# import model saving capability for modularity
import joblib

# general model fit-score
def fit_score(model, label):
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    f1 = f1_score(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    # print(f'-----{label}-----')
    # print(classification_report(y_test, y_pred))
    joblib.dump(model, f'Main/Resources/Models/{label}.pkl') #saving fitted model for modularity/passing to server
    return [acc, f1, prec, rec]

# general model fit-score
def model_score(model):
    y_pred = model.predict(X_test_scaled)
    f1 = f1_score(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    return [acc, f1, prec, rec]

# random forest function
def rfc():
    clf = RandomForestClassifier(n_estimators=50, random_state=global_random_state)
    return fit_score(clf, 'rfc')

# extremely random forest function
def erf():
    clf = ExtraTreesClassifier(n_estimators=50, random_state=global_random_state)
    return fit_score(clf, 'erf')

# logistic regression function for modularization
def lr():
    log = LogisticRegression()
    return fit_score(log, 'lr')

# svm function for modularization
def svm():
    svm = SVC(kernel='linear')
    return fit_score(svm, 'svm')

# going to manually ignore k at low values due to risk of outlier influence and overfitting
n_neighbors_manual = int(math.sqrt(len(X_train_scaled)))

# knn function for modularization
def knn_final():
    knn = KNeighborsClassifier(n_neighbors=n_neighbors_manual)
    return fit_score(knn, 'knn')

# save vars
# rfc_computed = rfc()
# erf_computed = erf()
# lr_computed = lr()
# svm_computed = svm()
# knn_computed = knn_final()