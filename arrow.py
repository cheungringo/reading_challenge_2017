# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 22:05:43 2018


@author: Ringo
"""
import plotly
import plotly.graph_objs as go
from helpers import build_info_arrow, is_fiction, black_rgba, white_rgba

fic_color = 'rgba(51, 107, 135, 1)' # orange
nonfic_color = 'rgba(255, 120, 80, 1)' # blue

def arrow(books):
    '''
        Builds a chart with vertical arrows pointing from my rating to average
        user rating. Arrows are colored by fiction/non-fiction and ordered in
        the x dimension by date read at.
    '''
    books.sort(key=lambda x: x['read_at'])
    x = [i+1 for i in range(len(books))]
    my_ratings = [book['rating'] for book in books]
    book_info = [build_info_arrow(book) for book in books]
    shapes = []
    build_arrows(books, shapes)
    trace_me = build_scatter(x, my_ratings, book_info, 'circle', white_rgba())
    trace_legend = build_legend()
    trace_avgs = build_avg_ratings(books)
    data = [trace_me, trace_legend]
    data.extend(trace_avgs)
    layout = go.Layout(
        title='My Ratings vs. Average User Ratings',
        xaxis=build_axis(0, 71, None, {}),
        yaxis=build_axis(
            2,
            5,
            title='Rating',
            titlefont=dict(
                family='Open Sans, monospace',
                size=14,
                color='rgba(0, 0, 0, 1)',
            )
        ),
        font=dict(
            family='Open Sans, monospace',
        ),
        showlegend=False,
        shapes=shapes,
    )
    fig = go.Figure(
        data=data,
        layout=layout,
    )
    fig = plotly.offline.plot(fig, filename='arrows.html')

def build_avg_ratings(books):
    '''
        Build average rating traces separately because we need the marker 
        symbols to be either triangle up or triangle down and either fic_color
        or nonfic_color which gives four combinations. Just use four traces.
    '''
    x_avg = {
        "up": {"fic": [], "nonfic": []}, 
        "down": {"fic": [], "nonfic": []},
    }
    ratings_avg = {
        "up": {"fic": [], "nonfic": []}, 
        "down": {"fic": [], "nonfic": []},
    }
    for i in range(len(books)):
        book = books[i]
        relevant_x, relevant_rating = None, None
        if book['rating'] > book['average_rating']:
            relevant_x = x_avg['down']
            relevant_rating = ratings_avg['down']
        if book['rating'] < book['average_rating']:
            relevant_x = x_avg['up']
            relevant_rating = ratings_avg['up']
        if is_fiction(book['genre']):
            relevant_x = relevant_x['fic']
            relevant_rating = relevant_rating['fic']
        if not is_fiction(book['genre']):
            relevant_x = relevant_x['nonfic']
            relevant_rating = relevant_rating['nonfic']
        relevant_x.append(i+1)
        relevant_rating.append(book['average_rating'])
    trace_avg_up_nonfic = build_scatter(
        x_avg['up']['nonfic'], 
        ratings_avg['up']['nonfic'], 
        None, 
        'triangle-up',
        nonfic_color[:-2] + '.5)',
    )
    trace_avg_up_fic = build_scatter(
        x_avg['up']['fic'], 
        ratings_avg['up']['fic'], 
        None, 
        'triangle-up',
        fic_color[:-2] + '.5)',
    )
    trace_avg_down_nonfic = build_scatter(
        x_avg['down']['nonfic'], 
        ratings_avg['down']['nonfic'], 
        None, 
        'triangle-down',
        nonfic_color,
    )
    trace_avg_down_fic = build_scatter(
        x_avg['down']['fic'], 
        ratings_avg['down']['fic'], 
        None, 
        'triangle-down',
        fic_color,
    )
    return [trace_avg_up_nonfic, trace_avg_up_fic, trace_avg_down_nonfic, \
            trace_avg_down_fic]
def build_legend():
    '''
        Builds a legend using a scatter plot data trace.
    '''
    return go.Scatter(
        x=[15, 15],
        y=[3, 2.9],
        marker = dict(
            size = [10, 10],
            color = [fic_color, nonfic_color],
        ),
        mode='markers+text',
        name='Markers and Text',
        text=['Fiction', 'Non-Fiction'],
        textposition='right',
        textfont=dict(
            family='Open Sans, monospace',
            size=14,
            color=black_rgba(),
        ),
        hoverinfo='none',
    )

def build_axis(range_min, range_max, title, titlefont):
    '''
        Returns an axis configuration dictionary for use in a plotly layout.
    '''
    return dict(
        range=[range_min, range_max],
        title=title,
        titlefont=titlefont,
        showgrid=False,
        zeroline = False,
        showline=False,
        autotick=True,
        ticks='',
        showticklabels=False
    )
    
def build_scatter(x, y, text, symbol, color):
    '''
        Return a data trace with certain parameters set to the input arguments.
    '''
    return go.Scatter(
        x=x,
        y=y,
        mode='markers',
        text=text,
        hoverinfo="text", # this disables the coordinate info
        marker=dict(
            size = 10,
            symbol = symbol,
            color = color,
        ),
    )

def build_arrows(books, shapes):
    '''
        Construct the arrows using shapes.
    '''
    for i in range(len(books)):
        book = books[i]
        arrow_color = fic_color if is_fiction(book['genre']) else nonfic_color
        # upward arrows have a lower opacity for easier reading of the chart
        if book['rating'] < book['average_rating']:
            arrow_color = arrow_color[:-2] + '.5)'
        shapes.append({
            'type': 'line',
            'x0': i+1,
            'y0': book['average_rating'],
            'x1': i+1,
            'y1': book['rating'],
            'line': {
                'color': arrow_color,
                'width': 2,
            },
        })

    
    
    
