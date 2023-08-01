import scrapy
from scrapy.crawler import CrawlerProcess
import logging

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
        desc_and_price.update(dict(zip(short_descs_list, price_list)))
        url_list = response.xpath('//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/@href').extract()
        base_url = 'https://www.amazon.ae'
        for webpage in url_list:
            yield response.follow(url = base_url + webpage, callback = self.parse_back)

    # parses the laptop extended description
    def parse_back(self, response):
        temp = response.xpath('//*[@id="productOverview_feature_div"]')
        temp2 = temp.xpath('.//div[@class="a-section a-spacing-small a-spacing-top-small"]/table/tbody')
        temp3 = temp2.xpath('.//tr/td[@class="a-span3"]/span/text()').extract()
        logging.info(f'The temp object is: {temp3}')


logging.basicConfig(level=logging.INFO)
desc_and_price = dict()

process = CrawlerProcess()
process.crawl(Amazon_Laptops_Crawler)
process.start()    
