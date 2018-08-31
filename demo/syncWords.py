# -*- coding: utf-8 -*-
import requests
import threading
import time
import re
import sys
# r = requests.get('https://api.github.com/events')
# print(r.text)
from word_service import  *
try:
    # sleeper()
    # print '中文'.decode('utf8')
    # print sys.getdefaultencoding()
    # print re.sub('[^\d]*', '', u'\u8bfe\u7a0b\u6570 226')
    #
    # r = requests.get('http://www.iciba.com/comment')
    # print(r.text)
    _wordservice = wordService()
    _wordservice.openMongo()
    _wordservice.syncWords()





except KeyboardInterrupt:
    print('\n\nKeyboard exception received. Exiting.')
    exit()
