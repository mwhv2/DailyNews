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
import re

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

s_url = f"https://newsapi.org/v2/top-headlines?country=us&category=science&pageSize=6&apiKey={key}"
s_res = requests.get(s_url)
s_res = s_res.json()

#Custom technology section
wired = feedparser.parse('https://www.wired.com/feed/rss')
ars = feedparser.parse('https://feeds.arstechnica.com/arstechnica/index')
eng = feedparser.parse('https://www.engadget.com/rss.xml')

esoup0 = BeautifulSoup(eng['entries'][0]['summary'])
sent0 = re.split(r'[.!?]', esoup0.text)[0]

esoup1 = BeautifulSoup(eng['entries'][1]['summary'])
sent1 = re.split(r'[.!?]', esoup1.text)[0]

tech = [{'title': wired['entries'][0]['title'],
         'link': wired['entries'][0]['link'], 
         'summary': wired['entries'][0]['summary'],
         'url': wired['entries'][0]['media_thumbnail'][0]['url']},
        {'title': wired['entries'][1]['title'],
         'link': wired['entries'][1]['link'], 
         'summary': wired['entries'][1]['summary'],
         'url': wired['entries'][1]['media_thumbnail'][0]['url']},
        {'title': ars['entries'][0]['title'],
         'link': ars['entries'][0]['link'], 
         'summary': ars['entries'][0]['summary'],
         'url': ars['entries'][0]['media_thumbnail'][0]['url']},
        {'title': ars['entries'][1]['title'],
         'link': ars['entries'][1]['link'], 
         'summary': ars['entries'][1]['summary'],
         'url': ars['entries'][1]['media_thumbnail'][0]['url']},
        {'title': eng['entries'][0]['title'],
         'link': eng['entries'][0]['link'], 
         'summary': sent0,
         'url': eng['entries'][0]['media_content'][0]['url']},
        {'title': eng['entries'][1]['title'],
         'link': eng['entries'][1]['link'], 
         'summary': sent1,
         'url': eng['entries'][1]['media_content'][0]['url']},]


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
try:
    short_url = short['entries'][0]['links'][1]['href']
except IndexError:
    short_url = short['entries'][0]['links'][0]['href']
short_title = short['entries'][0]['title']
short_trans = short['entries'][0]['links'][0]['href']
short_main = "https://www.npr.org/podcasts/510351/short-wave"

# Get most recent Scientific American 60-second science podcast
sciam = feedparser.parse("http://rss.sciam.com/sciam/60secsciencepodcast?format=xml")
sciam_img = "https://static.scientificamerican.com/sciam/cache/file/6E8467DF-0688-4D4F-95E46E6B82CC3912_source.jpg"
try:
    sciam_url = sciam['entries'][0]['links'][0]['href']
except IndexError:
    sciam_url = sciam['entries'][1]['links'][1]['href']
sciam_title = sciam['entries'][0]['title']
sciam_trans = sciam['entries'][0]['links'][0]['href']
sciam_main = "https://www.scientificamerican.com/"

# Get the hourly French news from rfi.fr
try:
    rfi = feedparser.parse("https://www.rfi.fr/fr/podcasts/journal-fran%C3%A7ais-facile/podcast")
    rfi_url = rfi['entries'][0]['links'][1]['href']
except IndexError:
    rfi = feedparser.parse("https://apis.fle.rfi.fr/products/get_product/fle_getpodcast_by_nid_author_rfi?token_application=applepodcast_fle&program.entrepriseId=WBMZ39-FLE-FR-20220627")
    rfi_url = rfi['entries'][0]['links'][1]['href']
rfi_img = "https://overcast.fm/art/full/1971980?4"
rfi_title = rfi['entries'][0]['title']
rfi_main = "https://www.rfi.fr/fr/"

# Get food and travel from NYTimes
food_backup = 'https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?q=80&w=1964&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
trav_backup = 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
trav = feedparser.parse('https://www.nytimes.com/services/xml/rss/nyt/Travel.xml')
food = feedparser.parse('https://rss.nytimes.com/services/xml/rss/nyt/DiningandWine.xml')
try:
    food['entries'][0]['media_content'][0]['url']
except KeyError:
    food['entries'][0]['media_content'] = [{'url': food_backup}]
try:
    food['entries'][1]['media_content'][0]['url']
except KeyError:
    food['entries'][1]['media_content'] = [{'url': food_backup}]

try:
    trav['entries'][0]['media_content'][0]['url']
except KeyError:
    trav['entries'][0]['media_content'] = [{'url': trav_backup}]
try:
    trav['entries'][1]['media_content'][0]['url']
except KeyError:
    trav['entries'][1]['media_content'] = [{'url': trav_backup}]

cnn = feedparser.parse('http://rss.cnn.com/rss/cnn_travel.rss')
f_n_t = [{'title': food['entries'][0]['title'],
         'link': food['entries'][0]['link'], 
         'summary': food['entries'][0]['summary'],
         'url': food['entries'][0]['media_content'][0]['url']},
        {'title': food['entries'][1]['title'],
         'link': food['entries'][1]['link'], 
         'summary': food['entries'][1]['summary'],
         'url': food['entries'][1]['media_content'][0]['url']},
        {'title': trav['entries'][0]['title'],
         'link': trav['entries'][0]['link'], 
         'summary': trav['entries'][0]['summary'],
         'url': trav['entries'][0]['media_content'][0]['url']},
        {'title': trav['entries'][1]['title'],
         'link': trav['entries'][1]['link'], 
         'summary': trav['entries'][1]['summary'],
         'url': trav['entries'][1]['media_content'][0]['url']},
        {'title': cnn['entries'][0]['title'],
         'link': cnn['entries'][0]['link'], 
         'summary': cnn['entries'][0]['summary'],
         'url': cnn['entries'][0]['media_content'][0]['url']},
        {'title': cnn['entries'][1]['title'],
         'link': cnn['entries'][1]['link'], 
         'summary': cnn['entries'][1]['summary'],
         'url': cnn['entries'][1]['media_content'][0]['url']},]

data = feedparser.parse('https://ourworldindata.org/atom-data-insights.xml')
dlink = data['entries'][0]['link']
dsoup = BeautifulSoup(data['entries'][0]['content'][0]['value'])
dtext = dsoup.text
dimg = dsoup.find('img')['src']

# National Weather Service 5 day forecast (3 hour intervals)
# Current location is set to Wooster, OH. This requires
# latitude and longitude info.
try:
    init_url = "https://api.weather.gov/points/40.80,-81.93"
    resp = requests.get(init_url)
    resp = resp.json()
    forecast_url = resp['properties']['forecastHourly']
    forecast = requests.get(forecast_url)
    forecast = forecast.json()
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

    init_url = "https://api.weather.gov/points/38.79,-90.49"
    # Request for information using St. Charles MO Lat and Long
    resp = requests.get(init_url)

    resp = resp.json()
    forecast_url = resp['properties']['forecastHourly']

    forecast = requests.get(forecast_url)
    forecast = forecast.json()

    periods = forecast['properties']['periods']

    df2 = pd.DataFrame()
    for i in periods:
        dt = pd.to_datetime(i['startTime'])
        temp = i['temperature']
        short = i['shortForecast']
        dew = i['dewpoint']['value']*9/5+32
        temp = pd.DataFrame({'Date': [dt],
                             u'Temperature \u00B0F': [temp],
                             'Short': [short], 
                             'Dewpoint \u00B0F': [dew]})
        df2 = pd.concat([df2, temp])

    init_url = "https://api.weather.gov/points/43.58,-116.56"
    # Request for information using Nampa ID Lat and Long
    resp = requests.get(init_url)

    resp = resp.json()
    forecast_url = resp['properties']['forecastHourly']

    forecast = requests.get(forecast_url)
    forecast = forecast.json()

    periods = forecast['properties']['periods']

    df3 = pd.DataFrame()
    for i in periods:
        dt = pd.to_datetime(i['startTime'])
        temp = i['temperature']
        short = i['shortForecast']
        dew = i['dewpoint']['value']*9/5+32
        temp = pd.DataFrame({'Date': [dt],
                             u'Temperature \u00B0F': [temp],
                             'Short': [short], 
                             'Dewpoint \u00B0F': [dew]})
        df3 = pd.concat([df3, temp])

    dflist = [df, df2, df3]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for d in dflist:
        fig.add_trace(px.line(d,x='Date',y=u'Temperature \u00B0F',hover_data=[u'Temperature \u00B0F',"Short"]).data[0],
                     secondary_y=False) 
        fig.update_yaxes(title='Temperature \u00B0F', secondary_y=False)
        fig.add_trace(px.line(d, x='Date', y='Dewpoint \u00B0F').data[0],
            secondary_y=True,)
        fig.update_yaxes(title='Dewpoint \u00B0F', secondary_y=True)

    fig.data[0]['visible'] = True
    fig.data[1]['visible'] = True
    fig.data[2]['visible'] = False
    fig.data[3]['visible'] = False
    fig.data[4]['visible'] = False
    fig.data[5]['visible'] = False

    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="Wooster, OH",
                         method="update",
                         args=[{"visible": [True, True, False, False, False, False]}
                              ]),
                    dict(label="St. Charles, MO",
                         method="update",
                         args=[{"visible": [False, False, True, True, False, False]},
                               ]),
                    dict(label="Nampa, ID",
                         method="update",
                         args=[{"visible": [False, False, False, False, True, True]},
                               ]),
                    
                ]),x=0.0,
                    xanchor="left",
                    y=1.1,
                    yanchor="top"
            )])

    fig.data[0]['line_color'] = '#ff7f0e'
    fig.data[2]['line_color'] = '#ff7f0e'
    fig.data[4]['line_color'] = '#ff7f0e'
    fig.add_hline(y=32,line_width=1)
    fig.update_layout(hovermode='x',template="plotly_dark", hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)'))

    fig.update_layout(margin=dict(l=50, r=1, b=80, t=50))
    fig.add_annotation(xref="paper", x="0", yref="paper",
                           y="-0.15",
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
        string1 = BeautifulSoup(r1['content'][0]['value'])
        string2 = BeautifulSoup(r2['content'][0]['value'])
        try:
            img1 = string1.find('img')['src']
        except TypeError:
            img1 = "https://www.nasa.gov/wp-content/uploads/2023/04/nasa-logo-web-rgb.png"
        try:
            img2 = string2.find('img')['src']
        except TypeError:
            img2 = "https://www.nasa.gov/wp-content/uploads/2023/04/nasa-logo-web-rgb.png"
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
                        <img class="img-fluid" src = "{img1}" alt="{nope}"/>
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
                        <img class="img-fluid" src = "{img2}" alt="{nope}"/>
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
    if i == 3:
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
for i in [0, 2, 4]:
    Tech_Text = Tech_Text + f"""
    <div class="row mb-3">
        <div class="col-md-6">
            <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                <div class="col-sm-7 p-3 d-flex flex-column position-static">
                    <h5 class="mb-1">
                    <a href="{tech[i]['link']}" target="_blank">{tech[i]['title']}</a>
                    </h5>
                    <p class="card-text mb-auto">{tech[i]['summary']}</p>
                </div>
                <div class="col-sm-5 rounded">
                    <a href="{tech[i]['link']}" target="_blank">
                    <img class="img-fluid" src = "{tech[i]['url']}" alt="{nope}"/>
                    </a>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                <div class="col-sm-7 p-3 d-flex flex-column position-static">
                    <h5 class="mb-1">
                    <a href="{tech[i+1]['link']}" target="_blank">{tech[i+1]['title']}</a>
                    </h5>
                    <p class="card-text mb-auto">{tech[i+1]['summary']}</p>
                </div>
                <div class="col-sm-5 rounded">
                    <a href="{tech[i+1]['link']}" target="_blank">
                    <img class="img-fluid" src = "{tech[i+1]['url']}" alt="{nope}"/>
                    </a>
                </div>
            </div>
        </div>
    </div>
    """

FT_Text = ""
for i in [0, 2, 4]:
    FT_Text = FT_Text + f"""
    <div class="row mb-3">
        <div class="col-md-6">
            <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                <div class="col-sm-7 p-3 d-flex flex-column position-static">
                    <h5 class="mb-1">
                    <a href="{f_n_t[i]['link']}" target="_blank">{f_n_t[i]['title']}</a>
                    </h5>
                    <p class="card-text mb-auto">{f_n_t[i]['summary']}</p>
                </div>
                <div class="col-sm-5 rounded">
                    <a href="{f_n_t[i]['link']}" target="_blank">
                    <img class="img-fluid" src = "{f_n_t[i]['url']}" alt="{nope}"/>
                    </a>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="row g-0 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center">
                <div class="col-sm-7 p-3 d-flex flex-column position-static">
                    <h5 class="mb-1">
                    <a href="{f_n_t[i+1]['link']}" target="_blank">{f_n_t[i+1]['title']}</a>
                    </h5>
                    <p class="card-text mb-auto">{f_n_t[i+1]['summary']}</p>
                </div>
                <div class="col-sm-5 rounded">
                    <a href="{f_n_t[i+1]['link']}" target="_blank">
                    <img class="img-fluid" src = "{f_n_t[i+1]['url']}" alt="{nope}"/>
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
      <a class="p-2 link-secondary" href="#food">Food & Travel</a>
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
<h3 class="py-2"><a id="food">Food & Travel</a></h3>
""" + FT_Text + f"""
</main>

<main class="container">
<h3 class="py-2">Daily Data Insight</h3>
<div class="row mb-3">
            <div class="col" align="center">
                <div class="row g-2 rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-300 position-relative align-items-center caption text-center">
                    <a href={dlink} target="_blank">
                    <img class="img-fluid" src = {dimg} width="60%" alt="Image not available"/>
                     </a>
                    <p>{dtext}</p>
                </div>
            </div>
        </div>
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
