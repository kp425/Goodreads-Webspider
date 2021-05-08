import scrapy
import re
from javguru.items import Actress, Video

class Spider(scrapy.Spider):

    name = 'actress1'
    # def start_requests(self):
        #urls = ['https://jav.guru/actress/imai-kaho/']
        # urls = ['https://jav.guru/actress/niiyama-kaede/',
        #             'https://jav.guru/actress/mitoma-umi/']
        # for url in urls:
        #     name = url.split('/')[-2]
        #     item = Actress(name=name, link='', total_vids='', videos = [])
        #     yield scrapy.Request(url, meta = {'actress':item}, 
        #                                 callback = self.actress_videos)

    start_urls = ['https://jav.guru/jav-actress-list/']
    # start_urls = ['https://jav.guru/actress/julia/']


    def parse(self, response):
        
        response = response.xpath("//div[@class='wp-content']")
        response = response.xpath(".//li[contains(@class,'cat-item')]")
        
        names = response.xpath(".//a/text()").getall()
        links = response.xpath(".//a/@href").getall()
        total_vids = response.xpath("./text()").getall()
        start = 0
        end = 2
        for name, link, vids in zip(names[start:end], links[start:end], total_vids[start:end]):
            item = Actress(name='', link='', total_vids='', videos = [])
            item['name'] = name
            item['link'] = link
            item['total_vids'] = vids
            yield scrapy.Request(item['link'], meta={'actress':item}, 
                                        callback=self.actress_videos)
            



    
    def actress_videos(self, response):
       
        actress_item = response.meta['actress']

        response = response.xpath("//div[@class='blog-list-items']")
        response = response.xpath(".//div[contains(@class,'entry animation')]")
        info_bar = response.xpath(".//div[@class='theme']")

        for i in info_bar:
            item = Video(title='',link='',
                    views='',tags=[],date='')
            item['title'] = i.xpath(".//h2/a/@title").get()
            item['link'] =  i.xpath(".//h2/a/@href").get()
            item['views'] = i.xpath(".//p[@class='javstats']//text()").get()
            item['tags'] =  i.xpath(".//p[@class='tags']//a//text()").getall()
            item['date'] =  i.xpath(".//p[@class='date']//text()").get()
            # print(item['title'])
            # print(item['link'])
            # print(item['views'])
            # print(item['tags'])
            # print(item['date'])
            
            actress_item['videos'].append(item)

        next_page = response.xpath("//div[@id='postnav']//a[@class='page larger']/@href").get()

        if next_page != None:
            yield scrapy.Request(next_page, meta={'actress': actress_item},
                                    callback=self.actress_videos)
        else:
            yield actress_item
        

        
        
 

            

        
        # title = info_bar.xpath(".//h2/a/@title")
        # link = info_bar.xpath(".//h2/a/@href")
        # views = info_bar.xpath(".//p[@class='javstats']//text()")
        # tags = info_bar.xpath(".//p[@class='tags']//a//text()")
        # date = info_bar.xpath(".//p[@class='date']//text()")

        # for i in zip(title, link, views, tags, date):
        #     print(i[3].getall())

        # print(tags.getall())

        # return title, link, views, tags, date

    # #in actress page
    # def get_nextpage(self, response):
    #     #return a lot of pages, but get only the first one
    #     next_page = response.xpath("//div[@id='postnav']//a[@class='page larger']/@href").get()

    #     if next_page != None:
    #         yield scrapy.Request(next_page, callback=self.actress_videos)
    

    def logger_cb(self, response):
        self.logger.info("Visited %s", response.url)


