scrapy-collab
===============

### Run

`scrapy crawl CollabSpider`


### Fields

Project:  

name,url,description,needs,contributors,groups,skills_owned,locations,follower_count,owner,tags,media,goals

User:  

name,url,label,location,skills,interests,education,groups,work,avatar

### CSV Export 
 
Projects

`mongoexport -d "scrapy" -c "projects" --type=csv --fields name,url,description,needs,contributors,groups,skills_owned,locations,follower_count,owner,tags,media,goals >projects.csv`

Users

`mongoexport -d "scrapy" -c "userz" --type=csv --fields name,url,label,location,skills,interests,education,groups,work,avatar > userz.csv`


Using Scrapy to get Collab's person public profile.

### feature
* Get all **public** profile
* Using Scrapy
* Enable auto throttle
* Enable naive proxy providing
* Agent rotating
* Support Unicode
* Using MongoDB as Backend
* ...


### Dependency
* Scrapy == 0.20
* pymongo 
* BeautifulSoup4, UnicodeDammit


### usage
	1. start a MongoDB instance, `mongod`
	2. run the crawler, `scrapy crawl CollabSpider`

you may found `Rakefile` helpful.


### configuration
MongoDB setting ang other things in `settings.py`. 
