import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import pandas as pd

class Amazon_Laptops_Crawler(scrapy.Spider):
    name = "amazon_laptops_crawler"
    def start_requests(self):
        url = "https://www.amazon.ae/s?k=laptops&crid=3TPMTJP3KNQS2&sprefix=lapto%2Caps%2C383&ref=nb_sb_noss_2"
        yield scrapy.Request(url = url,
                             callback = self.parse_front)
    
    # parses the laptop price and short description
    def parse_front(self, response):
        laptop_divs = response.xpath('//div[@class="sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"]')
        short_descs_list = laptop_divs.xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]/text()').extract()
        price_list = laptop_divs.xpath('.//span[@class="a-price-whole"]/text()').extract()
        final_df['laptop_names']=short_descs_list
        final_df['prices(AED)']=price_list
        # desc_and_price.update(dict(zip(short_descs_list, price_list)))
        url_list = response.xpath('//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/@href').extract()
        base_url = 'https://www.amazon.ae'
        for webpage in url_list:
            yield response.follow(url = base_url + webpage, callback = self.parse_back)

    # parses the laptop extended description
    def parse_back(self, response):
        temp = response.css('table.a-normal.a-spacing-micro')
        temp2 = temp.xpath('.//tr[contains(@class, "a-spacing-small")]')
        keys = temp2.xpath('.//td[@class="a-span3"]/span/text()').extract()
        values = temp2.xpath('.//td[@class="a-span9"]/span/text()').extract()
        temp_dict = dict(zip(keys, values))
        extended_desc_list.append(temp_dict)


# logging.basicConfig(level=logging.INFO)
extended_desc_list = list()
final_df = pd.DataFrame()

process = CrawlerProcess()
process.crawl(Amazon_Laptops_Crawler)
process.start()    

final_df['extended_specs'] = extended_desc_list
final_df.to_csv('amazon_laptop_result.csv', encoding='utf-8')