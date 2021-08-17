# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 23:01:47 2021

@author: ZAP

Run specific line only : Fn + F9
Commenting one line: Ctrl + /

"""

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# ChromeDriver
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--incognito')
# prefs = {'profile.managed_default_content_settings.image': 2}
# chrome_options.add_experimental_option("prefs", prefs)
# driver = webdriver.Chrome(
#     options=chrome_options, executable_path='E:/Development/ChromeDriver/chromedriver.exe')

# URL = "https://id.investing.com/indices/idx-composite-news"
URL = "https://www.cnbcindonesia.com/indeks?date="
page = requests.get(URL)
time.sleep(6)
print(page.text)


soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="wrapper")
print(results)


"""
REFERENSI 2
https://www.edureka.co/blog/web-scraping-with-python/   
"""
# products=[] #List to store name of the product
# prices=[] #List to store price of the product
# ratings=[] #List to store rating of the product
# driver.get("https://www.flipkart.com/laptops/~buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;uniq")

# # extract the data from the website

# content = driver.page_source
# soup = BeautifulSoup(content)
# for a in soup.findAll('a',href=True, attrs={'class':'_31qSD5'}):
#     name=a.find('div', attrs={'class':'_3wU53n'})
#     price=a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
#     rating=a.find('div', attrs={'class':'hGSR34 _2beYZw'})
#     products.append(name.text)
#     prices.append(price.text)
#     ratings.append(rating.text)

# df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings})

"""
REFERENSI 3

https://medium.com/milooproject/python-simple-crawling-using-beautifulsoup-8247657c2de5
https://gist.github.com/adamaulia/ac6075c6a2bbd626257e0c551656b340

Step to crawling website:
    1. get url
    2. find last page
    3. loop paging
    4. loop news in current page
"""

# prepare the dataframe
data_sentimen_berita = pd.DataFrame(
    columns=['tanggal', 'judul_berita', 'isi_berita'])


def crawl_sentiment_from_Investing(url):
    result = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    print(soup.prettify())
    # find paging page
    # paging element in website
    paging = soup.find_all("div", {'class': 'arial_12 js-pagination-wrapper'})
    print('Paging size: {}'.format(paging))
    paging_link = paging[0].find_all('a', {'class': 'pagination'})
    last_page = int([item.get('href').split('/')[-1]
                     for item in paging_link][-1])

    # looping through paging
    for page in range(1, last_page):
        print('Crawling throgh page {0} of {1}'.format(page, last_page))

        # find article link
        # karena buat pindah page selanjutnya, ntar url nya jadi https://id.investing.com/indices/idx-composite-news/<page>
        article_url = url + "/" + str(page)
        article_req = requests.get(article_url)
        article_soup = BeautifulSoup(article_req.text, "lxml")
        # list beritanya (?)
        # find_all nge return list elemen yang ada di dalem elemen yang dipanggil
        news_link = article_soup.find_all("div", {'class': 'medium_Title1'})

        # looping through article link
        for idx, news in enumerate(news_link):
            news_dict = {}

            # get news date published
            news_date = news.find('span').text
            # get news title
            news_title = news.find('a', {'class': 'title'}).text

            # get the news's url link
            news_url = news.find('a', {'class': 'title'}).get('href')

            # get news content in url
            req_news = requests.get(news_url)
            soup_news = BeautifulSoup(req_news.text, "lxml")

            # get news content
            news_content = soup_news.find(
                "div", {'class': 'WSYIWYF articlePage'})

            # get the content by looping through <p> div element
            p = news_content.find_all('p')
            content = ' '.join(item .text for item in p)
            news_content = content.encode('utf8', 'replace')

            # wrap in dictionary
            news_dict['id'] = idx
            news_dict['news_date'] = news_date
            news_dict['news_url'] = news_url
            news_dict['news_title'] = news_title
            news_dict['news_content'] = news_content
            result.append(news_dict)
    return result


sentiment_data = crawl_sentiment_from_Investing(URL)
sentiment_data
