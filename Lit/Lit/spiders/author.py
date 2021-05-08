import scrapy
import re
from ..items import AuthorItem

class AuthorSpider(scrapy.Spider):
    name = "author"

    custom_settings = {
        'ITEM_PIPELINES': {
            'Literotica.pipelines.AuthorPipeline': 299
        }
    }

    def __init__(self, urls):
        super(AuthorSpider, self).__init__()
        self.urls = urls
       
    def start_requests(self):
        for url in self.urls:
            item = AuthorItem(author='', links=[], dates=[])
            yield scrapy.Request(url, meta = {'author_item':item}, 
                                        callback = self.get_author)
    def get_author(self, response):
        author = response.xpath('//span[@class="unameClick"]//a/text()').get()
        item = response.meta['author_item']
        item['author'] = author
        return self.get_links_n_dates(response)

    def get_links_n_dates(self, response): 
        root = response.xpath('//tr[@class="sl" or @class="root-story r-ott"]')
        links = root.xpath('.//td[contains(@class,"fc")]//a/@href').getall()
        # dates = root.xpath('.//td[@class="dt" or (not(@*) and matches(text(),"\d\d\/\d\d\/\d\d")]//text()').getall()
        # dates = []
        # d = root.xpath('.//td[@class="dt" or not(@*)]').getall()
        # for i in d:
        #     dates.append(re.findall("\d\d\/\d\d\/\d\d" , i))
        
        # print(len(links))
        # print(len(dates))
        # print(dates)
        item = response.meta['author_item']
        item['links'] = links
        # item['dates'] = dates   
        yield item
    
    
 




    
 



