from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from webdriver_manager import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
start=time.time()
web = 'https://www.flipkart.com/search?q='
option = webdriver.ChromeOptions()
option.add_argument('--headless')
s=Service(executable_path=r'C:\Users\Joydip\Desktop\python files\chromedriver.exe')
driver = webdriver.Chrome(service=s, options=option)
keyword = input("enter your product:")
driver.get(web + keyword)
products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product
rev=[]
r=[]
l1=[]
description=[]
href=[]
img=[]
content = driver.page_source
soup = BeautifulSoup(content,features="lxml")
element = driver.find_element(by=By.CLASS_NAME, value="_13oc-S").find_element(by=By.TAG_NAME, value = "div").find_element(by=By.TAG_NAME, value = "div")
class_val = element.get_attribute("class")
print(class_val)
def review():
  HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

	# Making the HTTP Request
  webpage = requests.get(web+keyword, headers=HEADERS)

	# Creating the Soup Object containing all data
  soup = BeautifulSoup(webpage.content, "lxml")
  #links = soup.find('a', attrs={'rel':'noopener noreferrer'})
  '''if class_val=='_2kHMtA':
    links = soup.find_all('div', attrs={'class':'_2kHMtA'})
  else:
    links = soup.find_all('div', attrs={'class':'_4ddWXP'})
  for l in links:
    href = l.find('a')['href']'''
    #if len(href)>100:
  for l in href:
    url='https://www.flipkart.com'+l
    print(url)
    if len(l1) !=4:
        l1.append(url)
  for i in range(len(l1)):
    HEAD = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

	# Making the HTTP Request
    webpge = requests.get(l1[i], headers=HEAD)

	# Creating the Soup Object containing all data
    soup = BeautifulSoup(webpge.content, "lxml")
    if class_val=='_4ddWXP':
      desc=soup.find('div',attrs={'class':'_2418kt'})
      if len(description) !=4: description.append(desc.text)
    r=[]
    for b in soup.findAll('div', attrs={'class':'t-ZTKy'}):
      r.append(b.text.strip())
    if len(rev) !=4:
      rev.append(r)
      #print(rev)
    del r

def vertical(val):
 for a in soup.findAll('div', attrs={'class':val}):
    purl=a.find('a',attrs={'class':'_1fQZEK'})['href']
    image=a.find('img', attrs={'class':'_396cs4 _3exPp9'})
    name=a.find('div', attrs={'class':'_4rR01T'})
    price=a.find('div', attrs={'class':'_30jeq3 _1_WHN1'})
    rating=a.find('div', attrs={'class':'_3LWZlK'})
    desc=a.find('ul',attrs={'class':'_1xgFaf'})
    if len(products) !=4: products.append(name.text)
    #print(name.text)
    if len(prices) !=4: prices.append(int(price.text[1::].replace(',','')))
    #print(price.text)
    if len(ratings) !=4:
      if rating is None:
        ratings.append("No rating")
        #print("No rating")
      else:
        ratings.append(rating.text)
        #print(rating.text)
    if len(img) !=4: img.append(image.get('src'))
    #print(image.get('src'))
    if len(href) !=4: href.append(purl)
    if len(description) !=4: description.append(desc.text)
def horizontal(val):
    for a in soup.findAll('div', attrs={'class':val}):
      purl=a.find('a',attrs={'class':'s1Q9rs'})['href']
      image=a.find('img', attrs={'class':'_396cs4 _3exPp9'})
      name=a.find('a', href=True, attrs={'class':'s1Q9rs'})
      price=a.find('div', attrs={'class':'_30jeq3'})
      rating=a.find('div', attrs={'class':'_3LWZlK'})
      desc=a.find('ul',attrs={'class':'_1xgFaf'})
      if len(products) !=4: products.append(name.text)
      #print(name.text)
      if len(prices) !=4: prices.append(int(price.text[1::].replace(',','')))
      #print(price.text)
      if len(ratings) !=4:
        if rating is None:
          ratings.append("No rating")
          #print("No rating")
        else:
          ratings.append(rating.text)
        #print(rating.text)
      if len(img) !=4: img.append(image.get('src'))
      #print(image.get('src'))
      if len(href) !=4: href.append(purl)
#time.sleep(2)
if class_val=='_2kHMtA':
    vertical(class_val)
    review()
else:
    horizontal(class_val)
    review()

df = pd.DataFrame([{'Srno':[x for x in range(5,9)],'Product Name':products,'Price':prices,'Description':description,'Url':l1,'Image URL':img,'Ratings':ratings,'Reviews':rev}])
df.to_json('products-ekart-1.json', orient='records', lines=True)

end=time.time()
print('Execution time:',end-start)