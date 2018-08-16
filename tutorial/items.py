# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CategoryItem(Item):
    # define the fields for your item here like:
    # name = Field()
    name = Field()
    wordCount= Field()
    classCount = Field()
    key = Field()
    parent = Field()


class WordItem(Item):
    word = Field()
    am = Field()
    em = Field()
    comment = Field()
    video = Field()
    category = Field()