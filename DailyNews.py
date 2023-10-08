import requests
import json
from requests.exceptions import ConnectionError
import datetime
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import feedparser
import os
from bs4 import BeautifulSoup

nope = "Image not available"

# Set the current date and time
now1 = datetime.datetime.now()
update = now1.strftime("%H:%M")
now = now1.strftime("%A, %B %d, %Y")

# This API key is for NewsAPI. Documentation here: https://newsapi.org/docs
key = os.environ.get('API_KEY')

# For top headlines and science in the US
re1_url = f"https://newsapi.org/v2/top-headlines?sources=associated-press,bbc-news,al-jazeera-english,le-monde,national-geographic&pageSize=8&apiKey={key}"
response = requests.get(re1_url)
response = response.json()

s_url = f"https://newsapi.org/v2/top-headlines?country=us&category=science&pageSize=10&apiKey={key}"
s_res = requests.get(s_url)
s_res = s_res.json()

t_url = f"https://newsapi.org/v2/top-headlines?sources=wired,ars-technica,engadget,ign,polygon&pageSize=8&apiKey={key}"
t_res = requests.get(t_url)
t_res = t_res.json()

# Space news from NASA and the ESA
skt = feedparser.parse('https://www.universetoday.com/feed/')
nasa = feedparser.parse("https://www.nasa.gov/rss/dyn/breaking_news.rss")
spc = feedparser.parse('https://www.space.com/home/feed/site.xml')
apod = feedparser.parse("https://apod.pixelweben.de/rss_en.xml")
space = skt['entries'][:2] + nasa['entries'][:2] + spc['entries'][:2]
apod = apod['entries'][0]
apod_soup = BeautifulSoup(apod['summary'], 'lxml')
apod_image = apod_soup.find('img')['src']

# Get link to NPR Hourly News summary
npr = feedparser.parse("https://feeds.npr.org/500005/podcast.xml")
npr_img = "https://media.npr.org/assets/img/2018/08/06/nprnewsnow_podcasttile_sq.webp?s=400&c=85"
npr_url = npr['entries'][0]['links'][0]['href']
npr_title = npr['entries'][0]['title']
npr_main = "https://www.npr.org/"

# Get the more recent Short Wave podcast
short = feedparser.parse("https://feeds.npr.org/510351/podcast.xml")
short_img = "https://media.npr.org/assets/img/2022/09/23/short-wave_tile_npr-network-01_sq-517382b4b8fd0ab48ea9c781253f9992eab733dc.jpg?s=400&c=85&f=webp"
short_url = short['entries'][0]['links'][0]['href']
short_title = short['entries'][0]['title']
short_trans = short['entries'][0]['links'][0]['href']
short_main = "https://www.npr.org/podcasts/510351/short-wave"

# Get most recent Scientific American 60-second science podcast
sciam = feedparser.parse("http://rss.sciam.com/sciam/60secsciencepodcast?format=xml")
sciam_img = "https://static.scientificamerican.com/sciam/cache/file/42C04BF1-2ED5-44D9-A29114A15A9BDF42_source.jpg"
try:
    sciam_url = sciam['entries'][0]['links'][1]['href']
except IndexError:
    sciam_url = sciam['entries'][1]['links'][1]['href']
sciam_title = sciam['entries'][0]['title']
sciam_trans = sciam['entries'][0]['links'][0]['href']
sciam_main = "https://www.scientificamerican.com/"

# Get the hourly French news from rfi.fr
rfi = feedparser.parse("https://www.rfi.fr/fr/podcasts/journal-fran%C3%A7ais-facile/podcast")
rfi_url = rfi['entries'][0]['links'][1]['href']
rfi_img = "https://overcast.fm/art/full/1971980?4"
rfi_title = rfi['entries'][0]['title']
rfi_main = "https://www.rfi.fr/fr/"

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
    df = pd.DataFrame()
    for i in periods:
        dt = pd.to_datetime(i['startTime'])
        temp = i['temperature']
        short = i['shortForecast']
        dew = i['dewpoint']['value']*9/5+32
        temp = pd.DataFrame({'Date': [dt],
                             u'Temperature \u00B0F': [temp],
                             'Short': [short], 
                             'Dewpoint \u00B0F': [dew]})
        df = pd.concat([df, temp])
    df.set_index("Date",inplace=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(px.line(df,x=df.index,y=u'Temperature \u00B0F',hover_data=[u'Temperature \u00B0F',"Short"]).data[0],
                 secondary_y=False) 
    fig.update_traces(line_color='#ff7f0e')
    fig.update_yaxes(title='Temperature \u00B0F', secondary_y=False)
    fig.add_trace(px.line(df, x=df.index, y='Dewpoint \u00B0F').data[0],
        secondary_y=True,)
    fig.update_yaxes(title='Dewpoint \u00B0F', secondary_y=True)
    fig.add_hline(y=32,line_width=1)
    fig.update_layout(hovermode='x',template="plotly_dark", hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)'))

    fig.update_layout(margin=dict(l=50, r=1, b=80, t=50))
    fig.add_annotation(xref="paper", x="0", yref="paper", y="-0.15",
                       text="""<a href="https://www.weather.gov/" target="_blank">Data from the National Weather Service</a>""",
                       showarrow=False)
    fig.write_html("NWSforecast.html")
except KeyError:
    pass


# Initialize and build lists of stories to be written onto html page
A = [0,2,4,6,8]
B = [1,3,5,7,9]
Text = ""
for i in range(int(len(response['articles'])/2)):
    r1 = response['articles'][A[i]]
    r2 = response['articles'][B[i]]
    if i == 0:
        Text = Text + f"""
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{npr_main}" target="_blank">{npr_title}</a>
                        </h5>
                        <p class="card-text mb-auto">The latest news in five minutes. Updated hourly.<audio controls><source src="{npr_url}" type="audio/mpeg"></audio></p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{npr_main}" target="_blank">
                        <img class="img-fluid" src = "{npr_img}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{rfi_main}" target="_blank">{rfi_title}</a>
                        </h5>
                        <p class="card-text mb-auto">Un vrai journal d’information pour suivre l’actualité internationale en français. \
                        <audio controls><source src="{rfi_url}" type="audio/mpeg"></audio></p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{rfi_main}" target="_blank">
                        <img class="img-fluid" src = "{rfi_img}" alt="{nope}"/>
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
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r1['url']}" target="_blank">{r1['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r1['description']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r1['url']}" target="_blank">
                        <img class="img-fluid" src = "{r1['urlToImage']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r2['url']}" target="_blank">{r2['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r2['description']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r2['url']}" target="_blank">
                        <img class="img-fluid" src = "{r2['urlToImage']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        """


A = [0,2,4,6,8]
B = [1,3,5,7,9]
Space_Text = ""
for i in range(4):
    if i < 3:
        r1 = space[A[i]]
        r2 = space[B[i]]
    if i == 0:
        soup1 = BeautifulSoup(r1['summary'], 'lxml')
        sum1 = soup1.get_text().split('\n')[0]
        url1 = r1['media_content'][0]['url']
        
        soup2 = BeautifulSoup(r2['summary'], 'lxml')
        sum2 = soup2.get_text().split('\n')[0]
        url2 = r2['media_content'][0]['url']
        
        Space_Text = Space_Text + f"""
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r1['link']}" target="_blank">{r1['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{sum1}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r1['link']}" target="_blank">
                        <img class="img-fluid" src = "{url1}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r2['link']}" target="_blank">{r2['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{sum2}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r2['link']}" target="_blank">
                        <img class="img-fluid" src = "{url2}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        """
    if i == 1:
        Space_Text = Space_Text + f"""
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r1['link']}" target="_blank">{r1['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r1['summary']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r1['link']}" target="_blank">
                        <img class="img-fluid" src = "{r1['links'][1]['href']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r2['link']}" target="_blank">{r2['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r2['summary']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r2['link']}" target="_blank">
                        <img class="img-fluid" src = "{r2['links'][1]['href']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        """
    if i == 2:
        
        Space_Text = Space_Text + f"""
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r1['link']}" target="_blank">{r1['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r1['summary']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r1['link']}" target="_blank">
                        <img class="img-fluid" src = "{r1['links'][1]['href']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r2['link']}" target="_blank">{r2['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r2['summary']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r2['link']}" target="_blank">
                        <img class="img-fluid" src = "{r2['links'][1]['href']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        """
    if i == 3:
        Space_Text = Space_Text + f"""
        <div class="row mb-3">
            <div class="col" align="center">
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center caption text-center">
                    <a href="{apod['link']}" target="_blank">
                    <img class="img-fluid" src = "{apod_image}" alt="{nope}"/>
                     </a>
                    <p>{apod['title']}</p>
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
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{short_main}" target="_blank">{short_title}</a>
                        </h5>
                        <p class="card-text mb-auto">New discoveries, everyday mysteries, and the science behind the headlines — all in about 10 minutes, every weekday. \
                        <a href="{short_trans}" target="_blank">Transcript</a><audio controls><source src="{short_url}" type="audio/mpeg"></audio></p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{short_main}" target="_blank">
                        <img class="img-fluid" src = "{short_img}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{sciam_main}" target="_blank">{sciam_title}</a>
                        </h5>
                        <p class="card-text mb-auto">Tune in every week for rapid reports from the world of science—we'll make it quick and fascinating. \
                        <a href="{sciam_trans}" target="_blank">Transcript</a><audio controls><source src="{sciam_url}" type="audio/mpeg"></audio></p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{sciam_main}" target="_blank">
                        <img class="img-fluid" src = "{sciam_img}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        """
    else:
        Science_Text = Science_Text + f"""
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r1['url']}" target="_blank">{r1['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r1['description']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r1['url']}" target="_blank">
                        <img class="img-fluid" src = "{r1['urlToImage']}" alt="{nope}"/>
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                    <div class="col-sm-7 p-3 d-flex flex-column position-static">
                        <h5 class="mb-1">
                        <a href="{r2['url']}" target="_blank">{r2['title']}</a>
                        </h5>
                        <p class="card-text mb-auto">{r2['description']}</p>
                    </div>
                    <div class="col-sm-5 rounded">
                        <a href="{r2['url']}" target="_blank">
                        <img class="img-fluid" src = "{r2['urlToImage']}" alt="{nope}"/>
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
            <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                <div class="col-sm-7 p-3 d-flex flex-column position-static">
                    <h5 class="mb-1">
                    <a href="{r1['url']}" target="_blank">{r1['title']}</a>
                    </h5>
                    <p class="card-text mb-auto">{r1['description']}</p>
                </div>
                <div class="col-sm-5 rounded">
                    <a href="{r1['url']}" target="_blank">
                    <img class="img-fluid" src = "{r1['urlToImage']}" alt="{nope}"/>
                    </a>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                <div class="col-sm-7 p-3 d-flex flex-column position-static">
                    <h5 class="mb-1">
                    <a href="{r2['url']}" target="_blank">{r2['title']}</a>
                    </h5>
                    <p class="card-text mb-auto">{r2['description']}</p>
                </div>
                <div class="col-sm-5 rounded">
                    <a href="{r2['url']}" target="_blank">
                    <img class="img-fluid" src = "{r2['urlToImage']}" alt="{nope}"/>
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

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
    
    <link href="https://fonts.googleapis.com/css?family=Playfair&#43;Display:700,900&amp;display=swap" rel="stylesheet">
    <link href="blog.css" rel="stylesheet">
  </head>
  <body>
    
<div class="container">
  <header class="blog-header py-3">
    <div class="align-items-center">
      <div class="text-center">
        <p class="blog-header-logo" href="#">The Daily News</p>
	<p>{now}</p>
      </div>
    </div>
  </header>
</div>

<div class="container-md">
  <div class="nav-scroller py-1 mb-2">
    <nav class="nav d-flex justify-content-between">
      <a class="p-2 link-secondary" href="#top">Headlines</a>
      <a class="p-2 link-secondary" href="#space">Space</a>
      <a class="p-2 link-secondary" href="#science">Science</a>
      <a class="p-2 link-secondary" href="#tech">Technology</a>
      <a class="p-2 link-secondary" href="#weather">Weather</a>
    </nav>
  </div>
</div>

<main class="container">
<h3 class="py-2"><a id="top">Headlines</a></h3>
""" + Text + f"""
</main>

<main class="container">
<h3 class="py-2"><a id="space">Space</a></h3>
""" + Space_Text + f"""
</main>

<main class="container">
<h3 class="py-2"><a id="science">Science</a></h3>
""" + Science_Text + f"""
</main>

<main class="container">
<h3 class="py-2"><a id="tech">Technology</a></h3>
""" + Tech_Text + f"""
</main>

<main class="container">
<h3 class="py-2"><a id="weather">Seven Day Forecast and Current SDO Views</a></h3>
<div class="row mb-3">
    <div class="col-md-7">
        <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
            <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless"
            src="NWSforecast.html" height="525" width="100%"></iframe>
        </div>
    </div>
    <div class="col-md-5">
        <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
            <div class="carousel slide" data-bs-ride="carousel" id="carousel">
                <div class="carousel-indicators">
                    <button type="button" data-bs-target="#carousel" data-bs-slide-to="0" class="active"></button>
                    <button type="button" data-bs-target="#carousel" data-bs-slide-to="1"></button>
                    <button type="button" data-bs-target="#carousel" data-bs-slide-to="2"></button>
                    <button type="button" data-bs-target="#carousel" data-bs-slide-to="3"></button>
                </div>
                <div class="carousel-inner">
                    <div class="carousel-item active">
                        <img src="https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_1600.jpg" class="d-block w-100">
                    </div>
                    <div class="carousel-item">
                        <img src="http://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0335.jpg" class="d-block w-100">
                    </div>
                    <div class="carousel-item">
                        <img src="http://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0171.jpg" class="d-block w-100">
                    </div>
                    <div class="carousel-item">
                        <img src="http://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0094.jpg" class="d-block w-100">
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<div class="row mb-3 embed-responsive">
    <iframe src='https://mars.nasa.gov/layout/embed/image/mslweather/' height='630' scrolling='no' frameborder='0'></iframe>
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
