# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 20:56:41 2018

@author: Ringo
"""
import json

def get_credentials(file_name):
    creds = json.load(open(file_name))
    return (creds["username"], creds["api_key"])

# BEGIN: color functions 

def black_rgba():
    return 'rgba(0, 0, 0, 1)'

def white_rgba():
    return 'rgba(255, 255, 255, 0)'

def fic_color_rgba():
    # fic: http://www.color-hex.com/color/c0c0c1
    return 'rgba(192, 192, 193, 0.7)'

def nonfic_color_rgba():
    # nonfic: http://www.color-hex.com/color/2a3132
    return 'rgba(42, 49, 50, 0.7)'

def get_color_fic(genre):
    '''
        this helped: https://www.canva.com/learn/100-color-combinations/
    '''
    try:
        if is_fiction(genre):
            return fic_color_rgba()
        else:
            return nonfic_color_rgba()
    except ValueError:
        # TODO: pick an error color
        pass

# END: color functions

def hours_spent_reading(books, wpm):
    '''
        calculates hours spent reading by summing up total word count and
        dividing by my reading speed in wpm
    '''
    return (sum([book['word_count'] for book in books])/wpm)/60.0

# BEGIN: partitioning lists into dictionary of lists
    
def partition_books_by_genre(books):
    '''
        partitions books into lists based on which genre the book is, sorting is not necessary
    '''
    books_by_genre = {}
    for book in books:
        genre = book['genre']
        if genre in books_by_genre.keys():
            books_by_genre[genre].append(book)
        else:
            books_by_genre[genre] = [book]
    return books_by_genre

def partition_books_by_month(books):
    '''
        partitions books into lists based on which month the book was read in
        within each of these partitioned lists, the books are sorted in order
        of decreasing word count
    '''
    books_by_month = []
    books_per_month = [] # TODO: remove
    count = 0 # TODO: remove
    for month in range(1, 13):
        current_month_books = list(
            filter(lambda x: month == x['read_at'].month, books)
        )
        current_month_books.sort(
            key=lambda x: x['read_at'].day,
        )
        books_per_month.append(len(current_month_books)) # TODO: remove
        count += len(current_month_books) # TODO: remove
        books_by_month.append(current_month_books)
    return books_by_month

# END: partitioning lists into dictionary of lists

# BEGIN: building html strings
    
def build_info(book):
    return (
        "<i>{}</i> by {}<br>"
        "Finished {} <br>"
        "Genre: {}<br>"
        "Word Count: {}".format(
            book['title'], book['author'],
            book['read_at'].strftime("%b %d"), 
            book['genre'],
            book['word_count'],
        )
    )

def build_info_arrow(book):
    return (
        "<i>{}</i> by {}<br>"
        "Finished {} <br>"
        "Genre: {}<br>"
        "My Rating: {}<br>"
        "Average Rating: {}".format(
            book['title'], book['author'],
            book['read_at'].strftime("%b %d"), 
            book['genre'],
            book['rating'],
            book['average_rating'],
        )
    )

# END: building html strings
        
def is_fiction(genre):
    '''
    returns True if this genre belongs to fiction, False if genre does not and
    throws an error if the genre is unknown
    '''
    wikipedia_genres = "https://en.wikipedia.org/wiki/List_of_writing_genres" \
        "#Genre_categories:_fiction_and_nonfiction"
    fiction_genres = [
        'classic',
        'comics/graphic novel',
        'crime',
        'crime/detective',
        'fable',
        'fairy tale',
        'fan fiction',
        'fantasy',
        'folklore',
        'historical fiction',
        'horror',
        'humor',
        'legend',
        'magical realism',
        'meta fiction',
        'mystery',
        'mythology',
        'mythopeia',
        'picture book',
        'realistic fiction',
        'science fiction',
        'short story',
        'short story collection',
        'suspense/thriller',
        'tall tale',
        'western', 
        'literary fiction'
    ]
    nonfiction_genres = [
        'biography',
        'essay',
        'owner\'s manual',
        'journalism',
        'lab report',
        'memoir',
        'narrative nonfiction',
        'reference',
        'self-help',
        'speech',
        'textbook',
    ]
    if genre in fiction_genres:
        return True
    if genre in nonfiction_genres:
        return False
    raise ValueError(
        "Genre {} does not belong to the list of genres found at {}".format(
            genre,
            wikipedia_genres
        )
    )

