'''Get data'''
import requests
from bs4 import BeautifulSoup
index = 0
data = []
for i in range(0,10):
    url = 'https://oto.com.vn/mua-ban-xe-cu-da-qua-su-dung/p{}'.format(i)
    
    response = requests.get(url)
    content = response.content

    soup = BeautifulSoup(content, 'html.parser')
    body = soup.find_all('div', class_='item-car')
    body[0].find('li', class_='seller-phone').text
    for car in body:
        car_name = car.find('span', class_='car-name').string
        gear = car.find_all('li')[0].string
        fuel = car.find_all('li')[2].string
        km = car.find_all('li')[3].string
        price = car.find('p', class_='price').string
        city = car.find('li', class_='seller-location').text
        phone = car.find('li', class_='seller-phone').text
        #href
        data.append({'car_name':car_name, 
                    'gear':gear,
                    'fuel':fuel,
                    'km':km,
                    'price':price,
                    'city':city,
                    'phone':phone
                    })
    index += 1
    print(i)

print(data)
'''clean'''

'''#can define some functions to clean data
def fix_price(x):
    if x is not string:
    return int(x.strip()[0:-6])*1000000
fix_price(' 495 triệu\r\n                ')'''

'''save data'''