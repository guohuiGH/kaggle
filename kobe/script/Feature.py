#!/usr/bin/env python
# encoding: utf-8
import csv
import math
from sklearn.preprocessing import OneHotEncoder
class Feature():
    def __init__(self):
        self.path = '../data/cloumns'
        self.update_path = '../data/new_cloumns'
        self.Y = list()
        pass

    def writeOneHotFile(self,enc, read_file, write_file):
        with open(read_file) as rf, open(write_file, 'w') as wf:
            reader = csv.reader(rf)
            writer = csv.writer(wf)
            temp = list()
            for row in reader:
                for i in range(0,len(row)):
                    row[i] = int(row[i])
                temp.append(row)

            w = enc.transform(temp).toarray()
            #writer.writerows(w)
            result = list()
            for ar in w:
                temp = list(ar[0:len(ar)-2])
                temp.append(ar[len(ar)-1])
                result.append(temp)
            writer.writerows(result)


    def categoryNumerical(self,train_path, test_path):
        cloumns = list()
        with open(self.update_path) as rf:
            reader = csv.reader(rf)
            for row in reader:
                cloumns.append(row)
        #self.Y = cloumns[0][1:]
        self.Y = cloumns[10][1:]
        new_cloumns = list()
        lc = len(cloumns)-1
        index = cloumns[lc][1:]

        #valid_cloumn = range(1,4)
        #valid_cloumn.extend(range(8,21))
        #valid_cloumn.extend(range(22,24))
        valid_cloumn = range(0,10)
        valid_cloumn.extend(range(11,17))
        for i in valid_cloumn:
            row = cloumns[i]
            data = dict()
            line = list()
            counter = 1
            for j in range(1,len(row)):
                if row[j] not in data:
                    data[row[j]] = counter
                    counter += 1
                line.append(data[row[j]])
            new_cloumns.append(line)
        new_cloumns.append(self.Y)

        all_data = dict()
        for i in range(0,len(index)):
            all_data[index[i]] = [row[i] for row in new_cloumns]
        #self.writeFile(all_data, '../data/ttrain.csv', '../data/rf/train.csv')
        #self.writeFile(all_data, '../data/validation.csv', '../data/rf/validation.csv')
        self.writeFile(all_data, train_path, '../data/rf/train.csv')
        self.writeFile(all_data, test_path, '../data/rf/validation.csv')
        self.oneHot(all_data)

    def writeFile(self,all_data, readPath, writerPath):
        with open(readPath) as rf , open(writerPath, 'w') as wf:
            reader = csv.reader(rf)
            writer = csv.writer(wf)
            for row in reader:
                if row[len(row)-1] in all_data:
                    writer.writerow(all_data[row[len(row)-1]])

    def oneHot(self, all_data):
        x = [all_data[key] for key in all_data]
        print x[0]
        enc = OneHotEncoder()
        enc.fit(x)
        self.writeOneHotFile(enc, '../data/rf/train.csv', '../data/rf/one_hot_train.csv')
        self.writeOneHotFile(enc, '../data/rf/validation.csv', '../data/rf/one_hot_validation.csv')

    def newFeature(self):
        left_data = dict()
        drop_cloumn = ['loc_x','loc_y','game_event_id', 'game_id', 'lat', 'lon', 'team_id', 'team_name', 'minutes_remaining', 'seconds_remaining']
        new_cloumn = ['left_time','type','action_type','combined_shot_type','playoffs', 'season','shot_distance', 'shot_type', 'shot_zone','game_date','matchup']
        with open(self.path) as rf:
            reader = csv.reader(rf)
            for row in reader:
                left_data[row[0]] = row[1:]
        left_time = list();last_moment = list()
        for i in range(0,len(left_data['minutes_remaining'])):
            t = int(left_data['minutes_remaining'][i])*60 + int(left_data['seconds_remaining'][i])

            left_time.append(str(int(math.sqrt(t))))
            if t < 60:
                last_moment.append('1')
            else:
                last_moment.append('0')
        left_data['left_time'] = left_time; left_data['last_moment'] = last_moment

        for i in range(0,len(left_data['matchup'])):
            if left_data['matchup'][i].count('@') == 1:
                left_data['matchup'][i] = '1'
            else:
                left_data['matchup'][i] = '0'

        new_type = list()
        for i in range(0, len(left_data['action_type'])):
            new_type.append(left_data['action_type'][i] + left_data['combined_shot_type'][i])
        left_data['new_type'] = new_type

        precision = dict()
        for i in range(0, len(left_data['game_event_id'])):
            gei = left_data['game_event_id'][i]
            if gei not in precision:
                precision[gei] = [0,0,0]
            shot = left_data['shot_made_flag'][i]

            if shot == '1':

                precision[gei][1] +=1
            else:
                precision[gei][0] +=1
        for key in precision:
            precision[key][2] = 1.0*precision[key][1]/(1.0*(precision[key][0] + precision[key][1]))
        pre = list()
        for i in range(0, len(left_data['game_event_id'])):
            pre.append(str(int(precision[left_data['game_event_id'][i]][2]*50)))
        left_data['precision'] = pre


        with open(self.update_path, 'w+') as wf:
            writer = csv.writer(wf)
            for key in left_data.keys():
                if key not in drop_cloumn:
                    s = [key]; s.extend(left_data[key])
                    writer.writerow(s)



if __name__=="__main__":
    feature = Feature()
    feature.newFeature()
    #feature.categoryNumerical('../data/ttrain.csv', '../data/validation.csv')
