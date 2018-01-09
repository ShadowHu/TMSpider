# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from TMSpider import settings
import time
import logging
import sys

logger = logging.getLogger()

class TmspiderPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8')
        self.cursor = self.connect.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

    def process_item(self, item, spider):
        sql = '''INSERT INTO TMTest (itemUrl, pid, insertTime, title, cateid, soldMonth, shop, rate, price, originalPrice, commentNum, skuid) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");''' % \
        (item['itemUrl'], 
        item['pid'], 
        int(time.time()), 
        self.connect.escape(item['title']), 
        item['cateid'], 
        item['soldMonth'], 
        self.connect.escape(item['shop']), 
        item['rate'], 
        item['price'], 
        item['originalPrice'], 
        item['commentNum'], 
        item['skuid'], 
        )
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except pymysql.err.IntegrityError:
            pass
        except Exception as err:
            # print(sql)
            # self.connect.rollback()
            self.cursor.close()
            self.connect.close()
            logging.log(logging.ERROR, err)
            sys.exit("SHUT DOWN EVERYTHING!")
        else:
            logger.info('Insert successful')
            return item