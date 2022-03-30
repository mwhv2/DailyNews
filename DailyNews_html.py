import requests, json
from requests.exceptions import ConnectionError
import datetime
import pandas as pd
import plotly.express as px
import feedparser

# Set the current date and time
now1 = datetime.datetime.now()
update = now1.strftime("%H:%M %p")
now = now1.strftime("%A, %B %d, %Y")

# This API key is for NewsAPI. Documentation here: https://newsapi.org/docs
key = 'c185e8c5fb6144fcbf8fe7352b46bf67'

# For top headlines and science in the US
re1_url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=10&apiKey={key}"
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
fig.update_layout(hovermode='x',template="seaborn")
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
A = [0,2,4,6,8]
B = [1,3,5,7,9]
Text = ""
for i in range(int(len(response['articles'])/2)):
    r1 = response['articles'][A[i]]
    r2 = response['articles'][B[i]]
    Text = Text + f"""
    <tr>
    <td style="width:50%">
    <p><strong><a href="{r1['url']}" target="_blank">{r1['title']}</a></strong></p>
    <a href="{r1['url']}" target="_blank">
    <img src = "{r1['urlToImage']}" alt="Unable to retrieve image" style='float: left;width:30%;height:30%;padding-right:5px'/>
    </a>
    <p>{r1['description']}</p>
    <p><small>{r1['author']}</small></p>
    </td>
    <td style="width:50%">
    <p><strong><a href="{r2['url']}" target="_blank">{r2['title']}</a></strong></p>
    <a href="{r2['url']}" target="_blank">
    <img src = "{r2['urlToImage']}" alt="Unable to retrieve image" style='float: left;width:30%;height:30%;padding-right:5px'/>
    </a>
    <p>{r2['description']}</p>
    <p><small>{r2['author']}</small></p>
    </td>
    </tr>
    """

Science_Text = ""
for i in range(int(len(s_res['articles'])/2)):
    r1 = s_res['articles'][A[i]]
    r2 = s_res['articles'][B[i]]
    Science_Text = Science_Text + f"""
    <tr>
    <td style="width:50%">
    <p><strong><a href="{r1['url']}" target="_blank">{r1['title']}</a></strong></p>
    <a href="{r1['url']}" target="_blank">
    <img src = "{r1['urlToImage']}" alt="Unable to retrieve image" style='float: left;width:30%;height:30%;padding-right:5px'/>
    </a>
    <p>{r1['description']}</p>
    <p><small>{r1['author']}</small></p>
    </td>
    <td style="width:50%">
    <p><strong><a href="{r2['url']}" target="_blank">{r2['title']}</a></strong></p>
    <a href="{r2['url']}" target="_blank">
    <img src = "{r2['urlToImage']}" alt="Unable to retrieve image" style='float: left;width:30%;height:30%;padding-right:5px'/>
    </a>
    <p>{r2['description']}</p>
    <p><small>{r2['author']}</small></p>
    </td>
    </tr>
    """

Fr_Text = ""
for i in range(int(len(fr_res['articles'])/2)):
    r1 = fr_res['articles'][A[i]]
    r2 = fr_res['articles'][B[i]]
    Fr_Text = Fr_Text + f"""
    <tr>
    <td style="width:50%">
    <p><strong><a href="{r1['url']}" target="_blank">{r1['title']}</a></strong></p>
    <a href="{r1['url']}" target="_blank">
    <img src = "{r1['urlToImage']}" alt="Unable to retrieve image" style='float: left;width:30%;height:30%;padding-right:5px'/>
    </a>
    <p>{r1['description']}</p>
    <p><small>{r1['author']}</small></p>
    </td>
    <td style="width:50%">
    <p><strong><a href="{r2['url']}" target="_blank">{r2['title']}</a></strong></p>
    <a href="{r2['url']}" target="_blank">
    <img src = "{r2['urlToImage']}" alt="Unable to retrieve image" style='float: left;width:30%;height:30%;padding-right:5px'/>
    </a>
    <p>{r2['description']}</p>
    <p><small>{r2['author']}</small></p>
    </td>
    </tr>
    """

Tech_Text = ""
for i in range(int(len(t_res['articles'])/2)):
    r1 = t_res['articles'][A[i]]
    r2 = t_res['articles'][B[i]]
    Tech_Text = Tech_Text + f"""
    <tr>
    <td style="width:50%">
    <p><strong><a href="{r1['url']}" target="_blank">{r1['title']}</a></strong></p>
    <a href="{r1['url']}" target="_blank">
    <img src = "{r1['urlToImage']}" alt="Unable to retrieve image" style='float: left;width:30%;height:30%;padding-right:5px'/>
    </a>
    <p>{r1['description']}</p>
    <p><small>{r1['author']}</small></p>
    </td>
    <td style="width:50%">
    <p><strong><a href="{r2['url']}" target="_blank">{r2['title']}</a></strong></p>
    <a href="{r2['url']}" target="_blank">
    <img src = "{r2['urlToImage']}" alt="Unable to retrieve image" style='float: left;width:30%;height:30%;padding-right:5px'/>
    </a>
    <p>{r2['description']}</p>
    <p><small>{r2['author']}</small></p>
    </td>
    </tr>
    """


f_html = open('DailyNews.html','w',encoding="utf-8")

html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>The Daily News</title>
    <link rel="stylesheet" href="dnews_styles.css">
</head>
<body>
<header>
    <div class="head1">The Daily News</div>
    <div class="head2">{now}</div>
</header>
<div class="sidenav">
  <a href="#top">Top US Headlines</a>
  <a href="#science">Science</a>
  <a href="#france">French News</a>
  <a href="#tech">Technology</a>
  <a href="#forecast">Weather</a>
  <p>Produced using NewsAPI</p>
</div>
<video controls poster={npr_image} style="width:12%;float:right">
        <source src={npr_url} type="audio/mpeg">
</video>
<div class="body_sec">
<h2><a id="top">Top US Headlines</a></h2>
<table>
""" + Text + f"""
</table>
<hr>
</div>
<video controls poster={sciam_img} style="width:12%;float:right">
        <source src={sci_url} type="audio/mpeg">
</video>
<div class="body_sec">
<h2><a id="science">Science</a></h2>
<table>
""" + Science_Text + f"""
</table>
<hr>
</div>
<video controls poster={rfi_img} style="width:12%;float:right">
        <source src={rfi} type="audio/mpeg">
</video>
<div class="body_sec">
<h2><a id="france">French News</a></h2>
<table>
""" + Fr_Text + f"""
</table>
<hr>
<h2><a id="tech">Technology</a></h2>
<table>
""" + Tech_Text + f"""
</table>
<hr>
<h2><a id="forecast">Seven Day Forecast and Current SDO View at 171&#8491</a></h2>
<table>
<tr>
<td style="width:70%">
<iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless"
src="NWSforecast.html" height="525" width="100%"></iframe>
</td>
<td><a href="https://helioviewer.org/" target="_blank">
<img src={Sun_im} alt="Latest SDO image not available" style="width:97%"></a>
</td>
</tr>
</table>
</div>
<footer>Last updated at {update}. Created by Matt Wentzel-Long</footer>
</body>
</html>
"""

f_html.write(html_template)
f_html.close()
