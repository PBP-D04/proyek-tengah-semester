from django.conf import settings
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bookphoria.settings")  # Ganti 'myproject' dengan nama proyek Django Anda
import django
django.setup()
from Homepage.models import Book, Author, Category
from django.contrib.auth.models import User
from datetime import date


def get_json_from_file(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data
def add_dummy_data(json_data):
    user = User.objects.get(username='isaganteng')
    for book_data in json_data:
        print(book_data['volumeInfo']['title'], "\n")

        # mendapatkan nama author dan entitas author
        author_names = book_data['volumeInfo'].get('authors', [])
        authors = []
        for author_name in author_names:
            author, created = Author.objects.get_or_create(name=author_name)
            authors.append(author)

        # mendapatkan kumpulan kategori
        category_names = book_data['volumeInfo'].get('categories', [])
        categories = []
        for category_name in category_names:
            category, created = Category.objects.get_or_create(name=category_name)
            categories.append(category)

        # mendapatkan date dari published_date dari json
        published_date_str = book_data['volumeInfo'].get('publishedDate', None)
        if(published_date_str is not None):
            if len(published_date_str) == 4:
                published_date_str+='-01-01'
            elif len(published_date_str) == 7 and published_date_str.count('-') == 1:
                published_date_str += '-01'

            published_date = date.fromisoformat(published_date_str)
        
        # mendapatkan saleability
        saleability = True if book_data['saleInfo']['saleability'] == 'FOR_SALE' else False
        print('ini saleability: ',saleability)
        # mendapatkan url pdf & epub link yang sesuai
        pdf_link = book_data['accessInfo']['pdf'].get('acsTokenLink', None)
        epub_link = book_data['accessInfo']['epub'].get('acsTokenLink', None)
        if(pdf_link is None):
            pdf_link = book_data['accessInfo']['pdf'].get('downloadLink', None)
        if(epub_link is None):
            epub_link = book_data['accessInfo']['epub'].get('downloadLink', None)
        print('ini pdf dan epub link: ', pdf_link, ' dan ', epub_link )
        print('\n')
        
        newBook = Book(
            user= user,
            title = book_data['volumeInfo']['title'],
            subtitle = book_data['volumeInfo'].get('subtitle',None),
            description = book_data['volumeInfo'].get('description',None),
            publisher = book_data['volumeInfo'].get('publisher',None),
            published_date = published_date,
            language = book_data['volumeInfo']['language'],
            is_ebook = book_data['saleInfo']['isEbook'],
            pdf_available = book_data['accessInfo']['pdf']['isAvailable'],
            pdf_link = pdf_link,
            thumbnail = book_data['volumeInfo']['imageLinks'].get('thumbnail', None),
            price = book_data['saleInfo'].get('retailPrice',{}).get('amount',None),
            currencyCode = book_data['saleInfo'].get('retailPrice',{}).get('currencyCode',None),
            saleability = saleability,
            buy_link = book_data['saleInfo'].get('buyLink', None),
            epub_available = book_data['accessInfo']['epub']['isAvailable'],
            epub_link = epub_link,
            maturity_rating = book_data['volumeInfo']['maturityRating'],
            page_count = int(book_data['volumeInfo'].get('pageCount', 0))
        )
        newBook.save()
        newBook.authors.add(*authors)
        newBook.categories.add(*categories)
def main():
    json_file_data = get_json_from_file('books.json')
    add_dummy_data(json_file_data)

if __name__ == '__main__':
    main()