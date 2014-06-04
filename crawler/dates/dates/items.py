# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
class DatesItem(Item):
    name = Field()
    date = Field()
    isBirth = Field()
    url = Field()
    desc = Field()
    