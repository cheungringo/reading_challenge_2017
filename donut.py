# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 20:55:23 2018

@author: Ringo
"""
import random
from helpers import is_fiction, get_credentials, white_rgba, \
    partition_books_by_genre
import plotly
import plotly.graph_objs as go

creds = get_credentials("creds.json")
plotly.tools.set_credentials_file(username=creds[0], api_key=creds[1])

def double_donut(books):
    '''
        Builds 2 two-ringed donut diagrams on the plot, one for fiction and 
        one for non-fiction.
    '''
    relevant_books = list(filter(lambda x: is_fiction(x['genre']), books))
    data = donut(relevant_books, 0.05, 0.15, 0.18, 0.25, "fiction")
    relevant_books = list(filter(lambda x: not is_fiction(x['genre']), books))
    data.extend(donut(relevant_books, 0.05, 0.15, 0.18, 0.75, "non-fiction"))
    layout = {
        "title":"Books Read by Genre 2017",
        "showlegend": False,
        "font": dict(
            family='Open Sans, monospace',
        ),
    }
    fig = go.Figure(
        data=data,
        layout=layout,
    )
    fig = plotly.offline.plot(fig, filename='double-donut.html')
    
def donut(books, in_radius, mid_radius, out_radius, center_x, fiction_str):
    '''
        Returns the data traces as an array for a two ringed donut chart 
        with the title in the middle.
        The first ring breaks the books down by genre while the second ring
        breaks down each of the genres by user rating.
    '''
    trace_in = build_trace([len(books)], \
        ["{}<br>{} books <br>read".format(len(books), fiction_str)], \
        {"x": [center_x - in_radius, center_x + in_radius]}, [], 'label', \
        'label', 0, dict(colors=[white_rgba()]), 
    )
    num_books_per_genre, genre_names, ratings, rating_texts = [], [], [], []
    # this is a hack because I want custom textinfo and hoverinfo and 
    # I can only specify one freeform array for the text field because this must be unique and
    # 7 rated 3/5 is not unique and messes up the pie chart
    books_by_genre = partition_books_by_genre(books)
    genre_map = {}
    genre_colors, label_texts = [], []
    for genre, books in books_by_genre.items():
        genre_colors.append(get_genre_color(genre_map, genre))
        num_books_per_genre.append(len(books))
        genre_names.append(genre)
    # same color for a genre but different shades by rating
    rating_colors = [] 
    for genre in genre_names:
        books_for_genre = books_by_genre[genre]
        for rating in range(5, -1, -1):
            books_with_cur_rating = (
                list(filter(lambda x: x['rating'] == rating, books_for_genre))
            )
            num_books_cur_rating = len(books_with_cur_rating)
            if num_books_cur_rating > 0:
                ratings.append(num_books_cur_rating)
                label_texts.append("{}★".format(rating))
                rating_texts.append(
                    build_pie_hoverstring(books_with_cur_rating),
                ) 
                rating_colors.append(
                    get_rating_shade(rating, genre_map[genre]),
                )
    marker = dict(colors=genre_colors, line=dict(color='#ffffff', width=1))
    trace_mid = build_trace(num_books_per_genre, genre_names, \
        {"x": [center_x - mid_radius, center_x + mid_radius]}, [], 'label', \
        'none', in_radius/mid_radius, marker)
    marker = dict(colors=rating_colors, line=dict(color='#ffffff', width=1))
    trace_outer = build_trace(ratings, rating_texts, \
        {"x": [center_x - out_radius, center_x + out_radius]}, label_texts, 
        'text', 'label', mid_radius/out_radius, marker)
    return [trace_in, trace_mid, trace_outer]

def build_trace(values, labels, domain, text, textinfo, hoverinfo, hole, \
    marker):
    '''
        Builds a data trace using the input arguments
    '''
    return {
        "values": values,
        "labels": labels,
        "domain": domain,
        "text": text,
        "textinfo": textinfo,
        "hoverinfo": hoverinfo,
        "type": "pie", 
        "hole": hole,
        "sort": False,
        "marker": marker,
    }
    
def build_pie_hoverstring(books):
    '''
        Builds the string that appears when you hover over the outermost ring.
    '''
    hover_info = ""
    for i in range(len(books)):
        book = books[i]
        hover_info += "{}. <i>{}</i> by {}<br>".format(
            i+1, book['title'], book['author'],
        )
    return hover_info
        
def get_genre_color(genre_map, genre):
    '''
        if the genre isn't in the map yet, randomly get a color for it. No need
        to check collisions because the chance of colliding is (1/256)^3 ~= 0.
    '''
    try:
        return genre_map[genre]
    except KeyError:
        color_str = '#%02x%02x%02x' % (
            int((random.randint(0, 256) + 255)/2),
            int((random.randint(0, 256) + 255)/2),
            int((random.randint(0, 256) + 255)/2),
        )
        genre_map[genre] = color_str
    return color_str

def get_rating_shade(rating, color_str):
    '''
        Expects a hex color like this: #ffffff and gets the appropriate shade 
        for the rating with 5 being the darkest and 0 being the lightest. 
    '''
    h = color_str.lstrip('#')
    rgb = tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))
    shaded_rgb = tuple(min(x - 15*(rating-2), 255) for x in rgb)
    return '#%02x%02x%02x' % shaded_rgb
