from bs4 import BeautifulSoup
import requests
import pprint
import schedule
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
}

link = 'https://www.amazon.in/s?k=processors+intel+i7+13th&crid=1NAC4N7US11UF&sprefix=processors+intel+i7+13th%2Caps%2C210&ref=nb_sb_noss_2'

html_doc = requests.get(link,headers = headers)

text = BeautifulSoup(html_doc.text,'html.parser')

keyboard_price = text.select('.a-price-whole')
keyboard_name_span = text.select('[data-cy = "title-recipe"]')
keyboard_name = []

for tag in keyboard_name_span:
	name_span = tag.find_all('span')
	for span in name_span:
		if not span.attrs:
			name = span.get_text()
	if name != 'SponsoredSponsored ':
		keyboard_name.append(name)

keyboards = []
	
def show_products ():
	for idx,key_name in enumerate(keyboard_name):
		if idx<len(keyboard_price):
			price = keyboard_price[idx].get_text()
			keyboards.append({'name':key_name,'price':price})
		else:
			keyboards.append({'name':key_name,'price':None})

	return keyboards
pprint.pprint(show_products())

def send_email(product_name,price):
	requests.post("https://ntfy.sh/thunderbolt1010",
    data=f'''Product : {product_name} has a sudden price fall to {price}.
    Dont miss the offer , buy it !!!
    ''',
    headers={
        "Title": "Sudden Pice fall!!!",
        "Email": "rishivel10@gmail.com"
    })

pprint.pprint(show_products())

def check_price_reduced(product_name,product_price):
	show_products()
	for item in keyboards:
		if item['name']==product_name:
			print(f'Found Product : {product_name}')
			print(f'Actual Price : {product_price}')
			print(f'Current Price :{item['price']}')
			if int(item['price'].replace(',',''))< product_price:
				print('Product price dropped it is the right time to buy...')
				send_email(product_name,item['price'])
				return 
			else :
				print('Product price not dropped dont buy now !!')
				return
	print('No Product found!!')


#check_price_reduced('Apple MacBook Air Laptop: Apple M1 chip, 13.3-inch/33.74 cm Retina Display, 8GB RAM, 256GB SSD Storage, Backlit Keyboard, FaceTime HD Camera, Touch ID. Works with iPhone/iPad; Space Grey',40000)