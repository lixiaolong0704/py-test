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
    wordCount = Field()
    courseCount = Field()
    classId = Field()
    key = Field()
    parent = Field()
    tag = Field()
    hasChild = Field()


class WordItem(Item):
    word = Field()

    en = Field()  # 英音
    am = Field()  # 美音
    en_video = Field()
    am_video = Field()


    comment = Field()

    category = Field()
    courseId = Field()
    _id = Field()
    version = Field()

    # 变形 object
    change = Field()
