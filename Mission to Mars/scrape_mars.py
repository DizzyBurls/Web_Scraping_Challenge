import requests
import os
from splinter import Browser
from bs4 import BeautifulSoup as BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Establish the target URL

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Use Beautiful Soup to scrape the target URL and return 'pretty' html.

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
  
    # Noting that the title we want is in the <div class="list_text">, select the FIRST title in the scraped code:

    recent_article = news_soup.select_one('div', class_='list_text')
    recent_title = recent_article.find('div', class_='content_title')
 
    # Clean the most recent title so as to only diplay text.

    recent_title_text_only = recent_article.find('div', class_='content_title').get_text()
    
    # Noting that the paragraph we want is in the <div class="article_teaser_body">, select the FIRST paragraph in the scraped code:

    recent_paragraph = recent_article.find("div", class_ ="article_teaser_body").text
     
    # Establish the URL that we need to scrape from.

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Create Beautiful Soup data.

    html = browser.html
    mars_image_soup = BeautifulSoup(html, 'html.parser') 
  
    # Noting that the image link is in <a class="showimg fancybox-thumbs" href="image/featured/mars2.jpg" target="_blank">:

    image_to_scrape = mars_image_soup.find('a', class_="showimg fancybox-thumbs")
    
    # Build a URL to the jpg in question.

    image_to_scrape_url = url + image_to_scrape["href"]
  
    # Establish the URL to be scraped.

    url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(url)

    # Call the second table and store it as a Pandas database.

    Mars_Facts_df = tables[1]
    Mars_Facts_df.columns = ['Description','Value']

    # Use Pandas to convert the data to a HTML table string
    Mars_Facts_html = Mars_Facts_df.to_html()
    
    # Remove 'new lines'.

    Mars_Facts_html.replace('\n', '')

    # Establish the URL to be scraped.

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create Beautiful Soup data.

    html = browser.html
    hemisphere_image_soup = BeautifulSoup(html, 'html.parser') 
    
    # Noting that the information of interest is in <div class="description">:

    data_to_scrape = hemisphere_image_soup.find_all('div', class_="description")
    
    # Create and empty list for scraped data.

    hemispheres_list=[]

    for i in range(len(data_to_scrape)):
    
        hemisphere_url = url + data_to_scrape[i].a['href']
        browser.visit(hemisphere_url)
        html = browser.html
        High_Res_soup = BeautifulSoup(html, "html.parser")
        hemisphere_title = High_Res_soup.find('h2', class_="title").text
        hemisphere_img_url = url + High_Res_soup.find_all('img')[4]['src']
    
        hemispheres_list.append({'title': hemisphere_title, 'img_url': hemisphere_img_url})

    browser.quit()

    # Store all scraped data in the one dictionary.
    
    scrape_data = {"article_title": recent_title_text_only,
        "article_paragraph": recent_paragraph,
        "feature_image_url": image_to_scrape_url,
        "mars_statistics": Mars_Facts_html,
        "image_urls_hemispheres": hemispheres_list
    }
    return scrape_data

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_info())