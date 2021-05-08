from multiprocessing import Pool, Process
import os
import lxml.etree
import lxml.html
import requests
import time
import asyncio
import aiohttp
from functools import wraps
import argparse

def timer(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"Total execution time: {time.perf_counter() - start}")
    return _time_it


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()

# fastest avg 7-8s 
@timer
def main_mp(urls, nprocesses=5):
    chunks = []
    chunk_size = len(urls)//nprocesses
    for i in range(0,len(urls),chunk_size):
        chunk = urls[i:i+chunk_size]
        chunks.append(chunk)

    def _main(urls):
        async def __main(urls):
            tasks = []
            async with aiohttp.ClientSession() as session:
                for url in urls:
                    tasks.append(fetch(url, session))
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    get_videoinfo(response)
    
        asyncio.run(__main(urls))

    processes = []
    for chunk in chunks:
        p = Process(target=_main, args=(chunk,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    

# 2nd fastest avg 9-10s
@timer
def main(urls):
    async def __main(urls):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for url in urls:
                tasks.append(fetch(url, session))
            responses = await asyncio.gather(*tasks)
            for response in responses:
                get_videoinfo(response)
    asyncio.run(__main(urls))

    
# worst performance
@timer           
async def main1(urls):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            response = await fetch(url, session)
            get_videoinfo(response)


# Can be any random job
def get_videoinfo(url):
    # response = requests.get(url)
    response = url
    root = lxml.html.fromstring(response)

    title = root.xpath('.//div[@class="data"]//h1/text()')[0]
    tags = root.xpath('.//div[@class="sgeneros"]//a[@rel="tag"]/text()')
    rv = root.xpath('.//div[@class="dt_rating_data"]')[0]
    rating = rv.xpath('.//span[@itemprop="ratingValue"]/text()')[0]
    votes = rv.xpath('.//span[@itemprop="ratingCount"]/text()')[0]

    info = root.xpath('.//div[@id="info1"]')[0]
    try:
        desc = info.xpath('.//div[@class="wp-content"]//p/text()')[0]
    except IndexError:
        desc = ""
    fields = info.xpath('.//div[@class="custom_fields"]//span[@class="valor"]/text()')
    try:
        (title1, _, _, first_airdate, last_airdate, nepisodes, status) = fields
    except ValueError:
        title1 = ""
        print(fields)
    studio = info.xpath('.//div[@class="custom_fields"] \
                        //div[@class="mta_series"]//a[@rel="tag"]//text()')
    
    # print(title1)
    # print(studio)
    # print(fields) 
    # print(desc)
    # print(title)
    # print(tags)
    # print(rating)
    # print(votes)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str)
    args = parser.parse_args()
    url = args.url

    response = requests.get(url)
    root = lxml.html.fromstring(response.content)
    urls = root.xpath('.//ul//li[@class="current-menu-item"]//a/@href')
    
    # multiproc = True

    main_mp(urls, 3)

    
    

   








