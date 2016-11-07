from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
import csv
import json

names = []

url ='http://www.jabong.com/men/clothing/new-products'
def scrollDown(browser, numberOfScrollDowns):
	body = browser.find_element_by_tag_name("body")
 	while numberOfScrollDowns >=0:
 		print numberOfScrollDowns
 		try:
	 		browser.find_element_by_css_selector('.load-more-products').click()
	 		numberOfScrollDowns=numberOfScrollDowns-1
		except:
			pass
		time.sleep(2)
	return browser

def secondcrawl(l):
	html  = requests.get(l)
	data = html.text
	print "Second crawl"
	print l
	try:
		soup = BeautifulSoup(data,'html.parser')
		sellerinfo = soup.find('div',{'class':'seller-info'})
		sellername = sellerinfo.find('div',{'class':'btn-popover title delivery-info'}).text
		sellerinside = sellerinfo.find('div',{'id':'seller-info-content'})
		selleraddress = sellerinside.find('span',{'class':'col-lg-9 col-md-9 col-sm-9 seller-detail seller-detail-add'}).text
		selleremail = sellerinside.find('span',{'class':'col-lg-9 col-md-9 col-sm-9 email'}).text
		print selleremail
		if sellername not in names:
			names[sellername] = "'"+selleraddress+"','"+selleremail+"'"
			print names
			with open('data.json', 'w') as f:
     				json.dump(names, f)
	except:
		pass
	

def crawl(l):
	browser = webdriver.Chrome()
	browser.get(l)
	browser = scrollDown(browser,230)
	print "Starting Crawl"
	maindiv = browser.find_elements_by_css_selector('.col-xxs-6.col-xs-4.col-sm-4.col-md-3.col-lg-3.product-tile.img-responsive')
	c=0
	for productdivs in maindiv:
		print c
		if c==0:
			c=c+1
			pass
		else:
			c=c+1
			a_element = productdivs.find_element_by_tag_name("a")
			product_link = a_element.get_attribute("href")
			secondcrawl(str(product_link))

crawl(url)
del crawl