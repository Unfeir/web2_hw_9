from models import Authors, Quotes

from datetime import datetime


def create_author(author: dict):
    """Create author from dict"""

    person = Authors(fullname=author['fullname'])
    person.born_date = datetime.strptime(author['born_date'], '%B %d, %Y').date()
    person.born_location = author['born_location']
    person.description = author['description']
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

    name = quote['author']
    author_id = search_author(name)
    if not author_id:
        author_id = create_author({'fullname': name})

    quot = Quotes(quote=quote['quote'])
    quot.author = author_id
    quot.tags = quote['tags']
    quot.save()

