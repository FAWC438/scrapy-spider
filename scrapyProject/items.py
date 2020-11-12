# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # bupt
    school = scrapy.Field()
    link = scrapy.Field()

    # lianjia
    zone_name = scrapy.Field()
    building_names = scrapy.Field()
    total_price = scrapy.Field()
    area = scrapy.Field()
    price_per_area = scrapy.Field()

    # xuetang
    class_name = scrapy.Field()
    teacher = scrapy.Field()
    school_name = scrapy.Field()
    student_num = scrapy.Field()
