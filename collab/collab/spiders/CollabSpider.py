# from scrapy.xpath import Selector
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy import log
from collab.items import User, Project
from os import path
from collab.parser.HtmlParser import HtmlParser
import os
import urllib
import string
from bs4 import UnicodeDammit
from collab.db import MongoDBClient

class CollabspiderSpider(CrawlSpider):
    name = 'CollabSpider'
    allowed_domains = ['localhost','localhost:8000','http://localhost:8000']
    start_urls = [ "http://localhost:8000/project/" ,"http://localhost:8000/person/"]

    rules = (
        # Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def __init__(self):
        pass

    def parse_elem(self, response):
        response = response.replace(url=HtmlParser.remove_url_parameter(response.url))

        hxs = Selector(response)
        project={
            'name'         : '//*[@id="search_headline"]/text()',
            'description'  : '//*[@id="project_info"]/div[1]/div[7]/h2[2]/text()',
            'needs'        : '//*[@id="seeking"]/li/strong/text()',
            'contributors' : '//*[@id="contributors"]/ul/li/span/span/a[1]/text()',
            'groups'       : '//*[@id="project_group_list"]/ul/li/a[contains(@href,"groups")]/text()',
            'skills_owned' : '//*[@id="contributors"]/ul/li/span/span/a[2]/text()',
            'locations'    : '//*[@id="contributors"]/ul/li/span/span/a[contains(@href,"location")]/text()',
            'followers'    : '//*[@id="project_info"]/div[2]/center/h4/strong/text()',
            'owner'        : '//*[@id="project_info"]/div[1]/div[5]/h2[1]/a/text()',
            'tags'         : '//*[@id="project_info"]/div[2]/div[11]/ul/li/a/text()',
            'media'        : '//*[@id="project_images"]/div[1]/center/img/@src',
            'goals'        : '//*[@id="project_goals"]/li/h4/text()'
        }

        p=Project()
        p['_id']=response.url
        p['name']=hxs.xpath(project['name']).extract()[0]
        p['url']=response.url
        p['description']=''.join(hxs.xpath(project['description']).extract()).replace('\n','')
        p['needs']=hxs.xpath(project['needs']).extract()
        p['contributors']=hxs.xpath(project['contributors']).extract()
        p['groups']=hxs.xpath(project['groups']).extract()
        p['skills_owned']=hxs.xpath(project['skills_owned']).extract()
        p['locations']=hxs.xpath(project['locations']).extract()
        p['follower_count']=int(hxs.xpath(project['followers']).extract()[0])
        p['owner']=hxs.xpath(project['owner']).extract()[0]
        p['tags']=hxs.xpath(project['tags']).extract()
        p['media']=hxs.xpath(project['media']).extract()
        p['goals']=hxs.xpath(project['goals']).extract()
        yield p





    def parse_user(self, response):
        response = response.replace(url=HtmlParser.remove_url_parameter(response.url))

        hxs = Selector(response)

        user={
            'name'      : '//*[@id="search_headline"]/span/text()',
            'label'     : '//*[@id="profile_head"]/div[3]/h1[2]/a[1]/text()',
            'location'  : '//*[@id="profile_head"]/div[3]/h1[2]/a[2]/text()',
            'skills'    : '//div/div/ul/li/a[contains(@href,"skillz")]/text()',
            'interests' : '//div/div/ul/li/a[contains(@href,"interests")]/text()',
            'education' : '//div/div/ul/li/span/a[contains(@href,"school")]/text()',
            'groups'    : '//div/div/ul/li/a[contains(@href,"groups")]/text()',
            'work'      : '//div/div/ul/li/a[contains(@href,"company")]/text()',
            'avatar'    : '//*[@id="avatar_main_wrapper"]/img/@src'
        }
        u=User()
        u['_id']=response.url
        u['name']=hxs.xpath(user['name']).extract()[0]
        u['url']=response.url
        u['label']=hxs.xpath(user['label']).extract()[0]
        u['location']=hxs.xpath(user['location']).extract()[0]
        u['skills']=hxs.xpath(user['skills']).extract()
        u['interests']=hxs.xpath(user['interests']).extract()
        u['education']=hxs.xpath(user['education']).extract()
        u['groups']=hxs.xpath(user['groups']).extract()
        u['work']=hxs.xpath(user['work']).extract()
        u['avatar']=hxs.xpath(user['avatar']).extract()[0]
        yield u

    def parse(self, response):
        """
        default parse method, rule is not useful now
        """
        # import pdb; pdb.set_trace()
        response = response.replace(url=HtmlParser.remove_url_parameter(response.url))
        hxs = Selector(response)
        # index_level = self.determine_level(response)
        # log.msg("Parse: index level:" + str(index_level))
        directories=False
        import re


        for url in hxs.xpath('/html/body/ul/li/a/@href').extract():
            # log.msg('yield process, url:' + url)
            # print(url)
            if re.match(".*/project/.*", response.url):
                print("PROJECT",response.url,url)

                if re.match(".*/[0-9]{1,4}/", response.url) and re.match(".*\.html", url):
                    # print("Parsing TO: "+response.url+'/'+url)
                    yield Request(response.url+url, callback=self.parse_elem)

                elif re.match("[0-9]{1,4}/", url):
                    # print("Continuing TO: http://localhost:8000/project/"+url)

                    yield Request("http://localhost:8000/project/"+url, callback=self.parse)



            else:
                yield Request("http://localhost:8000/person/"+url, callback=self.parse_user)

        # if index_level in [1, 2, 3, 4]:
        #     self.save_to_file_system(index_level, response)
        #     relative_urls = self.get_follow_links(index_level, hxs)
        #     if relative_urls is not None:
        #         for url in relative_urls:
        #             log.msg('yield process, url:' + url)
        #             yield Request(url, callback=self.parse_school)



        # elif index_level == 5:
        #     personProfile = HtmlParser.extract_person_profile(hxs)
        #     collab_id = self.get_collab_id(response.url)
        #     collab_id = UnicodeDammit(urllib.unquote_plus(collab_id)).markup
        #     if collab_id:
        #         personProfile['_id'] = collab_id
        #         personProfile['url'] = UnicodeDammit(response.url).markup
        #         yield personProfile

    def determine_level(self, response):
        """
        determine the index level of current response, so we can decide wether to continue crawl or not.
        level 1: people/[a-z].html
        level 2: people/[A-Z][\d+].html
        level 3: people/[a-zA-Z0-9-]+.html
        level 4: search page, pub/dir/.+
        level 5: profile page
        """
        import re
        url = response.url
        if re.match(".+/[a-zA-Z0-9]*\.html", url):
            return 1
        elif re.match(".+/[A-Z]\d+.html", url):
            return 2
        elif re.match(".+/people-[a-zA-Z0-9-]+", url):
            return 3
        elif re.match(".+/pub/dir/.+", url):
            return 4
        elif re.match(".+/search/._", url):
            return 4
        elif re.match(".+/pub/.+", url):
            return 5
        log.msg("Crawl cannot determine the url's level: " + url)
        return None

    def save_to_file_system(self, level, response):
        """
        save the response to related folder
        """
        if level in [1, 2, 3, 4, 5]:
            fileName = self.get_clean_file_name(level, response)
            if fileName is None:
                return

            fn = path.join(self.settings["DOWNLOAD_FILE_FOLDER"], str(level), fileName)
            self.create_path_if_not_exist(fn)
            if not path.exists(fn):
                with open(fn, "w") as f:
                    f.write(response.body)

    def get_clean_file_name(self, level, response):
        """
        generate unique collab id, now use the url
        """
        url = response.url
        if level in [1, 2, 3]:
            return url.split("/")[-1]

        collab_id = self.get_collab_id(url)
        if collab_id:
            return collab_id
        return None

    def get_collab_id(self, url):
        find_index = url.find("localhost:8000/")
        if find_index >= 0:
            log.msg(url, url[find_index + 15:].replace('/', '-'))
            return url[find_index + 15:].replace('/', '-')
        return None

    def get_follow_links(self, level, hxs):
        if level in [1, 2, 3]:
            relative_urls = hxs.xpath("//html/body/ul/li/a/@href").extract()
            relative_urls = ["http://localhost:8000" + x for x in relative_urls]
            return relative_urls
        elif level == 4:
            relative_urls = relative_urls = hxs.xpath("//html/body/ul/li/a/@href").extract()
            relative_urls = ["http://localhost:8000" + x for x in relative_urls]
            return relative_urls

    def create_path_if_not_exist(self, filePath):
        if not path.exists(path.dirname(filePath)):
            os.makedirs(path.dirname(filePath))

