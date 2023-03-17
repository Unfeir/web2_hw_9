from models import Authors, Quotes
from scrap import grab_author, grab_quotes

from datetime import datetime

base_url = 'https://quotes.toscrape.com'

def create_author(author: dict):
    """Create author from dict"""
    biography = grab_author(base_url + author['link'])
    person = Authors(fullname=author['fullname'])

    person.born_date = datetime.strptime(biography['born_date'], '%B %d, %Y').date()
    person.born_location = biography['born_location']
    person.description = biography['description']
    person.save()
    return person.id


def search_author(name: str):
    """Take author name and return author ID"""

    author = Authors.objects(fullname=name)
    if author:
        for el in author:
            return el.id
    return


def create_quote(quote: dict):
    """Create quote, if quote with new author - will create this author"""

    name = quote['author']['fullname']
    author_id = search_author(name)
    if not author_id:

        author_id = create_author(quote['author'])

    quot = Quotes(quote=quote['quote'])
    quot.author = author_id
    quot.tags = quote['tags']
    quot.save()


if __name__ == '__main__':
    quotes_for_db = grab_quotes(base_url)
    for quote in quotes_for_db:
        create_quote(quote)