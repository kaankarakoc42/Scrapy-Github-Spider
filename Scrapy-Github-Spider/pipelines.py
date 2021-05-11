# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from json import dumps

class ScrapytestPipeline:
    def open_spider(self, spider):
        self.file = open(spider.output, 'w',encoding="utf8")
        if spider.extraItems:
           self.file.write("[")

    def close_spider(self, spider):
        if spider.extraItems:
           self.file.write("{}]")
        self.file.close()

    def process_item(self, item, spider):
        item = dumps(
            dict(item),
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
            ensure_ascii=False
        )
        self.file.write(item)
        if spider.extraItems:
           self.file.write(",\n")    
        return item
