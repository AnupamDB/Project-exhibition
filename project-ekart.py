from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from webdriver_manager import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
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
content = driver.page_source
soup = BeautifulSoup(content,features="lxml")
element = driver.find_element(by=By.CLASS_NAME, value="_13oc-S").find_element(by=By.TAG_NAME, value = "div").find_element(by=By.TAG_NAME, value = "div")
class_val = element.get_attribute("class")
print(class_val)
def vertical():
 for a in soup.findAll('a',href=True, attrs={'class':'_1fQZEK'}):
    name=a.find('div', attrs={'class':'_4rR01T'})
    price=a.find('div', attrs={'class':'_30jeq3 _1_WHN1'})
    rating=a.find('div', attrs={'class':'_3LWZlK'})
    products.append(name.text)
    print(name.text)
    prices.append(price.text)
    print(price.text)
    if rating is None:
        ratings.append("No rating")
        print("No rating")
    else:
        ratings.append(rating.text)
        print(rating.text)
def horizontal(val):
    for a in soup.findAll('div', attrs={'class':val}):
      name=a.find('a', href=True, attrs={'class':'s1Q9rs'})
      price=a.find('div', attrs={'class':'_30jeq3'})
      rating=a.find('div', attrs={'class':'_3LWZlK'})
      products.append(name.text)
      print(name.text)
      prices.append(price.text)
      print(price.text)
      if rating is None:
        ratings.append("No rating")
        print("No rating")
      else:
        ratings.append(rating.text)
        print(rating.text)
if class_val=='_2kHMtA':
    vertical()
else:
    horizontal(class_val)
df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings})
df.to_json('products-ekart.json', orient='records', lines=True)
end=time.time()
print('Execution time:',end-start)
'''df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings})
df.to_csv('products.csv', index=False, encoding='utf-8')'''
