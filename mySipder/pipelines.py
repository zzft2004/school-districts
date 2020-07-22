# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class Pipeline_csv(object):
    def open_spider(self, spider):
        # newline可以去掉csv的空行
        self.f = open('school.csv', 'w', encoding='utf-8-sig', newline='')
        self.fw = csv.writer(self.f)
        self.keys = ['region_name', 'school_name', 'school_type', 'school_level',
                    'public_private', 'aver_price_m2', 'school_address', 'xiaoqushu',
                    'xiaoqu', 'school_advantage', 'house_onsale']
        self.fw.writerow(self.keys)

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, sipder):
        rowinfo = [item.get(key, '') for key in self.keys]
        self.fw.writerow(rowinfo)
        return item


class MysipderPipeline:
    def process_item(self, item, spider):
        return item
