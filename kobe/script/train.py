#!/usr/bin/env python
# encoding: utf-8

import csv
import sys
import copy
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.svm import SVC
from xgboost.sklearn import XGBRegressor
from xgboost.sklearn import XGBClassifier
from sklearn.cross_validation import *
from sklearn import grid_search
from sklearn.metrics import log_loss

def gbdtClassifier(x,y,targetx, kfold):
    print "gbdtClassifier"
    grid = grid_search.GridSearchCV(estimator=GradientBoostingClassifier(),
            param_grid = {
                'n_estimators' : [1000],
                'max_depth' : [4,6],
                'learning_rate' : [0.008],
                'subsample' : [0.6],

                },
            cv = kfold,
            scoring='log_loss',
            n_jobs=1
            )
    grid.fit(x,y)
    print(grid.best_score_)
    print(grid.best_params_)

    #param = grid.best_params_
    #newclf = GradientBoostingClassifier(n_estimators=param['n_estimators'],max_depth = param['max_depth'], learning_rate = param['learning_rate'])
    #newclf = GradientBoostingClassifier(grid.best_params_)
    #newclf.fit(x,y)
    return grid.predict_proba(targetx)[:,1]
    #return newclf.predict_proba(targetx)[:,1]

def getParam(tag):
    params = list()

    n_estimators = [1000]
    max_depth = [4]
    learning_rate = [0.006]#,0.0075,0.007,0.006]
    subsample = [0.6]
    loss = ['ls']

    p = dict()
    for n in n_estimators:
        p['n_estimators'] = n
        for dp in max_depth:
            p['max_depth'] = dp
            for lr in learning_rate:
                p['learning_rate'] = lr
                for ss in subsample:
                    p['subsample'] = ss

                    if tag == 'regressor':
                        for l in loss:
                            p['loss'] = l
                    params.append(copy.copy(p))

    return params



def gbdtRegressor(x,y,targetx):
    pa = getParam('')
    for p in pa:
        clf = GradientBoostingClassifier(**p)
        scores = cross_val_score(clf,x,y,cv=5,scoring='log_loss')
        print scores
        print sum(scores)/len(scores)
        print p
    clf.fit(x,y)
    return clf.predict_proba(targetx)[:,1]
    pass

def gbdt(x,y,targetx):
    pa = getParam('regressor')
    for p in pa:
        kf = KFold(len(x),n_folds=8, shuffle=True)

        #clf = GradientBoostingRegressor(**p).fit(x,y)
        #return clf.predict(targetx)

        dx = x.values
        dy = y.values
        total = list()
        for train_index, test_index in kf:
            x_train, x_test = dx[train_index], dx[test_index]
            y_train, y_test = dy[train_index], dy[test_index]
            clf = GradientBoostingRegressor(**p)
            clf.fit(x_train, y_train)
            pred = clf.predict(x_test)
            a = log_loss(y_test, pred, 1e-15)
            print a
            total.append(copy.copy(a))
        print "best score:" , sum(total)/len(total)
        print p


def xgbost(x,y,targetx):
    clf_xgb = XGBClassifier(n_estimators=1000,max_depth=6, learning_rate=0.0075,subsample=0.7,colsample_bytree=0.7,seed=4)
    clf_xgb.fit(x,y)
    return clf_xgb.predict_proba(targetx)[:,1]


if __name__=="__main__":

    data = pd.read_csv('d.csv')
    train_data = pd.DataFrame()
    features = [key for key in data.keys() if key != 'shot_made_flag']
    for f in features:
        data[f] = data[f].astype(int)

        train_data = pd.concat([train_data, data.loc[:,[f]]], axis=1)
    mask = data['shot_made_flag'].isnull()
    x = train_data[~mask]
    y = data.shot_made_flag[~mask]
    targetx = train_data[mask]

    targety = gbdt(x,y,targetx)
    #targety = gbdtRegressor(x,y,targetx)
    #targety = xgbost(x,y,targetx)
    df = pd.read_csv('../data.csv')
    mask2 = df['shot_made_flag'].isnull()
    target_id = df[mask]["shot_id"]
    submission = pd.DataFrame({"shot_id":target_id, "shot_made_flag":targety})
    submission.to_csv('a.csv',index=False)
