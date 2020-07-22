# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, Compose, Join

def mysplit(info):
    return info.split('/')


class FtxSchoolItem(scrapy.Item):
    # define the fields for your item here like
    region_name = scrapy.Field(output_processor=Join())
    school_name = scrapy.Field(output_processor=Join())
    school_address = scrapy.Field(output_processor=Join())
    school_type = scrapy.Field(output_processor=Join())
    school_level = scrapy.Field(output_processor=Join())
    public_private = scrapy.Field(output_processor=Join())
    aver_price_m2 = scrapy.Field(output_processor=Join())
    xiaoqushu = scrapy.Field(output_processor=Join())
    xiaoqu = scrapy.Field(output_processor=Join())
    school_advantage = scrapy.Field(output_processor=Join())
    house_onsale = scrapy.Field(output_processor=Join())


class MysipderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
