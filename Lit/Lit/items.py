# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AuthorItem(scrapy.Item):
    author = scrapy.Field()
    links = scrapy.Field()
    dates = scrapy.Field()
    

class StoryItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    desc = scrapy.Field()
    words = scrapy.Field()
    rating = scrapy.Field()
    views = scrapy.Field()
    fav = scrapy.Field()
    comments = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    category = scrapy.Field()
    author = scrapy.Field()
    author_stories = scrapy.Field()
    author_followers = scrapy.Field()

    def __str__(self):
        return ""
        # return self.__dict__.pop('content', None)