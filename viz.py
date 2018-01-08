from rw import read_books_from_file
from timeline import timeline
from donut import double_donut
from helpers import hours_spent_reading
from arrow import arrow

def main():
    '''
        Get list of books read in 2017. Create data visulizations. 
        Print out how many hours were spent reading this year.
    '''
    books = read_books_from_file('reading-challenge-2017_v2.csv')
    timeline(books)
    double_donut(books)
    arrow(books)
    print(hours_spent_reading(books, 350))
    
if __name__ == '__main__':
    main()
