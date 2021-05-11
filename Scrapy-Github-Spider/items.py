# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
      username = scrapy.Field()
      name = scrapy.Field()
      followers = scrapy.Field()
      follows = scrapy.Field()
      stars = scrapy.Field()
      userbio = scrapy.Field()
      repo_count = scrapy.Field()
      pp = scrapy.Field()
      repos = scrapy.Field()
