import requests
import csv
import time
import bs4

url = "https://old.reddit.com/r/soccer/"
# Headers to mimic a browser visit
headers = {'User-Agent': 'Mozilla/5.0'}

# Returns a requests.models.Response object
page = requests.get(url, headers=headers)
soup = bs4.BeautifulSoup(page.text, 'html.parser')
domains = soup.find_all("span", class_="domain")
soup.find_all("span", {"class": "domain", "height": "100px"})
for domain in domains:
    if domain != "(self.soccer)":
        continue

    print(domain.text)

for domain in soup.find_all("span", class_="domain"):
    if domain != "(self.soccer)":
        continue

    parent_div = domain.parent.parent.parent.parent
    print(parent_div.text)

attrs = {'class': 'thing', 'data-domain': 'self.soccer'}
counter = 1
#for post in soup.find_all('div', attrs=attrs):
   # print(post.attrs['data-domain'])
while (counter <= 10):
    for post in soup.find_all('div', attrs=attrs):
        title = post.find('p', class_="title").text
        author = post.find('a', class_='author').text
        comments = post.find('a', class_='comments').text
        comments = post.find('a', class_='comments').text.split()[0]
        if comments == "comment":
           comments = 0

        likes = post.find("div", attrs={"class": "score likes"}).text
        if likes == "•":
           likes = "None"

        post_line = [counter, title, author, likes, comments]
        with open('output.csv', 'a') as f:
          writer = csv.writer(f)
          writer.writerow(post_line)
        counter += 1

    next_button = soup.find("span", class_="next-button")
    next_page_link = next_button.find("a").attrs['href']
    time.sleep(2)
    page = requests.get(next_page_link, headers=headers)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')


