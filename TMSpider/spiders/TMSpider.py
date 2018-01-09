#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-03 19:23:42
# @Author  : ShadowHu (shadow_hu1441@163.com)
# @GitHub  : https://github.com/ShadowHu

import scrapy
from scrapy import Request
from TMSpider.items import TMItem
# from scrapy.loader import ItemLoader
import re, json
from TMSpider. settings import CATE_FILE


# CATE_URL = "https://list.tmall.com/search_product.htm?start_price={}&end_price={}&search_condition=55&cat=50105688&sort=rq&style=l&from=sn_1_rightnav&active=1&shopType=any#J_crumbs"
# ITEM_URL = "https://detail.tmall.com/item.htm?id={}"
LIST_URL = "https://list.tmall.com/m/search_items.htm?page_size=60&page_no={}&cat={}"

class TMSpider(scrapy.Spider):
	name = 'tm'
	# start_urls = ['https://food.tmall.com/']
	with open(CATE_FILE) as catefile:
		start_urls = [LIST_URL.format(1, x) for x in catefile]

	def parse(self, response):
		js = json.loads(response.body_as_unicode())
		maxpage = js["total_page"]
		for itemjs in js['item']:
			item = TMItem()
			item['title'] = itemjs['title']
			item['cateid'] = itemjs['cat_id']
			item['commentNum'] = itemjs['comment_num']
			item['pid'] = itemjs['item_id']
			item['shop'] = itemjs['shop_name']
			item['price'] = itemjs['price']
			item['originalPrice'] = itemjs['original_price']
			item['skuid'] = itemjs['sku_id']
			item['itemUrl'] = itemjs['url']
			item['rate'] = itemjs['user_rate']['description_match']
			item['soldMonth'] = itemjs['sold']
			yield item

		for p in range(2, maxpage+1):
			yield Request(re.sub('page_no=\d+', 'page_no='+str(p), response.url), callback=self.parse)
