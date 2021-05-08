import scrapy
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from .spiders import AuthorSpider, StorySpider
from .config import app_config
import os
import argparse
import pathlib
import tempfile
import shutil


def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--author', type=str,
                        help="pass a url of author \
                              or a textfile containing all author urls")
    group.add_argument('--story', type=str, 
                        help="pass a url of author \
                              or a textfile containing all author urls \
                              or a folder of textfiles full of author_urls")
    parser.add_argument('--dest', type=str)
    parser.add_argument('--nspiders', type=int)
    # parser.add_argument('--save_links', type=str)
    return parser.parse_args()


process = CrawlerProcess(get_project_settings())

def run_story_spider(src=app_config['LINKS_SAVE_PATH'], 
                     nspiders=1):

    def _crawl_when_url(src):
        src_ = [src]
        process.crawl(StorySpider, urls=src_)

    def _crawl_when_textfile(src): 
        src_ = []
        with open(src,'r') as f:
            src_ += f.readlines()
        process.crawl(StorySpider, urls=src_)

    def _crawl_when_textfile_dist(src, nspiders=1):
        src_ = []
        with open(src,'r') as f:
            src_ += f.readlines()
        print(len(src_))
        size_per_chunk = len(src_)//nspiders
        for i in range(0, len(src_), size_per_chunk):
            chunk = src_[i:i+size_per_chunk]
            print(len(chunk))
            process.crawl(StorySpider, urls=chunk)

    def _crawl_when_folder(src): 
        for txtfile in os.listdir(src):
            src_ = []
            txtfile_ = os.path.join(src, txtfile)
            with open(txtfile_,'r') as f:
                src_ += f.readlines()
                process.crawl(StorySpider, urls=src_)
        
    '''
        merges all links and equally distribute-links 
        specified by us. This won't properly log when spider is closed.
        Find a workaround.
    '''

    def _crawl_when_folder_dist(src, nspiders=1):

        src_ = []
        for txtfile in os.listdir(src):
            txtfile_ = os.path.join(src, txtfile)
            with open(txtfile_,'r') as f:
                src_ += f.readlines()
        size_per_chunk = len(src_)//nspiders
        for i in range(0, len(src_), size_per_chunk):
            chunk = src_[i:i+size_per_chunk]
            process.crawl(StorySpider, urls=chunk)
    
    if str(src).startswith("http"):
        _crawl_when_url(src)

    elif os.path.isfile(src):
        if nspiders > 1:
            _crawl_when_textfile_dist(src, nspiders)
        else:
            _crawl_when_textfile(src)
    
    elif os.path.isdir(src):
        if nspiders > 1:
            _crawl_when_folder_dist(src, nspiders)
        else:
            _crawl_when_folder(src)

def run_author_spider(src, dest):

    def _crawl_when_url(src):
        src_ = [src]
        return process.crawl(AuthorSpider, urls=src_)
        
    def _crawl_when_textfile(src): 
        src_ = []
        with open(src,'r') as f:
            src_ += f.readlines()
        return process.crawl(AuthorSpider, urls=src_)
  
    deferred_object = None
    if str(src).startswith("http"):
        deferred_object =  _crawl_when_url(src)
    elif os.path.isfile(src):
        deferred_object = _crawl_when_textfile(src)
    return deferred_object


def download_stories(src, nspiders=1):
    story_deferred = run_story_spider(src, nspiders=nspiders)
    process.start( )

def download_author_stories(src, nspiders=1):
    
    author_deferred = run_author_spider(src, 
                                        app_config["LINKS_SAVE_PATH"])
    author_deferred.addCallback(lambda _ : run_story_spider(app_config["LINKS_SAVE_PATH"],
                                                            nspiders = nspiders))
    process.start()

if __name__ == "__main__":
    
    args = parse_arguments()
    if args.dest:
        app_config['STORIES_SAVE_PATH'] = args.dest

    if (args.nspiders is None) or (args.nspiders<1):
        nspiders = 1
    else:
        nspiders = args.nspiders

    if args.author:
        app_config['INCLUDE_AUTHOR_FOLDER'] = True
        src = args.author
        tmpdir = tempfile.mkdtemp()
        app_config["LINKS_SAVE_PATH"] = tmpdir
        download_author_stories(src, nspiders)
        shutil.rmtree(tmpdir)
    elif args.story:
        src = args.story
        download_stories(src, args.nspiders)

    




    