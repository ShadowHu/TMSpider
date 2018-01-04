# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class TMItem(scrapy.Item):
    # define the fields for your item here like:
    title = Field()
    price = Field()
    saleMonth = Field()
    cateid = Field()
    itemUrl = Field()
    pid = Field()
    brand = Field()
    categories = Field()
    images = Field()
    price = Field()
    shop = Field()
    description = Field()
    itemDetail = Field()

