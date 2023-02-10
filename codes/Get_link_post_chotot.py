'''Get all link of posts'''
import requests
from bs4 import BeautifulSoup

posts = []
for i in range(0,1000):
    url = 'https://xe.chotot.com/mua-ban-oto-cu-sdca1?page={}'.format(i)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print('time out')
        continue
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for y in soup.find_all('a', class_="AdItem_adItem__gDDQT"):
        link = 'https://xe.chotot.com'+y['href']
        posts.append(link)
    print(i)
print(len(posts)) #20015
#find unique link posts
uni_posts = set(posts) #19897
posts = list(uni_posts)
#save posts list into txt
with open('posts7-2-2023.txt', 'w') as f:
    for s in posts:
        f.write(s+'\n')
#read list into txt
with open("posts7-2-2023.txt", 'r') as f:
    posts = [line.rstrip('\n') for line in f]
print(len(posts))