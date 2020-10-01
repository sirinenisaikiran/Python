from flask import Flask, make_response, request


app = Flask(__name__)

xml_o = """<?xml version="1.0" encoding="UTF-8"?>
<query xmlns:yahoo="http://www.yahooapis.com/v1/base.rng"
    yahoo:count="1" yahoo:created="{fulldatetime}" yahoo:lang="en-IN">
    <results>
        <channel>
            <yweather:units
                xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                distance="mi" pressure="in" speed="mph" temperature="F"/>
            <title>Yahoo! Weather - {location}, {country}</title>
            <link>http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2460286/</link>
            <description>Yahoo! Weather for {location}, {country}</description>
            <language>en-us</language>
            <lastBuildDate>{fulldatetimewithday}</lastBuildDate>
            <ttl>60</ttl>
            <yweather:location
                xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                city="{location}" country="{country}" region=" {country}"/>
            <yweather:wind
                xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                chill="3" direction="23" speed="22"/>
            <yweather:atmosphere
                xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                humidity="71" pressure="1007.0" rising="0" visibility="16.1"/>
            <yweather:astronomy
                xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                sunrise="7:6 am" sunset="10:56 pm"/>
            <image>
                <title>Yahoo! Weather</title>
                <width>142</width>
                <height>18</height>
                <link>http://weather.yahoo.com</link>
                <url>http://l.yimg.com/a/i/brand/purplelogo//uh/us/news-wea.gif</url>
            </image>
            <item>
                <title>Conditions for {location}, {country} at 06:00 AM AKDT</title>
                <geo:lat xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">64.499474</geo:lat>
                <geo:long xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">-165.405792</geo:long>
                <link>http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2460286/</link>
                <pubDate>{fulldatetimewithday}</pubDate>
                <yweather:condition
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="31" date="{fulldatetimewithday}"
                    temp="17" text="Clear"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="23" date="{todaysDateInText}" day="{day}" high="27"
                    low="17" text="Breezy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="34" date="{plus1DateInText}" day="{plus1day}" high="38"
                    low="22" text="Mostly Sunny"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="28" date="{plus2DateInText}" day="{plus2day}" high="33"
                    low="28" text="Mostly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="28" date="{plus3DateInText}" day="{plus3day}" high="36"
                    low="29" text="Mostly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="28" date="{plus4DateInText}" day="{plus4day}" high="35"
                    low="26" text="Mostly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="28" date="{plus5DateInText}" day="{plus5day}" high="34"
                    low="31" text="Mostly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="30" date="{plus6DateInText}" day="{plus6day}" high="34"
                    low="29" text="Partly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="28" date="{plus7DateInText}" day="{plus7day}" high="33"
                    low="30" text="Mostly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="28" date="{plus8DateInText}" day="{plus8day}" high="34"
                    low="31" text="Mostly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="26" date="{plus9DateInText}" day="{plus9day}" high="37"
                    low="29" text="Cloudy"/>
                <description>&lt;![CDATA[&lt;img src="http://l.yimg.com/a/i/us/we/52/31.gif"/&gt;
&lt;BR /&gt;
&lt;b&gt;Current Conditions:&lt;/b&gt;
&lt;BR /&gt;Clear
&lt;BR /&gt;
&lt;BR /&gt;
&lt;b&gt;Forecast:&lt;/b&gt;
&lt;BR /&gt; {day} - Breezy. High: 27Low: 17
&lt;BR /&gt; {plus1day} - Mostly Sunny. High: 38Low: 22
&lt;BR /&gt; {plus2day} - Mostly Cloudy. High: 33Low: 28
&lt;BR /&gt; {plus3day} - Mostly Cloudy. High: 36Low: 29
&lt;BR /&gt; {plus4day} - Mostly Cloudy. High: 35Low: 26
&lt;BR /&gt;
&lt;BR /&gt;
&lt;a href="http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2460286/"&gt;Full Forecast at Yahoo! Weather&lt;/a&gt;
&lt;BR /&gt;
&lt;BR /&gt;
&lt;BR /&gt;
]]&gt;</description>
                <guid isPermaLink="false"/>
            </item>
        </channel>
    </results>
</query>
"""

json_o = """{{
 "query": {{
  "count": 1,
  "created": "{fulldatetime}",
  "lang": "en-IN",
  "results": {{
   "channel": {{
    "units": {{
     "distance": "mi",
     "pressure": "in",
     "speed": "mph",
     "temperature": "F"
    }},
    "title": "Yahoo! Weather - {location}, {country}",
    "link": "http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2460286/",
    "description": "Yahoo! Weather for {location}, {country}",
    "language": "en-us",
    "lastBuildDate": "{fulldatetimewithday}",
    "ttl": "60",
    "location": {{
     "city": "{location}",
     "country": "{country}",
     "region": " {country}"
    }},
    "wind": {{
     "chill": "3",
     "direction": "23",
     "speed": "22"
    }},
    "atmosphere": {{
     "humidity": "71",
     "pressure": "1007.0",
     "rising": "0",
     "visibility": "16.1"
    }},
    "astronomy": {{
     "sunrise": "7:6 am",
     "sunset": "10:56 pm"
    }},
    "image": {{
     "title": "Yahoo! Weather",
     "width": "142",
     "height": "18",
     "link": "http://weather.yahoo.com",
     "url": "http://l.yimg.com/a/i/brand/purplelogo//uh/us/news-wea.gif"
    }},
    "item": {{
     "title": "Conditions for {location}, {country} at 06:00 AM",
     "lat": "64.499474",
     "long": "-165.405792",
     "link": "http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2460286/",
     "pubDate": "{fulldatetimewithday}",
     "condition": {{
      "code": "31",
      "date": "{fulldatetimewithday}",
      "temp": "17",
      "text": "Clear"
     }},
     "forecast": [
      {{
       "code": "23",
       "date": "{todaysDateInText}",
       "day": "{day}",
       "high": "27",
       "low": "17",
       "text": "Breezy"
      }},
      {{
       "code": "34",
       "date": "{plus1DateInText}",
       "day": "{plus1day}",
       "high": "38",
       "low": "22",
       "text": "Mostly Sunny"
      }},
      {{
       "code": "28",
       "date": "{plus2DateInText}",
       "day": "{plus2day}",
       "high": "36",
       "low": "29",
       "text": "Mostly Cloudy"
      }},
      {{
       "code": "28",
       "date": "{plus3DateInText}",
       "day": "{plus3day}",
       "high": "35",
       "low": "26",
       "text": "Mostly Cloudy"
      }},
      {{
       "code": "28",
       "date": "{plus4DateInText}",
       "day": "{plus4day}",
       "high": "34",
       "low": "31",
       "text": "Mostly Cloudy"
      }},
      {{
       "code": "30",
       "date": "{plus5DateInText}",
       "day": "{plus5day}",
       "high": "34",
       "low": "29",
       "text": "Partly Cloudy"
      }},
      {{
       "code": "28",
       "date": "{plus6DateInText}",
       "day": "{plus6day}",
       "high": "33",
       "low": "30",
       "text": "Mostly Cloudy"
      }},
      {{
       "code": "28",
       "date": "{plus7DateInText}",
       "day": "{plus7day}",
       "high": "34",
       "low": "31",
       "text": "Mostly Cloudy"
      }},
      {{
       "code": "26",
       "date": "{plus8DateInText}",
       "day": "{plus8day}",
       "high": "37",
       "low": "29",
       "text": "Cloudy"
      }},
      {{
       "code": "28",
       "date": "{plus9DateInText}",
       "day": "{plus9day}",
       "high": "33",
       "low": "28",
       "text": "Mostly Cloudy"
      }}
     ],
     "description": "<![CDATA[<img src=\\"http://l.yimg.com/a/i/us/we/52/31.gif\\"/>\\n<BR />\\n<b>Current Conditions:</b>\\n<BR />Clear\\n<BR />\\n<BR />\\n<b>Forecast:</b>\\n<BR /> {day} - Breezy. High: 27Low: 17\\n<BR /> {plus1day} - Mostly Sunny. High: 38Low: 22\\n<BR /> {plus2day} - Mostly Cloudy. High: 33Low: 28\\n<BR /> {plus3day} - Mostly Cloudy. High: 36Low: 29\\n<BR /> {plus4day} - Mostly Cloudy. High: 35Low: 26\\n<BR />\\n<BR />\\n<a href=\\"http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2460286/\\">Full Forecast at Yahoo! Weather</a>\\n<BR />\\n<BR />\\n<BR />\\n]]>",
     "guid": {{
      "isPermaLink": "false"
     }}
    }}
   }}
  }}
 }}
}}"""

def getSubs(location):
    from datetime import datetime, date,timezone, timedelta
    b = datetime.now()
    a = date.today()
    subs = dict(
        #2018-04-21T15:18:32Z
        fulldatetime=datetime.utcnow().replace(tzinfo=timezone.utc, microsecond=0).isoformat().replace('+00:00', 'Z'),
        fulldatetimewithday= b.strftime("%a, %d %b %Y %I:%M %p"), #Sat, 21 Apr 2018 07:18 AM
        location=location,
        country="Unknown",
        todaysDateInText=(a + timedelta(days=0)).strftime("%d %b %Y"),
        day=(a + timedelta(days=0)).strftime("%a"),
        plus1DateInText=(a + timedelta(days=1)).strftime("%d %b %Y"),
        plus1day=(a + timedelta(days=1)).strftime("%a"),
        plus2DateInText=(a + timedelta(days=2)).strftime("%d %b %Y"),
        plus2day=(a + timedelta(days=2)).strftime("%a"),
        plus3DateInText=(a + timedelta(days=3)).strftime("%d %b %Y"),
        plus3day=(a + timedelta(days=3)).strftime("%a"),
        plus4DateInText=(a + timedelta(days=4)).strftime("%d %b %Y"),
        plus4day=(a + timedelta(days=4)).strftime("%a"),
        plus5DateInText=(a + timedelta(days=5)).strftime("%d %b %Y"),
        plus5day=(a + timedelta(days=5)).strftime("%a"),
        plus6DateInText=(a + timedelta(days=6)).strftime("%d %b %Y"),
        plus6day=(a + timedelta(days=6)).strftime("%a"),
        plus7DateInText=(a + timedelta(days=7)).strftime("%d %b %Y"),
        plus7day=(a + timedelta(days=7)).strftime("%a"),
        plus8DateInText=(a + timedelta(days=8)).strftime("%d %b %Y"),
        plus8day=(a + timedelta(days=8)).strftime("%a"),
        plus9DateInText=(a + timedelta(days=9)).strftime("%d %b %Y"),
        plus9day=(a + timedelta(days=9)).strftime("%a")
    )
    return subs     
    
def findLocation(text):
    import re 
    loc = re.findall(r"where text='(\w+)'", text)
    return loc[0] if len(loc)>=1 else "mumbai"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    headers_json = {'Content-Type':'application/json'}
    headers_xml = {'Content-Type':'application/xml'}
    subs = getSubs(findLocation(request.args.get("q","Notfound")))
    #print(path, request.args)
    if "format" in request.args and request.args["format"] == "xml":
        return xml_o.format(**subs), 200 ,headers_xml
    else:        
        return json_o.format(**subs), 200 ,headers_json

  


if __name__ == '__main__':
    app.run()
    
'''
http://localhost:5000/query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22nome%2C%20ak%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys
http://localhost:5000/query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22nome%2C%20ak%22)&format=xml&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys



'''