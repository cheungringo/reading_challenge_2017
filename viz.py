from rw import read_books_from_file
from timeline import timeline
from donut import double_donut
from helpers import hours_spent_reading, get_credentials
from arrow import arrow
import plotly

creds = get_credentials("creds.json")
plotly.tools.set_credentials_file(username=creds[0], api_key=creds[1])

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
