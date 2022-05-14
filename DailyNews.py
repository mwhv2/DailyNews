import requests
import json
from requests.exceptions import ConnectionError
import datetime
import pandas as pd
import plotly.express as px
import feedparser
import os

nope = "Image not available"

# Set the current date and time
now1 = datetime.datetime.now()
update = now1.strftime("%H:%M")
now = now1.strftime("%A, %B %d, %Y")

# This API key is for NewsAPI. Documentation here: https://newsapi.org/docs
key = os.environ.get('API_KEY')

# For top headlines and science in the US
#re1_url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=10&apiKey={key}"
re1_url = f"https://newsapi.org/v2/top-headlines?sources=associated-press,bbc-news,al-jazeera-english&pageSize=10&apiKey={key}"
response = requests.get(re1_url)
response = response.json()

s_url = f"https://newsapi.org/v2/top-headlines?country=us&category=science&pageSize=10&apiKey={key}"
s_res = requests.get(s_url)
s_res = s_res.json()

t_url = f"https://newsapi.org/v2/top-headlines?country=us&category=technology&pageSize=10&apiKey={key}"
t_res = requests.get(t_url)
t_res = t_res.json()

# Top headlines in France
fr_url = f"https://newsapi.org/v2/top-headlines?country=fr&pageSize=10&apiKey={key}"
fr_res = requests.get(fr_url)
fr_res = fr_res.json()

# Get link to NPR Hourly News summary
npr = feedparser.parse("https://feeds.npr.org/500005/podcast.xml")
npr_image = npr['feed']['image']['href']
npr_url = npr['entries'][0]['links'][0]['href']

# Get the more recent Short Wave podcast
short = feedparser.parse("https://feeds.npr.org/510351/podcast.xml")
short_img = short['feed']['image']['href']
short_url = short['entries'][0]['links'][1]['href']

# Get most recent Scientific American 60-second science podcast
sciam = feedparser.parse("http://rss.sciam.com/sciam/60secsciencepodcast?format=xml")
sciam_img = "https://static.scientificamerican.com/sciam/cache/file/42C04BF1-2ED5-44D9-A29114A15A9BDF42_source.jpg"
sci_url = sciam['entries'][0]['links'][1]['href']

# Get the hourly French news from rfi.fr
rfi = feedparser.parse("https://www.rfi.fr/fr/podcasts/journal-fran%C3%A7ais-facile/podcast")
rfi = rfi['entries'][0]['links'][1]['href']
rfi_img = "https://overcast.fm/art/full/1971980?4"

# National Weather Service 5 day forecast (3 hour intervals)
# Current location is set to Wooster, OH. This requires
# latitude and longitude info.
init_url = "https://api.weather.gov/points/40.80,-81.93"
resp = requests.get(init_url)
resp = resp.json()
forecast_url = resp['properties']['forecastHourly']
forecast = requests.get(forecast_url)
forecast = forecast.json()
try:
    periods = forecast['properties']['periods']
except KeyError:
    forecast = requests.get(forecast_url)
    forecast = forecast.json()
    periods = forecast['properties']['periods']

df = pd.DataFrame()
for i in periods:
    dt = pd.to_datetime(i['startTime'])
    temp = i['temperature']
    short = i['shortForecast']
    df = df.append([[dt,temp,short]])
df.columns = ["Date",u'Temperature \u00B0F',"Short"]
df.set_index("Date",inplace=True)

fig = px.line(df,x=df.index, y=u'Temperature \u00B0F',
              hover_data=[u'Temperature \u00B0F',"Short"])
fig.add_hline(y=32,line_width=1)
fig.update_layout(hovermode='x', template="seaborn", hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)'))
fig.update_traces(line_color='#ff7f0e')
fig.add_annotation(xref="paper", x="0", yref="paper",
                   y="-0.2",
                   text="""<a href="https://www.weather.gov/" target="_blank">Data from the National Weather Service</a>""",
                   showarrow=False)
fig.write_html("NWSforecast.html")

# Get most recent screenshot of the Sun at 171 Ang.
current = now1.strftime("%Y-%m-%dT%H:%M:%SZ")
try:
    ide = requests.get(f"https://api.helioviewer.org/v2/getClosestImage/?date={current}&sourceId=10")
    d = ide.json()['date'].replace(' ','T')
    Sun_im = f"https://api.helioviewer.org/v2/takeScreenshot/?date={d}Z&imageScale=5&layers=[SDO,AIA,AIA,171,1,100]&x0=0&y0=0&width=500&height=500&display=true"
except ConnectionError:
    Sun_im = ""

# Initialize and build lists of stories to be written onto html page
A = [0,1,3,5,7]
B = [1,2,4,6,8]
Text = ""
for i in range(int(len(response['articles'])/2)):
    r1 = response['articles'][A[i]]
    r2 = response['articles'][B[i]]
    if i == 0:
        Text = Text + f"""
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="embed-responsive embed-responsive-4by3 d-flex justify-content-center">
                        <video controls poster={npr_image} width="40%">
                                <source src={npr_url} type="audio/mpeg">
                        </video>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r1['url']}" target="_blank">{r1['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r1['description']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r1['url']}" target="_blank">
                        <img class="img-thumbnail" src = "{r1['urlToImage']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        """
    else:
        Text = Text + f"""
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r1['url']}" target="_blank">{r1['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r1['description']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r1['url']}" target="_blank">
                        <img class="img-thumbnail" src = "{r1['urlToImage']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r2['url']}" target="_blank">{r2['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r2['description']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r2['url']}" target="_blank">
                        <img class="img-thumbnail" src = "{r2['urlToImage']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        """

Fr_Text = ""
for i in range(int(len(fr_res['articles'])/2)):
    r1 = fr_res['articles'][A[i]]
    r2 = fr_res['articles'][B[i]]
    if i == 0:
        Fr_Text = Fr_Text + f"""
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="embed-responsive embed-responsive-4by3 d-flex justify-content-center">
                        <video controls poster={rfi_img} width="40%">
                                <source src={rfi} type="audio/mpeg">
                        </video>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r1['url']}" target="_blank">{r1['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r1['description']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r1['url']}" target="_blank">
                        <img class="img-thumbnail" src = "{r1['urlToImage']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        """
    else:
        Fr_Text = Fr_Text + f"""
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r1['url']}" target="_blank">{r1['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r1['description']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r1['url']}" target="_blank">
                        <img class="img-thumbnail" src = "{r1['urlToImage']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r2['url']}" target="_blank">{r2['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r2['description']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r2['url']}" target="_blank">
                        <img class="img-thumbnail" src = "{r2['urlToImage']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        """

A = [0,2,4,6,8]
B = [1,3,5,7,9]
Science_Text = ""
for i in range(int(len(s_res['articles'])/2)):
    r1 = s_res['articles'][A[i]]
    r2 = s_res['articles'][B[i]]
    if i == 4:
        Science_Text = Science_Text + f"""
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="embed-responsive embed-responsive-4by3 d-flex justify-content-center">
                        <video controls poster={short_img} width="40%">
                                <source src={short_url} type="audio/mpeg">
                        </video>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="embed-responsive embed-responsive-4by3 d-flex justify-content-center">
                        <video controls poster={sciam_img} width="40%">
                                <source src={sci_url} type="audio/mpeg">
                        </video>
                    </div>
                </div>
            </div>
        </div>
        """
    else:
        Science_Text = Science_Text + f"""
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r1['url']}" target="_blank">{r1['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r1['description']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r1['url']}" target="_blank">
                        <img class="img-thumbnail" src = "{r1['urlToImage']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r2['url']}" target="_blank">{r2['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r2['description']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r2['url']}" target="_blank">
                        <img class="img-thumbnail" src = "{r2['urlToImage']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        """

Tech_Text = ""
for i in range(int(len(t_res['articles'])/2)):
    r1 = t_res['articles'][A[i]]
    r2 = t_res['articles'][B[i]]
    Tech_Text = Tech_Text + f"""
    <div class="row mb-3">
        <div class="col-md-6">
            <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                <div class="col-sm-7 p-3 d-flex flex-column position-static">
                    <h5 class="mb-1">
                    <a href="{r1['url']}" target="_blank">{r1['title']}</a>
                    </h5>
                    <p class="card-text mb-auto">{r1['description']}</p>
                </div>
                <div class="col-sm-5 rounded">
                    <a href="{r1['url']}" target="_blank">
                    <img class="img-thumbnail" src = "{r1['urlToImage']}" alt="{nope}"/>
                    </a>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                <div class="col-sm-7 p-3 d-flex flex-column position-static">
                    <h5 class="mb-1">
                    <a href="{r2['url']}" target="_blank">{r2['title']}</a>
                    </h5>
                    <p class="card-text mb-auto">{r2['description']}</p>
                </div>
                <div class="col-sm-5 rounded">
                    <a href="{r2['url']}" target="_blank">
                    <img class="img-thumbnail" src = "{r2['urlToImage']}" alt="{nope}"/>
                    </a>
                </div>
            </div>
        </div>
    </div>
    """


f_html = open('index.html','w',encoding="utf-8")

html_template = f"""
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="">
        <meta name="author" content="Mark Otto, Jacob Thornton, and Bootstrap contributors">
        <meta name="generator" content="Hugo 0.88.1">
        <title>The Daily News</title>

        <link href="bootstrap.min.css" rel="stylesheet">

    <style>
      .bd-placeholder-img {{
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }}

      @media (min-width: 768px) {{
        .bd-placeholder-img-lg {{
          font-size: 3.5rem;
        }}
      }}
    </style>
    
    <link href="https://fonts.googleapis.com/css?family=Playfair&#43;Display:700,900&amp;display=swap" rel="stylesheet">
    <link href="blog.css" rel="stylesheet">
  </head>
  <body>
    
<div class="container">
  <header class="blog-header py-3">
    <div class="align-items-center">
      <div class="text-center">
        <p class="blog-header-logo text-dark" href="#">The Daily News</p>
	<p>{now}</p>
      </div>
    </div>
  </header>
</div>

<div class="container">
  <div class="nav-scroller py-1 mb-2">
    <nav class="nav d-flex justify-content-between">
      <a class="p-2 link-secondary" href="#top">Top Headlines</a>
      <a class="p-2 link-secondary" href="#science">Science</a>
      <a class="p-2 link-secondary" href="#france">French News</a>
      <a class="p-2 link-secondary" href="#tech">Technology</a>
      <a class="p-2 link-secondary" href="#weather">Weather</a>
    </nav>
  </div>
</div>

<main class="container">
<h3 class="py-2"><a id="top">Top Headlines</a></h3>
""" + Text + f"""
</main>

<main class="container">
<h3 class="py-2"><a id="science">Science</a></h3>
""" + Science_Text + f"""
</main>

<main class="container">
<h3 class="py-2"><a id="france">French News</a></h3>
""" + Fr_Text + f"""
</main>

<main class="container">
<h3 class="py-2"><a id="tech">Technology</a></h3>
""" + Tech_Text + f"""
</main>

<main class="container">
<h3 class="py-2"><a id="weather">Seven Day Forecast and Current SDO View at 171&#8491</a></h3>
<div class="row mb-3">
    <div class="col-md-8">
        <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
            <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless"
            src="NWSforecast.html" height="525" width="100%"></iframe>
        </div>
    </div>
    <div class="col-md-4">
        <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
            <a href="https://helioviewer.org/" target="_blank">
            <img src={Sun_im} alt="Latest SDO image not available" style="width:97%"></a>
        </div>
    </div>
</div>
</main>

<footer class="blog-footer">
  <p>Last updated at {update} UTC. Created by <a href="https://mwhv2.github.io/" target="_blank">Matt Wentzel-Long</a>.
  <br><a href="#">Back to top</a></p>
</footer>

</body>
</html>
"""

f_html.write(html_template)
f_html.close()
