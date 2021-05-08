import scrapy
import re
from javguru.items import Actress, Video

class JavSpider(scrapy.Spider):

    name = 'actress'
    
    def __init__(self, url):
        super(JavSpider, self).__init__()
        self.urls = [url]

    def start_requests(self):
        # urls = ['https://jav.guru/actress/hatano-yui/',
        #         'https://jav.guru/actress/imai-kaho/',
        #         'https://jav.guru/actress/hazuki-mion/']
        # urls = ['https://jav.guru/actress/hazuki-mion/']
        # urls = ['https://jav.guru/studio/jul/']
        # urls = ['https://jav.guru/actress/hatano-yui/']
        # urls = ['https://jav.guru/actress/imai-kaho/']
        # urls = ['https://jav.guru/studio/jul/']
        # urls = ['https://jav.guru/tag/anal-sex/']

        for url in self.urls:
            name = url.split('/')[-2]
            item = Actress(name=name, link=url, total_vids=0, videos = [])
            yield scrapy.Request(url, meta = {'actress':item}, 
                                        callback = self.get_actress_videos)


    def get_actress_videos(self, response):
        
        actress_item = response.meta['actress']

        response = response.xpath("//div[@id='primary']//div[@class='inside-article']")

        for i in response:

            item = Video(title='',link='',
                    views='',tags=[],date='')
            item['title'] = i.xpath(".//h2/a/@title").get()
            item['link'] =  i.xpath(".//h2/a/@href").get()
            item['views'] = i.xpath(".//div[@class='javstats']//text()").get()
            item['tags'] =  i.xpath(".//p[@class='tags']//a//text()").getall()
            item['date'] =  i.xpath(".//div[@class='date']//text()").get()
            # print(item['title'])
            # print(item['link'])
            # print(item['views'])
            # print(item['tags'])
            # print(item['date'])
            
            actress_item['videos'].append(item)

       
        next_page = response.xpath("//div[@class='wp-pagenavi']//a[@class='page larger']/@href").get()
   
        if next_page != None:
            yield scrapy.Request(next_page, meta={'actress': actress_item},
                                    callback=self.get_actress_videos)
        else:
            yield actress_item
        


    def logger_cb(self, response):
        self.logger.info("Visited %s", response.url)


