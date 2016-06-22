
import csv

train = list(); test = list()
ttrain = list(); validation = list()
descript = list()
with open("../data.csv") as f, open('../data/all.csv', 'w') as wf:
    reader = csv.reader(f)
    writer = csv.writer(wf)
    counter = 0
    for row in reader:

        temp = row[14]
        row[14] = row[0]
        row[0] = temp

        if counter == 0:
            descript = row
            counter+=1
            writer.writerow(row)
            continue

        if row[0] == '':
            row[0] = 0
            test.append(row)
        else:
            train.append(row)
            if len(train)%8==0:
                validation.append(row)
            else:
                ttrain.append(row)

        writer.writerow(row)
with open('../data/train.csv', 'w') as f:
    w = csv.writer(f)
    w.writerow(descript)
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


