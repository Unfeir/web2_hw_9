import re
import requests
from bs4 import BeautifulSoup


# base_url = 'https://quotes.toscrape.com'

def grab_quotes(url, next_page='/'):
    # print(url + next_page)
    all_quotes = []
    response = requests.get(url + next_page)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.select('div[class=col-md-8] div[class=quote]')
        npage = soup.select('ul[class=pager] li[class=next] a')

        for el in quotes:
            quote = {"tags": [], "author": {"fullname": "", "link": ""}, "quote": ""}
            quote_ = el.find('span', attrs={"class": "text"}).text
            quote["quote"] = quote_
            author = el.find('small', attrs={"class": "author"}).text
            quote["author"]["fullname"] = author
            author_link = el.find('a', href=True)
            quote["author"]["link"] = author_link['href']
            # print(author_link['href'])
            tags_ = el.select('a[class=tag]')
            quote["tags"] = list([tag.text for tag in tags_])
            all_quotes.append(quote)
            # break
        # print(all_quotes)


        if npage:
            # print(npage[0]['href'])
            all_quotes.extend(grab_quotes(url, npage[0]['href']))

        return all_quotes


# print(grab_quotes(base_url))


def grab_author(url):
    biography = {"born_date": "", "born_location": "", "description": ""}
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # name = soup.select('[class=author-title]')
        born_date = soup.select('div[class=author-details] span[class=author-born-date]')
        born_location = soup.select('div[class=author-details] span[class=author-born-location]')
        description = soup.select('div[class=author-details] div[class=author-description]')
        biography["born_date"] = born_date[0].text
        biography["born_location"] = born_location[0].text.replace("in ", "")
        biography["description"] = description[0].text.strip()

        return biography

# print(authors('http://quotes.toscrape.com/author/Marilyn-Monroe'))

