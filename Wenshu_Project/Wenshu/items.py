# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WenshuCaseItem(scrapy.Item):
    # define the fields for your item here like:
    court = scrapy.Field()
    content = scrapy.Field()
    type = scrapy.Field()
    # casereason = scrapy.Field()
    judgedate = scrapy.Field()
    # caseparty = scrapy.Field()
    procedure = scrapy.Field()
    number = scrapy.Field()
    nopublicreason = scrapy.Field()
    casedocid = scrapy.Field()
    name = scrapy.Field()
    contenttype = scrapy.Field()
    uploaddate = scrapy.Field()
    doctype = scrapy.Field()
    closemethod = scrapy.Field()
    effectivelevel = scrapy.Field()
