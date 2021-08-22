# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests


# %%
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# %%
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# %%
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# %%
slide_elem.find('div', class_='content_title')


# %%
# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title                             


# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# %% [markdown]
# ### Featured Images

# %%
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# %%
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# %%
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# %%
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# %%
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# %%
df.to_html()

# %% [markdown]
# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# %% [markdown]
# ### Hemispheres

# %%
# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
response = requests.get(url);
soup = soup(response.text, 'lxml')
browser.visit(url)


# %%
# 2. Create a list to hold the images and titles.
links = []
hemisphere_image_urls = ['https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',
                         'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',
                         'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',
                         'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'
                         ];

div_results = soup.find('div', class_='collapsible results');
div_items = div_results.find('div', class_='item');

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for div_item in div_items:
    hemisphere = {}
    div_content = div_items.find('div', class_='description')
    
    title = div_content.find('h3').text
    hemisphere['title'] = title
    
    href = div_items.find('a', {"class":"itemLink product-item"})['href']
    links.append(base_url + href)
    
for link in links:
    response = requests.get(link)
    soup = soup(response.text, 'lxml')
        
    img_src = soup.find("img", {"class":"wide-image"})['src']
    img_url = base_url + img_src
    hemisphere['img_url'] = img_url
        
hemisphere_img_urls.append(hemisphere)

#browser.back()

   


# %%
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# %%
# 5. Quit the browser
browser.quit()


