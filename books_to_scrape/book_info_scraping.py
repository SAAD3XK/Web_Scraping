import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

class Books_Crawler(scrapy.Spider):
    name = "books_crawler"

    # parses through all 50 pages
    def start_requests(self):
        for i in range(1, 51):
            temp_url = f"https://books.toscrape.com/catalogue/page-{i}.html"
            yield scrapy.Request(url = temp_url,
                                callback = self.parse_front)
    
    def parse_front(self, response):
        book_divs = response.xpath('//li[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]')

        # extracting titles of all 20 books
        titles_list = book_divs.xpath('.//h3/a/@title').extract()

        # extracting urls of all 20 books
        price_list = book_divs.xpath('.//p[@class="price_color"]/text()').extract()

        # extracting prices of all 20 books
        url_list = book_divs.xpath('.//h3/a/@href').extract()

        # passing each book's url, title, and price to parse_back method
        for title, price, url in zip(titles_list, price_list, url_list):
            yield response.follow(url=url, callback=self.parse_back,
                                  cb_kwargs={'title': title, 'price': price, 'url': url})

    def parse_back(self, response, title, price, url):
        # parses book's description
        book_desc = response.xpath('//div[@id="content_inner"]/article/p/text()').extract()

        if book_desc:
            book_desc_list.append(book_desc[0])  # Take only the first description if available
        else:
            book_desc_list.append(-1)  # Use -1 to represent missing description
        
        # update book_titles list
        book_titles_list.append(title)

        # update book_prices list
        book_prices_list.append(price)

        base_url = 'https://books.toscrape.com/catalogue/'

        # update book_urls list
        book_page_links_list.append(base_url + url)

# initializing the list variables
book_titles_list = list()
book_prices_list = list()
book_desc_list = list()
book_page_links_list = list()

# starting crawler process
process = CrawlerProcess()
process.crawl(Books_Crawler)
process.start()    

# create dictionary of lists
data = {
    "book_titles": book_titles_list,
    "book_prices": book_prices_list,
    "book_descs": book_desc_list,
    "page_links": book_page_links_list
}

# creating dataframe
final_df = pd.DataFrame(data)

# saving dataframe to csv
final_df.to_csv('books_scraping.csv', index=False)
