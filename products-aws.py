from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from webdriver_manager import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
start=time.time()
web = 'https://www.amazon.in/s?k='
option = webdriver.ChromeOptions()
option.add_argument('--headless')
s=Service(executable_path=r'C:\Users\Joydip\Desktop\python files\chromedriver.exe')
driver = webdriver.Chrome(service=s, options=option)
keyword = input("enter your product:")
driver.get(web + keyword)
products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product
content = driver.page_source
soup = BeautifulSoup(content,features="lxml")

for a in soup.findAll('div', attrs={'class':'a-section a-spacing-base'}):
    name=a.find('a', href=True, attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    price=a.find('span', attrs={'class':'a-offscreen'})
    rating=a.find('a',href=True, attrs={'class':'a-popover-trigger a-declarative'})
    products.append(name.text)
    print(name.text)
    if price is None:
        prices.append("NA")
        print("NA")
    else:
        prices.append(price.text)
        print(price.text)
    if rating is None:
        ratings.append("NA")
        print("NA")
    else:
        ratings.append(rating.text)
        print(rating.text[0:3])
df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings})
df.to_json('products-aws.json', orient='records', lines=True)
end=time.time()
print('Execution time:',end-start)
