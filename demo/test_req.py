# -*- coding: utf-8 -*-
import requests
import threading
import time
import re
import sys
# r = requests.get('https://api.github.com/events')
# print(r.text)
from pymongo import MongoClient


def test():
    print('Before: %s' % time.ctime())
    num = input('How long to wait: ')
    print 'start shit'
    # time.sleep(1000)
    print('After: %s\n' % time.ctime())
    print 'shit'


def sleeper():
    while True:
        # Get user input
        num = raw_input('How long to wait: ')

        # Try to convert it to a float
        try:
            num = float(num)
        except ValueError:
            print('Please enter in a number.\n')
            continue

        # Run our time.sleep() command,
        # and show the before and after time
        print('Before: %s' % time.ctime())
        time.sleep(num)
        print('After: %s\n' % time.ctime())
try:
    # sleeper()
    # print '中文'.decode('utf8')
    # print sys.getdefaultencoding()
    # print re.sub('[^\d]*', '', u'\u8bfe\u7a0b\u6570 226')
    #
    # r = requests.get('http://www.iciba.com/comment')
    # print(r.text)

    connection = MongoClient('localhost', 27017)
    db = connection['moli_word']
    categories = db['categories']
    for cate in categories.find():
        print cate['name']


except KeyboardInterrupt:
    print('\n\nKeyboard exception received. Exiting.')
    exit()
