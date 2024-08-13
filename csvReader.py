import csv

def printT(docs, fields='', limit=10):
    cnt = 0
    if docs[0]:
        ks = ''
        for k in fields if fields else docs[0].keys():
            ks += k + ','
        print(ks)
    for r in docs:
         if cnt > limit:
            break
         str = ''
         for f in fields if fields else docs[0].keys():
             str += r[f] + ','
         print(str)
         cnt += 1
 
def load(csvFile, encoding='UTF-8', newline='', delimiter=','):
    docs = []
    with open(csvFile, encoding=encoding, newline=newline) as csvf:
        rows = csv.reader(csvf, delimiter=delimiter)
        for row in rows:
            docs.append(row);
    return docs
