# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CollabItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class User(Item):
    """docstring for User"""
    _id = Field()
    url        = Field()
    name       = Field()
    label      = Field()
    location   = Field()
    skills     = Field()
    interests  = Field()
    education  = Field()
    groups     = Field()
    work       = Field()
    avatar     = Field()
    dtype      = 'user'

class Project(Item):
    """docstring for Project"""
    _id = Field()
    name           = Field()
    url            = Field()
    description    = Field()
    needs          = Field()
    contributors   = Field()
    groups         = Field()
    skills_owned   = Field()
    locations      = Field()
    follower_count = Field()
    owner          = Field()
    tags           = Field()
    media          = Field()
    goals          = Field()
    dtype          = 'project'
        

class PersonProfileItem(Item):
    _id = Field()
    url = Field()
    name = Field()
    also_view = Field()
    education = Field()
    locality = Field()
    industry = Field()
    summary = Field()
    specilities = Field()
    skills = Field()
    interests = Field()
    group = Field()
    honors = Field()
    education = Field()
    experience = Field()
    overview_html = Field()
    homepage = Field()
    
