# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 17:17:02 2018

@author: Ringo
"""
from datetime import datetime
import csv

def read_books_from_file(file_name):
    '''
        Reads <file_name> csv file and returns a list of book dictionaries
    '''
    firstrow = True # ignore the column headers
    books = []
    with open(file_name, 'r+', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if firstrow:
                firstrow = False
                continue
            books.append({
                'id': row[0],
                'title': row[1],
                'isbn': row[2],
                'isbn13': row[3],
                'read_at': datetime.strptime(
                    row[4], 
                    "%a %b %d %H:%M:%S %z %Y",
                ),
                'average_rating': float(row[5]),
                'rating': int(row[6]),
                'categories': row[7],
                'genre': row[8],
                'word_count': int(row[9]),
                'author': row[10],
            })
    return books

def save_books_to_file(books, file_name):
    '''
        Saves the list of book dictionaries to csv file <file_name>
    '''
    with open(file_name, 'w+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow([
            'Goodreads Id', 
            'Title', 
            'ISBN', 
            'ISBN13', 
            'Read At', 
            'Average Rating', 
            'Rating', 
            'Categories',
            'Genre',
            'Word Count',
            'Author',
        ])
        for book in books:
            csv_writer.writerow([
                book['id'], 
                book['title'], 
                book['isbn'],
                book['isbn13'], 
                book['read_at'].strftime("%a %b %d %H:%M:%S %z %Y"),
                book['average_rating'],
                book['rating'],
                book['categories'],
                book['genre'],
                book['word_count'],
                book['author'],
            ])

