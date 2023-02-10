'''Get data one post'''
#Access to a post site and get html content
import requests
from bs4 import BeautifulSoup

url = 'https://xe.chotot.com/mua-ban-oto-thanh-pho-gia-nghia-dak-nong/102931819.htm#px=SR-stickyad-[PO-1][PL-top]'
response = requests.get(url)
print(response.status_code) #200 is ok

content = response.content
soup = BeautifulSoup(content, 'html.parser')

#Brand
brand = soup.find('a', itemprop = 'carbrand').string
brand
#Carmodel
carmodel = soup.find('a', itemprop = 'carmodel').string
carmodel
#Manufactural year
mfyear_string = soup.find('span', itemprop = 'mfdate').string
from datetime import datetime
mftime = datetime.strptime(mfyear_string, '%Y')
mfyear = mftime.year
mfyear
#Km
km_string = soup.find('span', itemprop = 'mileage_v2').string
km = int(km_string)
km
#Transmission
gearbox = soup.find('span', itemprop = 'gearbox').string
gearbox
#Fuel
fuel = soup.find('span', itemprop = 'fuel').string
fuel
#Price
price_string = soup.find('span', itemprop = 'price').text
price = int(price_string[0:-3].replace('.','')) #remove '.','đ',' ' and convert to int
price
#Area: get data from script text so can not find out it in body content
'''area = soup.find('div', style='order:2').get_text() 
get all text from div contain address. The result do not include district'''

script = soup.find('script', id='__NEXT_DATA__').string
import re

start_pattern_district = 'area_name":"'
start_index_district = re.search(start_pattern_district, script).span()[1]
end_pattern_district = '","region'
end_index_district = re.search(end_pattern_district, script).span()[0]
district = script[start_index_district:end_index_district]
district

start_pattern_city = 'region_name":"'
start_index_city = re.search(start_pattern_city, script).span()[1]
end_pattern_city = '","company_ad'
end_index_city = re.search(end_pattern_city, script).span()[0]
city = script[start_index_city:end_index_city]
city

#Posted time get data from script text so can not find out it in body content
script = soup.find('script', id='__NEXT_DATA__').string
import re

start_pattern_time = 'date":"'
start_index_time = re.search(start_pattern_time, script).span()[1]
end_pattern_time = '","access-control-expose-headers"'
end_index_time = re.search(end_pattern_time, script).span()[0]
posted_time_string = script[start_index_time:end_index_time]
posted_time_string

from datetime import datetime
posted_time = datetime.strptime(posted_time_string, '%a, %d %b %Y %H:%M:%S %Z')

posted_year = posted_time.year
posted_month = posted_time.strftime('%b')
#PhoneNumber
'''phone_number = soup.find(class_='dtview')
print(soup)
phone_number'''
#Href
href = url
#Extract data into dictionary
data = {'brand': brand,
        'carmodel': carmodel,
        'year': mfyear,
        'km': km,
        'tranmission': gearbox,
        'fuel': fuel,
        'price': price,
        'dictrict': district,
        'city': city,
        'posted_year': posted_year,
        'posted_month': posted_month,
        'link': href
        }
print(data)

