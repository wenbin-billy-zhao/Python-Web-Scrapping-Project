# import dependencies
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# Get Mars Info
def mars_info():
    try:
        browser = init_browser()
        # create final dict for all mars info
        mars_info_dict = {}
        
        # read html from NASA website
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)

        # process html content
        html = browser.html
        # use bs to parse html into elements
        soup = bs(html, 'html.parser')

        #**********************************************************#
        # get news titles and news paragraphs
        news_title = soup.find("div", class_="content_title").text
        news_paragraph = soup.find("div", class_="article_teaser_body").text

        mars_info_dict['news_title'] = news_title
        mars_info_dict['news_paragraph'] = news_paragraph

        #**********************************************************#
        # GET JPL featured image url

        base_url = 'https://www.jpl.nasa.gov'
        mars_img_url = base_url + '/spaceimages/?search=&category=Mars'
        
        browser.visit(mars_img_url)
        browser.is_text_present('Full IMAGE')
        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(2)

        img_html = browser.html
        img_soup = bs(img_html, 'html.parser')
        
        img_url = img_soup.find('div', class_='fancybox-inner').img['src']
        
        featured_img_url = base_url + img_url

        mars_info_dict["featured_image_url"] = featured_img_url

        #**********************************************************#
        # scrape mars weather info from official twitter account page
        mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(mars_weather_url)
        time.sleep(2)

        mars_weather_html = browser.html

        mars_weather_soup = bs(mars_weather_html, 'lxml')

        # mars_weather = mars_weather_soup.find('p', class_='tweet-text').text.replace('\n', '').split("pic")[0]
        mars_weather = mars_weather_soup.find('p', class_='tweet-text').text.split("pic")[0]

        mars_info_dict['mars_weather'] = mars_weather


        #**********************************************************#
        # gest mars fact table and export to html table
        mars_facts_url = 'https://space-facts.com/mars/'

        mars_facts_table = pd.read_html(mars_facts_url)
        time.sleep(2)
        df = mars_facts_table[0]
        df.columns = ['Names', 'Value']
                
        mars_facts_html = df.to_html(index=False, justify='center')
        
        mars_info_dict['mars_facts'] = mars_facts_html

        ##### Mars Hemispheres #################################

        hemi_base_url = 'https://astrogeology.usgs.gov'
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        time.sleep(3)
        
        hemi_html = browser.html
        hemi_soup = bs(hemi_html, 'html.parser')
        items = hemi_soup.find_all('div', class_="item")
        hemi_img_dict = []

        for item in items:
            title = item.find('h3').text
            img_url = item.find('a', class_='itemLink product-item')['href']
            browser.visit(hemi_base_url + img_url)
            img_html = browser.html
            soup = bs(img_html, 'html.parser')
            img_url = hemi_base_url + soup.find('img', class_='wide-image')['src']
            hemi_img_dict.append(
                {
                    "title":title,
                    "img_url": img_url
                }
            )
        
        mars_info_dict["hemi"] = hemi_img_dict
    
        return mars_info_dict


    finally:
        browser.quit()



# debugging using the following lines
if __name__ == "__main__":
    listings = scrape()
    print(listings)
    
