# Define a function called `scrape` that will execute all of your scraping code from the `mission_to_mars.ipynb` notebook and return one Python dictionary containing all of the scraped data. 

from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo
import time


# Function `scrape` will execute all of scraping code from `mission_to_mars.ipynb`
# Return one Python dictionary containing all of the scraped data. 
def scrape():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    mars_data = {}
    news = mars_news(browser)
    mars_data['newstitle'] = news[0]
    mars_data['parent news'] = news[1]
    mars_data['image'] = mars_image(browser)
    mars_data['facts'] = mars_facts(browser)
    mars_data['hemis'] = mars_hemispheres(browser)
    return mars_data

# Scrapes NASA Mars News Site
# Pulls out latest news title and paragraph description
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    time.sleep(5)
 
    html = browser.html
    sitesoup = BeautifulSoup(html, 'html.parser')

    siteelement = sitesoup.select_one('ul.item_list li.slide')

    siteelement.find("div", class_='content_title')
    newstitle = siteelement.find("div", class_='content_title').get_text()

    parentnews = siteelement.find('div', class_="article_teaser_body").get_text()
    news_description = parentnews[0].text

    news = [newstitle, news_description]

    return news

# Scrapes JPL Mars Space Image Site 
# Pulls out featured image of Mars
def mars_image(browser):
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.findAll('img', class_= "headerimage fade-in")
    imgfound= img[0].attrs['src']

    imgfound_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'+imgfound

    return imgfound_url 

# Scrapes Space Facts Site
# Pulls out table with Mars facts and converts the table from Pandas to HTML format
def mars_facts(browser):
    goin2mars = 'https://space-facts.com/mars/'
    browser.visit(goin2mars)

    mars_data = pd.read_html(goin2mars)[1]
    cleaned_mars_data = mars_data.rename(columns= {'Mars - Earth Comparison': 'Attributes'}).drop(columns = ["Earth"])
    cleaned_mars_data 
    cleaned_mars_data_table = cleaned_mars_data.to_html(header=False, index=False)
    return cleaned_mars_data_table

# Scrapes Astrogeology USGS Site
# Pulls out high resolution images for each of Mar's hemispheres
# Results of image titles and urls are in list of dictionary format
def mars_hemispheres(browser):
    url ="https://astrogeology.usgs.gov"
    hemisphereUrl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphereUrl)
    
    time.sleep(1)

    html_hemisphere = browser.html
    soup_hemisphere = BeautifulSoup(html_hemisphere,'html.parser')

    list_imgs_url = []
    imgtitles = soup_hemisphere.findAll('h3')

    for title in range(len(imgtitles)):
        hemisphere ={}
        imgtitles = soup_hemisphere.findAll('h3')[title].text
        imgUrl = url + soup_hemisphere.findAll('a', class_='itemLink product-item')[title]['href']
        browser.visit(imgUrl)
    
        time.sleep(1)
    
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        imagelinktitle = soup.find('div', class_='downloads').find('a')['href']
        
        hemisphere["title"] = imgtitles
        hemisphere["imgUrl"] = imagelinktitle
        
        list_imgs_url.append(hemisphere)
        
        return list_imgs_url
