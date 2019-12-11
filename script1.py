#udemy did not have this import, but server did not work without it
import flask

from flask import Flask, render_template

#name of python script
app=Flask(__name__)

@app.route('/plot/')
def plot():
    import pandas as pd
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start=datetime.datetime(2017,3,1)
    end=datetime.datetime(2017,9,10)

    df=data.DataReader(name="MORN", data_source="yahoo", start=start,end=end)

    def updown(c,o):
        if c > o:
            value="Increase"
        elif c < o:
            value="Decrease"
        else:
            value="Equal"
        return value

    df["Status"]=[updown(c,o) for c,o in zip(df.Close,df.Open)]
    df["Midpoint"]=(df.Open+df.Close)/2
    df["Range"]=abs(df.Open-df.Close)

    p=figure(x_axis_type='datetime',width=1000,height=300, sizing_mode="scale_width")
    p.title.text="Candlestick Chart for MORN"
    p.grid.grid_line_alpha=0.45

    #converts to miliseconds for x axis scaling
    hours_12=12*60*60*1000
    p.segment(df.index,df.High,df.index,df.Low, color="black")
    p.rect(df.index[df.Status=="Increase"],df.Midpoint[df.Status=="Increase"],hours_12, df.Range[df.Status=="Increase"], fill_color="green",line_color="black")
    p.rect(df.index[df.Status=="Decrease"],df.Midpoint[df.Status=="Decrease"],hours_12, df.Range[df.Status=="Decrease"], fill_color="red",line_color="black")

    script1, div1 = components(p)
    cdn_js = CDN.js_files

    return render_template("plot.html",
    script1=script1,
    div1=div1,
    cdn_js=cdn_js[0])

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
