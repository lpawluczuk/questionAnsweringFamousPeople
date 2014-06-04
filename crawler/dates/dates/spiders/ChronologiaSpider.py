from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from dates.items import DatesItem
import re

class ChronologiaSpider(Spider):
    name = "chronologia"
    allowed_domains = ["chronologia.pl"]

    base_url = "http://www.chronologia.pl/"
    url_urodzeni = "urodzeni-"
    url_zmarli = "zmarli-"
    base_url_end = ".html"

    start_urls = [base_url + url_urodzeni + str(j) + "-" + str(i) + base_url_end for i in range(1,13) for j in range(1,32)] + [base_url + url_zmarli + str(j) + "-" + str(i) + base_url_end for i in range(1,13) for j in range(1,32)]
    
    def parse(self, response):
        sel = Selector(response)
        result = []
       
        ad = DatesItem()
        ad['name'] = ""
        for p in sel.xpath("//div[@class='poziomd']//text()").extract():

            if re.match("^.*,", p):
                if p.startswith(","):
                    ad['desc'] = p[2:]
                else:
                    ad['desc'] = p[6:]
                ad['name'] = ad['name'].lstrip('1234567890() ').strip()
                if re.match('^.\s', ad['name']):
                    ad['name'] = ad['name'][2:]

                ad['url'] = response.url
                if re.match(".*urodzeni.*", response.url):
                    ad['isBirth'] = True
                else:
                    ad['isBirth'] = False

                result.append(ad)
                ad = DatesItem()
                ad['name'] = ""
            elif re.match("^\s*[0-9]{1,4}", p) and not ad.has_key('date'):
                ad['date'] = re.match("^\s*[0-9]{1,4}", p).group()
            else:
                ad['name'] = ad['name'] + p
        return result
