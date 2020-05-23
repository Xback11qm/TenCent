# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from .settings import *


class TencentPipeline(object):
    def process_item(self, item, spider):
        print(dict(item))
        return item

class TencentMysqlPipeline(object):
    def open_spider(self,spider):
        self.db=pymysql.connect(MYSQL_HOST,MYSQL_USER,MYSQL_PWD,MYSQL_DB,charset=CHARSET)
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        ins = 'insert into tencenttab values(%s,%s,%s,%s,%s,%s)'
        job_li = [
            item['job_name'],
            item['job_type'],
            item['job_duty'],
            item['job_require'],
            item['job_address'],
            item['job_time']
        ]
        self.cursor.execute(ins, job_li)
        self.db.commit()

        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()