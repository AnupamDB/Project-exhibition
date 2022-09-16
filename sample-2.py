# importing libraries
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from webdriver_manager import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
start=time.time()
web = 'https://www.amazon.in/s?k='
keyword = input("enter your product:")
HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
req=requests.get(web+keyword,headers=HEADERS)
soup = BeautifulSoup(req.content, "lxml")
products=[] #List to store name of the product
prices=[] #List to store price of the product
img=[]
link=[]
image=[]
description=[]
reviews=[]
tot=[]
links = soup.find_all('a', attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
for l in links:
    href = l.get('href')
    #print(href)
    url='https://www.amazon.in'+href
    #print(url)
    if len(link) !=4: link.append(url)
def main(URL):
	# opening our output file in append mode
	#File = open("out.csv", "a")

	# specifying user agent, You can use other user agents
	# available on the internet
	HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

	# Making the HTTP Request
	webpage = requests.get(URL, headers=HEADERS)

	# Creating the Soup Object containing all data
	soup = BeautifulSoup(webpage.content, "lxml")

	# retrieving product title
	try:
		# Outer Tag Object
		title = soup.find("span",attrs={"id": 'productTitle'})

		# Inner NavigableString Object
		title_value = title.string

		# Title as a string value
		title_string = title_value.strip().replace(',', '')
		if len(products) !=4:
			products.append(title_string)
			#print(title_string)
	except AttributeError:
		title_string = "NA"
		products.append(title_string)
	#print("product Title = ", title_string)

	# saving the title in the file
	#File.write(f"{title_string},")

	# retrieving price
	try:
		price = soup.find("span", attrs={'class': 'a-offscreen'}).string.strip().replace(',', '').replace('.00','').replace('₹','').strip()
		if len(prices) !=4:
			prices.append(price)
		#print(prices)
		# we are omitting unnecessary spaces
		# and commas form our string
	except AttributeError:
		price = "NA"
		prices.append(price)
	#print("Products price = ", price)

	# saving
	#File.write(f"{price},")

	try:
		review_count = soup.find("img", attrs={'id': 'landingImage'})
		if len(img) !=4:
			img.append(dict(review_count.attrs)["src"]) #print(ratings)

	except AttributeError:
		review_count = "NA"
		img.append(review_count)
	try:
		desc=soup.find('div', attrs={'id':'pov2FeatureBulletsExpanderContent'})
		if len(description) !=4:
			description.append(desc.text)
	except AttributeError:
		description.append('NA')
	#print("Total reviews = ", review_count)
	#File.write(f"{review_count},")
	review(URL,reviews)
	'''review=soup.find_all('div', attrs={'class': 'a-expander-content reviewText review-text-content a-expander-partial-collapse-content'})
	for i in review:
		reviews.append(i.text.strip())
	tot.append(reviews)
	print(tot)'''



def review(URL,reviews):
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

	# Making the HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

	# Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")
    review=soup.find_all('div', attrs={'class': 'a-expander-content reviewText review-text-content a-expander-partial-collapse-content'})
    #for i in range(1):
    reviews=[]
    for j in review: reviews.append(j.text.strip())
    if (len(tot) !=4): tot.append(reviews) #print(tot)
    del reviews

if __name__ == '__main__':
# opening our url file to access URLs

	# iterating over the urls
	for links in link:
		main(links)
		#review(links)
	df = pd.DataFrame([{'Sr no':[x for x in range(1,5)],'Product Name':products,'Description':description,'Price':prices,'Url':link,'Image Url':img,'Reviews':tot}])
	#df = df.transpose()
	df.to_json('products-aws1.json', orient='records', lines=True)
end=time.time()
print("Execution time:",end-start)