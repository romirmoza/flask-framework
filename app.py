import quandl
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def drawplot(col, tick):
    quandl.ApiConfig.api_key = 'j2d-o1VPfbxdbifUEsLj'
    data = quandl.get_table('WIKI/PRICES', ticker = tick,
                qopts = { 'columns': ['ticker', 'date', col] },
                date = { 'gte': '2016-12-31', 'lte': '2017-12-31' },
                paginate=True)
    x = data['date']
    y = data[col]
    p = figure(plot_width=1200, plot_height=375, x_axis_type="datetime")
    p.line(x,y)
    return p

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        tick = request.form['ticker']
        col = request.form['options']
        p = drawplot(col,tick)
        script, div = components(p)
        return render_template('graph.html', script=script, div=div)
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')


if __name__ == '__main__':
    app.run(port=33507)
