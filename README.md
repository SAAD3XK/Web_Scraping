# Web_Scraping
## amazon.ae
In this project, I used scrapy to scrape amazon webpages detailing laptop information.
- A crawler is run which first scrapes the original index page from which the laptop descriptions and prices are saved.
- Then each laptop's href is followed to get the extended description of each laptop.
- All the info is saved to a pandas dataframe that is stored locally.

## books.toscrape.com
Similarly in this part, I've used scrapy's crawler to extract and book info.
- The book titles and prices are extracted from the main index page
- Each book's main page is followed by the crawler using the href and the book description is extracted and appended to a list
- All the lists are added as columns to a pandas dataframe which is further stored as a csv locally.