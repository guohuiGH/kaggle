#!/usr/bin/env python
# encoding: utf-8
import csv
class Analysis():
    def __init__(self,path):
        self.path = path
        pass
    def dataDistribution(self):
        data = dict()
        rows = list()
        cloumns = list()
        with open(self.path) as rf:
            reader = csv.reader(rf)
            rows = [row for row in reader]
            for i in range(0,len(rows[0])):
                cloumns.append([row[i] for row in rows])
        with open('../data/cloumns','w') as wf:
            writer = csv.writer(wf)
            writer.writerows(cloumns)
            #for i in range(0, len(cloumns)):
            #    writer.writerow(cloumns[i] + '\n')






if __name__=="__main__":
    analysis = Analysis('../data/train.csv')
    analysis.dataDistribution()
