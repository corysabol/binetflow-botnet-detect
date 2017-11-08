import os
import sys

import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier as DT
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import average_precision_score, accuracy_score
from sklearn.metrics import classification_report

def train_decision_tree(X_train, X_test, y_train, y_test):
    print("Training decision tree")
    clf = DT(random_state=0)
    clf = clf.fit(X_train, y_train)
    print(clf)
    p = clf.predict(X_test)
    report = classification_report(y_test, p)
    print(report)

def train_svm(X_train, X_test, y_train, y_test):
    print("Training svm")
    clf = SVC(verbose=True)
    clf = clf.fit(X_train, y_train)
    print(clf)
    p = clf.predict(X_test)
    report = classification_report(y_test, p)
    print(report)

def train_rand_forest(X_train, X_test, y_train, y_test):
    None

def main():
    args = sys.argv

    directory = os.fsencode(os.path.join('..','Datasets','ctu13pickles'))
    for f in os.listdir(directory):
        # read in the data set and prep it for training
        df = pd.read_pickle(os.path.join(directory.decode('utf-8'), f.decode('utf-8')))
        df.dropna(inplace=True)
        y = df['label']
        df.drop(['label'], axis=1, inplace=True)
        print(df.shape)
        X_train, X_test, y_train, y_test = tts(df, y, train_size=0.7)

        #train_svm(X_train, X_test, y_train, y_test)
        train_decision_tree(X_train, X_test, y_train, y_test)
        
        print("Dataframe: shape {}".format(df.shape))
        print("======================\n")

if __name__ == '__main__': main()
