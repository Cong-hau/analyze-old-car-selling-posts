'''read list into txt'''
with open("posts7-2-2023.txt", 'r') as f:
    posts = [line.rstrip('\n') for line in f]
print(len(posts))


'''Get data from all posts'''
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

data = []
index = 0
for url in posts[0]:
    try:
        response = requests.get(url, timeout=15)
    except requests.Timeout:
        continue
    if response.status_code != 200:
        continue
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    #brand
    brand = soup.find('a', itemprop = 'carbrand')
    if brand is not None:
        brand = brand.string
    #carmodel
    carmodel = soup.find('a', itemprop = 'carmodel')
    if carmodel is not None:
        carmodel = carmodel.string
    #Manufactural year
    mfyear_string = soup.find('span', itemprop = 'mfdate')
    if mfyear_string is None:
        mfyear = None
    else:
        mfyear_string = mfyear_string.string
        try:
            mftime = datetime.strptime(mfyear_string, '%Y')
            mfyear = mftime.year
        except ValueError:
            mfyear = mfyear_string
    #km
    km_string = soup.find('span', itemprop = 'mileage_v2')
    if km_string is None:
        km = None
    else:
        km = int(km_string.string)
    #Transmission, Fuel
    gearbox = soup.find('span', itemprop = 'gearbox')
    if gearbox is not None:
        gearbox = gearbox.string
    fuel = soup.find('span', itemprop = 'fuel')
    if fuel is not None:
        fuel = fuel.string
    #Price
    price_string = soup.find('span', itemprop = 'price')
    if price_string is None:
        price = None
    else:
        price_string = price_string.text
        price = int(price_string[0:-3].replace('.','')) #remove '.','đ',' ' and convert to int
    #Area: dictrict, city
    script = soup.find('script', id='__NEXT_DATA__').string

    start_pattern_district = 'area_name":"'
    start_index_district = re.search(start_pattern_district, script)
    end_pattern_district = '","region'
    end_index_district = re.search(end_pattern_district, script)
    if start_index_district is None:
        district = None
    elif end_index_district is None:
        district = None
    else:
        district = script[start_index_district.span()[1]:end_index_district.span()[0]]
    
    start_pattern_city = 'region_name":"'
    start_index_city = re.search(start_pattern_city, script)
    end_pattern_city = '","company_ad'
    end_index_city = re.search(end_pattern_city, script)
    if start_index_city is None:
        city = None
    elif end_index_city is None:
        city = None
    else:
        city = script[start_index_city.span()[1]:end_index_city.span()[0]]
    #Posted time
    start_pattern_time = 'date":"'
    start_index_time = re.search(start_pattern_time, script)
    end_pattern_time = '","access-control-expose-headers"'
    end_index_time = re.search(end_pattern_time, script)
    if start_index_time is None:
        posted_time, posted_year, posted_month = None, None, None
    elif end_index_city is None:
        posted_time, posted_year, posted_month = None, None, None
    else:
        posted_time_string = script[start_index_time.span()[1]:end_index_time.span()[0]]
        try:
            posted_time = datetime.strptime(posted_time_string, '%a, %d %b %Y %H:%M:%S %Z')
            posted_year = posted_time.year
            posted_month = posted_time.strftime('%b')
        except ValueError:
            posted_time, posted_year, posted_month = None, None, None

    #PhoneNumber
    #Href
    href = url
    data.append({'brand': brand,
        'carmodel': carmodel,
        'year': mfyear,
        'km': km,
        'tranmission': gearbox,
        'fuel': fuel,
        'price': price,
        'district': district,
        'city': city,
        'posted_year': posted_year,
        'posted_month': posted_month,
        'link': href
        })
    index += 1
    print(index)
#print(len(data))
#Export: Write data into a new csv
import csv
keys = data[0].keys()   
'''with open('data.csv', 'w', encoding='utf8', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)'''
#Append new data into existed csv
with open('data.csv', 'a', encoding='utf8', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writerows(data)



