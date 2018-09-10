import requests
import datetime
import pandas as pd 
import numpy as np
from flask import Flask,render_template,request,redirect,session
from bokeh.plotting import figure
from bokeh.palettes import Spectral11
from bokeh.embed import components 

app = Flask(__name__)

app.vars={}


@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
    
@app.route('/graph', methods=['POST'])
def graph():
    
    url ='https://api.iextrading.com/1.0/stock/%s/chart/%s' % (request.form['ticker'],request.form['period'])
    df=pd.DataFrame(requests.get(url).json())
    df=df[['date','open','high','low','close']]
    df['date'] = df['date'].astype(np.datetime64) 
    period_map={'1m': '1 Month','3m': '3 Months','6m': '6 Months',\
                '1y': '1 Year','2y': '2 Years','5y': '5 Years'}
    p = figure(title='%s Stock prices for %s' % (period_map[request.form['period']],request.form['ticker']),\
               x_axis_label='date',x_axis_type='datetime',y_axis_label='prices (in USD)',\
               plot_width=1000,plot_height=500)
    a=p.line(x=df['date'].values, y=df['open'].values,line_width=3,line_alpha=0.6, legend='%s: open' % request.form['ticker'])
    b=p.line(x=df['date'].values, y=df['close'].values,line_width=3,line_alpha=0.6, line_color="purple", legend='%s: close' % request.form['ticker'])
    c=p.line(x=df['date'].values, y=df['high'].values,line_width=3,line_alpha=0.6, line_color="green", legend='%s: high' % request.form['ticker'])
    d=p.line(x=df['date'].values, y=df['low'].values,line_width=3,line_alpha=0.6, line_color="red", legend='%s: low' % request.form['ticker'])

    a.visible=b.visible=c.visible=d.visible=False
    
    if request.form.get('open'):
        a.visible=True
    if request.form.get('close'):
        b.visible=True
    if request.form.get('high'):
        c.visible=True
    if request.form.get('low'):
        d.visible=True
        
    p.legend.location = "top_left"
    p.legend.click_policy="hide"
    
    script, div = components(p)
    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)