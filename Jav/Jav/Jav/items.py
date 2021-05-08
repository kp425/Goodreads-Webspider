# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Actress(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    total_vids = scrapy.Field()
    videos = scrapy.Field()
    # def __str__(self):
    #     return ""

class Video(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    views = scrapy.Field()
    tags = scrapy.Field()
    date = scrapy.Field()

class actress_info_sql(scrapy.Item):
    name = scrapy.Field()   #assuming name is unique
    link = scrapy.Field()
    total_vids = scrapy.Field()

class actress_videos_sql(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    views = scrapy.Field()
    tags = scrapy.Field()
    date = scrapy.Field()