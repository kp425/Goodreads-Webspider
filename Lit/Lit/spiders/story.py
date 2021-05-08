import scrapy
import re
import os
from ..items import StoryItem


class StorySpider(scrapy.Spider):
    name = "story"

    custom_settings = {'ITEM_PIPELINES' : {
        # 'Literotica.pipelines.DebugPipeline': 300,
        'Literotica.pipelines.WordDocPipeline': 301
        }
    }

    def __init__(self, urls):
        super(StorySpider, self).__init__()
        self.urls = urls
    def start_requests(self):
        for url in self.urls:
            item = StoryItem(content=[])
            yield scrapy.Request(url, meta = {'story_item':item}, 
                                        callback = self.get_category)
    
    def get_category(self, response):
        root = response.xpath('//div[@id="BreadCrumbComponent"]')
        category = root.xpath('//a[@class="h_aZ"]//text()').get()
        item = response.meta['story_item']
        item['category'] = category
        return self.get_authorinfo(response)

    def get_authorinfo(self, response):
        root = response.xpath('//div[@class="y_eS"]')
        author = root.xpath('.//a[@class="y_eU"]//text()').get()
        author_stories = root.xpath('.//div[@title="Stories"]//span//text()').get()
        author_followers = root.xpath('.//div[@title="Followers"]//span//text()').get()
        item = response.meta['story_item']
        item['author'] = author
        item['author_stories'] = author_stories
        item['author_followers'] = author_followers
        return self.get_title(response)
 
    def get_title(self, response):
        title = response.xpath('//h1[@class="j_bm headline j_eQ"]//text()').get()
        item = response.meta['story_item']
        item['title'] = title
        return self.get_storyinfo(response)
                                       
    def get_storyinfo(self, response):
        infobox = response.xpath('//div[@class="panel aK_r"]')
        
        desc = infobox.xpath('.//div[@class="aK_B"]//text()').get()
        words = infobox.xpath('.//span[@class="aK_ap"]//text()').getall()
        rvfc = infobox.xpath('.//div[contains(@class,"aT_ci")]')
        
        rating = rvfc.xpath('.//div[@title="Rating"]//span//text()').get()
        views = rvfc.xpath('.//div[@title="Views"]//span//text()').get()
        fav = rvfc.xpath('.//div[@title="Favorites"]//span//text()').get()
        comments = rvfc.xpath('.//div[@title="Comments"]//text()').get()
        # if comments == None:
        #     print(rating, views, fav, comments, response.url)
        

        item = response.meta['story_item']
        item['desc'] = desc
        item['words'] = words[0]
        item['rating'] = rating
        item['views'] = views
        item['fav'] = fav
        item['comments'] = comments
        return self.get_story(response)
        
    def get_story(self, response):
        body = response.xpath('//div[@class="panel article aa_eQ"]//p').getall()
        item = response.meta['story_item']
        item['content'] += body    
        return self.get_nextpage(response)
        
    def get_nextpage(self, response):
        item = response.meta['story_item']
        next_page = response.xpath('//a[@title="Next Page"]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, meta = {'story_item':item}, 
                                           callback = self.get_story) 
        else:
            item = self.get_storytags(response)
            yield item
       

    def get_storytags(self, response):
        tags = response.xpath('//div[@class="e_Q e_ar"]//a/text()').getall()
        item = response.meta['story_item']
        item['tags'] = tags
        return item


# if __name__ == "__main__":
#     urls = "https://www.literotica.com/s/a-mother-and-her-son"
#     process = CrawlerProcess(get_project_settings())
#     process.crawl(StorySpider, urls = urls)
#     process.start()








