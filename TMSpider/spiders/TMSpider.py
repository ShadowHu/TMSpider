#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-03 19:23:42
# @Author  : ShadowHu (shadow_hu1441@163.com)
# @GitHub  : https://github.com/ShadowHu

import scrapy
from scrapy import Request
from TMSpider.items import TMItem
from scrapy.loader import ItemLoader
import re, json

PAGE_CUT = [
	[0,20,40,60,80,100,150,200,300,500], # jinkou
	[], # xiuxian
	[], # chayin(empty)
	[], # jiu
	[]] # liangyou(empty) 

CATE_URL = "https://list.tmall.com/search_product.htm?start_price={}&end_price={}&search_condition=55&cat=50105688&sort=rq&style=l&from=sn_1_rightnav&active=1&shopType=any#J_crumbs"
ITEM_URL = "https://detail.tmall.com/item.htm?id={}"
LIST_URL = "https://list.tmall.com/m/search_items.htm?page_size=20&page_no={}&q=%B3%C2%BC%AA%CD%FA%B8%A3&type=p&tmhkh5=&from=mallfp..m_1_searchbutton"

class TMSpider(scrapy.Spider):
	name = 'tm'
	# start_urls = ['https://food.tmall.com/']
	start_urls = ["https://list.tmall.com/m/search_items.htm?page_size=20&page_no=1&q=%B3%C2%BC%AA%CD%FA%B8%A3&type=p&tmhkh5=&from=mallfp..m_1_searchbutton"]

	# def parse(self, response):
	# 	nodes = response.xpath('//ul[@class="mui-menu-nav-container"]/li/h4/a/@href')
	# 	nodenum = -1
	# 	for node in nodes:
	# 		nodenum += 1
	# 		url = 'http:' + node.extract() if node.extract()[:4] != 'http' else node.extract()
	# 		yield Request(url, callback=self.parse_allcate, meta={'nodenum':nodenum})

	# def parse_allcate(self, response):
	# 	nodenum = response.meta['nodenum']
	# 	if PAGE_CUT[nodenum] == []:
	# 		pass
	# 	else:
	# 		for p in range(len(PAGE_CUT[nodenum])):
	# 			if p+1 == len(PAGE_CUT[nodenum]):
	# 				url = CATE_URL.format(PAGE_CUT[nodenum][p], '')
	# 			else:
	# 				url = CATE_URL.format(PAGE_CUT[nodenum][p], PAGE_CUT[nodenum][p+1])
	# 			yield Request(url, callback=self.parse_cate)

	def parse(self, response): # All items between a specific distance
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
			yield Request(LIST_URL.format(p), callback=self.parse)

	# def parse_item(self, response):
	# 	item = TMItem()
	# 	itemld = ItemLoader(item=item, response=response)
	# 	itemText = response.body_as_unicode()
	# 	itemDetail = json.loads(re.search(r'{"api".+}', itemText).group(0))
	# 	item['itemDetail'] = itemDetail
	# 	item['title'] = itemDetail['itemDO']['title']
	# 	item['brand'] = itemDetail['itemDO']['brand']
	# 	item['cateid'] = itemDetail['itemDO']['categoryId']
	# 	item['pid'] = itemDetail['itemDO']['itemId']
	# 	print(itemDetail)

