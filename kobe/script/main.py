#!/usr/bin/env python
# encoding: utf-8
from Feature import Feature
from AnalysisData import Analysis
from Tp import TrainAndPredict

def offLine():

    analysis = Analysis('../data/train.csv')
    analysis.dataDistribution()
    feature = Feature()
    feature.newFeature()
    feature.categoryNumerical('../data/ttrain.csv', '../data/validation.csv')

    #train = TrainAndPredict('../data/rf/train.csv', '../data/rf/validation.csv', '../data/validation.csv')
    train = TrainAndPredict('../data/rf/one_hot_train.csv', '../data/rf/one_hot_validation.csv', '../data/validation.csv')
    #train.gbdtClassifier()
    #train.gbdtRegressor()
    #train.linearRegression()
    #train.logisticRegression()
    #train.svmSVC()
    train.xgbost()


def onLine():
    analysis = Analysis('../data/all.csv')
    analysis.dataDistribution()
    feature = Feature()
    feature.newFeature()
    feature.categoryNumerical('../data/train.csv', '../data/test.csv')
    #train = TrainAndPredict('../data/rf/train.csv', '../data/rf/validation.csv', '../data/test.csv')
    train = TrainAndPredict('../data/rf/one_hot_train.csv', '../data/rf/one_hot_validation.csv', '../data/test.csv')
    #train.gbdtClassifier()
    #train.gbdtRegressor()
    #train.linearRegression()
    #train.logisticRegression()
    train.xgbost()
    #train.svmSVC()

if __name__=='__main__':
    offLine()
    onLine()


