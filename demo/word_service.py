# -*- coding: utf-8 -*-
from pymongo import MongoClient


class wordService():

    def openMongo(self):
        connection = MongoClient('localhost', 27017)
        self.db = connection['moli_word']
        self.categories = self.db['categories']
        self.words = self.db['words']
        if self.words is not None:
            self.words.remove()

    # define the fields for your item here like:
    def getMainCategories(self):
        for cate in self.categories.find():

            # level2
            if 'hasChild' in cate:
                if cate['hasChild'] == 0:
                    yield cate
            else:  # level3
                if cate['parent'] != 0:
                    yield cate

    def syncWords(self):
        for cate in self.getMainCategories():
            print cate['name']
            currentCate = self.db[cate['key']]
            for w in currentCate.find():
                print w['word']
                self.words.insert(dict({
                    'word': w['word'],
                    'category': w['category']
                }))
