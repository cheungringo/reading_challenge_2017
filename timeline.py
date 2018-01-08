# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 20:54:03 2018

@author: Ringo
"""
padding = 0.05
from math import pi, sqrt
from helpers import partition_books_by_month, black_rgba, get_credentials, \
    fic_color_rgba, nonfic_color_rgba, get_color_fic, build_info
import plotly
import plotly.graph_objs as go

creds = get_credentials("creds.json")
plotly.tools.set_credentials_file(username=creds[0], api_key=creds[1])

def timeline(books):
    '''
        Builds a bubble chart where the y axis is month and the x axis is date.
        The size of the bubbles is proportional to the word count of the book.
        The color of the bubble represents fiction or non-fiction.
        Book information is displayed on hover.
    '''
    x, y, hover_text, marker_colors, marker_sizes = [], [], [], [], []
    partitioned_books = partition_books_by_month(books)
    construct_geometry(partitioned_books, wordcount_area_ratio(books),\
        marker_colors, marker_sizes, x, y, hover_text)
    trace_title = build_title('Reading Timeline 2017', 0.5, 12.2)
    trace_axes_labels = build_axes_labels()
    trace_legend = build_legend()
    trace_data = go.Scatter(
        x=x,
        y=y,
        text=hover_text,
        hoverinfo="text", # this disables the coordinate info
        mode='markers',
        marker = dict(
            color = marker_colors, 
            size = marker_sizes,
            sizemode = "area",
        ),
    )
    data = [trace_title, trace_axes_labels, trace_legend, trace_data]
    fig = go.Figure(
        data=data,
        layout=build_layout(),
    )
    fig = plotly.offline.plot(fig, filename='reading-timeline.html')

def build_title(title, title_x, title_y):
    '''
        Since we are using a custom sized grid, need to position the title 
        more precisely so use a trace for this where the marker is invisible 
        and the text is to the right.
    '''
    return go.Scatter(
        x=[title_x],
        y=[title_y],
        marker = dict(
            size = 30,
            color = 'rgba(0, 0, 0, 0)',
        ),
        mode='markers+text',
        name='Markers and Text',
        text=[title],
        textposition='right',
        textfont=dict(
            family='Open Sans, monospace',
            size=17,
            color=black_rgba(),
        ),
        hoverinfo='none',
    )

def build_axes_labels():
    '''
        Roll our own custom axes labels so we can specify where to put them 
        on the grid.
    '''
    return go.Scatter(
        x=[0 for x in range(12)],
        y=[11.5 - x for x in range(12)],
        marker = dict(
            size = 10,
            color = 'rgba(0, 0, 0, 0)',
        ),
        mode='markers+text',
        name='Markers and Text',
        text=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', \
              'Oct', 'Nov', 'Dec'],
        textposition='left',
        textfont=dict(
            family='Open Sans, monospace',
            size=14,
            color=black_rgba(),
        ),
        hoverinfo='none',
    )

def build_legend():
    '''
        Make a custom legend to specify fiction and non-fiction bubbles
    '''
    return go.Scatter(
        x=[5, 5],
        y=[4, 3.6],
        marker = dict(
            size = [20, 20],
            color = [fic_color_rgba(), nonfic_color_rgba()],
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

def build_layout():
    '''
        Set the grid to be a square so that the bubbles look nice.
        Turn off axes grid, ticks and lines. Set the font.
    '''
    axis = dict(
        range=[-1, 13],
        showgrid=False,
        zeroline = False,
        showline=False,
        autotick=True,
        ticks='',
        showticklabels=False
    )
    return go.Layout(
        yaxis=axis,
        xaxis=axis,
        width=1000,
        height=1000,
        hovermode= 'closest',
        showlegend=False,
        font=dict(
            family='Open Sans, monospace',
        ),
    )

def wordcount_area_ratio(books):
    '''
        compute the wordcount to area ratio considering that the largest circle
        can only have an area of (pi/4)*(1-2*padding)**2
    '''
    max_area = (pi/4)*(1-2*padding)**2
    longest_book = max(books, key=lambda x: x['word_count'])
    return max_area/longest_book['word_count']

def construct_geometry(books_by_month, ratio, marker_colors, marker_sizes, x_centers, y_centers, hover_text):
    '''
        expects books_by_month to be a list of lists, the first list represents
        months, books_by_month[i] gives a list of books read at month [i] where 
        i = 0 is Jan and i = 11 is Dec. Using the area:wordcount ratio, this 
        function will construct shapes by assigning them the appropriate 
        positions, colors, labels based on genre. y-axis represents month, 
        x-axis is day within month
    '''
    center_y = 11.5 # this gets incremented every month
    for cur_month_books in books_by_month:
        left_x = 0+padding # the lower y coordinate of the circle
        for book in cur_month_books:
            color = get_color_fic(book['genre'])
            area = ratio*book['word_count']
            marker_colors.append(color)
            diameter = sqrt(4*area/pi)
            marker_sizes.append(area*2500)
            hover_text.append(build_info(book))
            x_centers.append(left_x+diameter/2)
            y_centers.append(center_y)
            left_x = left_x + diameter + 2*padding
        center_y = center_y - 1
    return