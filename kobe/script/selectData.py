
import csv

train = list(); test = list()
ttrain = list(); validation = list()
with open("../data.csv") as f:
    reader = csv.reader(f)

    reader.next()
    for row in reader:
        temp = row[14]
        row[14] = row[0]
        row[0] = temp
        if row[0] == '':
            test.append(row)
        else:
            train.append(row)
            if len(train)%8==0:
                validation.append(row)
            else:
                ttrain.append(row)
with open('../data/train.csv', 'w') as f:
    w = csv.writer(f)
    w.writerows(train)

with open('../data/test.csv', 'w') as f:
    w = csv.writer(f)
    w.writerows(test)

length = len(train)
print length

with open('../data/ttrain.csv', 'w') as f:
    w = csv.writer(f)
    w.writerows(ttrain)

with open('../data/validation.csv', 'w') as f:
    w = csv.writer(f)
    w.writerows(validation)
            

