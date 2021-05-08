# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymongo
import mysql.connector
import datetime
import re
from itemadapter import ItemAdapter


class InitialProcessingPipeline:

    def __process(self, item):

        item['total_vids'] = len(item['videos'])
        for video in item['videos']:
            views = video['views']
            video['views'] = "".join([s for s in views if s.isdigit()])
            #preprocess datetime later
        return item

    def process_item(self, item, spider):
        item = self.__process(item)
        print(item['total_vids'])
        return item

class Sql_Pipeline:
    
    def __init__(self, password, database, host, port):
        self.password = password
        self.database = database
        self.host = host
        self.port = port 

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get('SQL_HOST'),
            database = crawler.settings.get('SQL_DATABASE'),
            port = crawler.settings.get('SQL_PORT'),
            password = crawler.settings.get('SQL_PASSWORD')
        )

    def open_spider(self, spider):
        self.cnx = mysql.connector.connect(password=self.password,
                              host=self.host, port=self.port,
                              database=self.database)
        self.cur = self.cnx.cursor(buffered=True)

    def close_spider(self, spider):
        self.cnx.commit()
        self.cnx.close()

    def __process(self, item):
        item['total_vids'] = int(item['total_vids'])
        for video in item['videos']:
            video['views'] = int(video['views'])
            video['tags'] = '^'.join(video['tags'])
            date_time = datetime.datetime.strptime(video['date'],"%d %b, %y")
            date = str(datetime.datetime.date(date_time))
            video['date'] = date
        return item
    
    def process_item(self, item, spider):

        item = self.__process(item)

        query1 = ("""INSERT INTO actress_info (actress_id, actress, actress_page, total_vids)
                VALUES (MD5(%s),%s,%s,%s)
                ON DUPLICATE KEY UPDATE total_vids = %s""")

        
        self.cur.execute(query1, (item['link'],item['name'], 
                                item['link'], item['total_vids'], 
                                item['total_vids']))
        
        query2 = ("""INSERT INTO video_info (video_id, title, video_link, views, tags, date, actress_id)
                VALUES (MD5(%s),%s,%s,%s,%s,%s,MD5(%s))
                ON DUPLICATE KEY UPDATE views = %s""")
        
        for video in item['videos']:
            row =  (video['link'], video['title'], video['link'], video['views'],video['tags'],video['date'],
                    item['link'], video['views'])
            self.cur.execute(query2, row)


    # def process_item(self, item, spider):

    #     query1 = ("""INSERT INTO actress_info (actress, actress_page, total_vids) 
    #               VALUES (%s, %s, %s)""")
        
    #     # query2 = ("""INSERT INTO video_info (actress, actress_page, title, link, views, tag)
    #     #           VALUES (%s, %s, %s, %s, %s, %s)""")

    #     query2 = ("""INSERT INTO video_info (actress, actress_page, title, link, views, tags) VALUES (%s, %s, %s, %s, %s, %s)""")

        
    #     self.cur.execute(query1, (item['name'], item['link'], item['total_vids']))

    #     for video in item['videos']:
    #         row =  (item['name'], item['link'], 
    #                 video['title'], video['link'], video['views'], 'tagxx'
    #                 # video['tags']
    #                 )
    #         self.cur.execute(query2, row)




class MongoPipeline:

    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_collection=crawler.settings.get('MONGODB_COLLECTION')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection_name = self.mongo_collection

    def close_spider(self, spider):
        self.client.close()

    
    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item



        


