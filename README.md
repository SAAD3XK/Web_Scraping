# Web_Scraping
In this project, I used scrapy to scrape amazon webpages detailing laptop information. 
A crawler is run which first scrapes the original index page from which the laptop descriptions and prices are saved.
Then each laptop's href is followed to get the extended description of each laptop.
All the info is saved to a pandas dataframe that is stored locally.
