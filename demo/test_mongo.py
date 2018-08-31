from pymongo import MongoClient
import json
import time

start_time = time.clock()


connection = MongoClient('192.168.3.192', 27017)
db = connection['moli_word']
words = db['words']

# for w in words.find():
#     print w['word']
#

catesGroup = dict()
wordAna = dict()
wordcollection = words.find()
wordslib =[]
for w in wordcollection:
    wordslib.append(w)



def checkWordCate(word):
    for wordlib in wordslib:
        if word.lower() == wordlib['word'].lower():
            if wordlib['category'] in catesGroup:
                catesGroup[wordlib['category']] += 1
            else:
                catesGroup[wordlib['category']] = 0
            # if x['word'] in wordAna:
            #     wordAna[x['word']] += 1
            # else:
            #     wordAna[x['word']] = 0


def enumWords(swords):
    for sw in swords:
        print 'search word:' + sw
        checkWordCate(sw)


with open('./b.txt') as f:
    for line in f:
        tl = line.strip();
        if len(tl) != 0:
            sentenceWords = tl.split(' ')
            enumWords(sentenceWords)


catesGroup = sorted(catesGroup.items(),key=lambda a:a[1],reverse=True)
print json.dumps(catesGroup, indent=4)
print time.clock() - start_time, "seconds"