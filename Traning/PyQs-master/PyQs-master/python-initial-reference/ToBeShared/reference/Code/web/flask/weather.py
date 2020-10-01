from flask import Flask, make_response, request


app = Flask(__name__)

xml_o = """<?xml version="1.0" encoding="UTF-8"?>
<query xmlns:yahoo="http://www.yahooapis.com/v1/base.rng"
    yahoo:count="1" yahoo:created="2018-04-21T15:18:32Z" yahoo:lang="en-IN">
    <results>
        <channel>
            <yweather:units
                xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                distance="mi" pressure="in" speed="mph" temperature="F"/>
            <title>Yahoo! Weather - Nome, AK, US</title>
            <link>http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2460286/</link>
            <description>Yahoo! Weather for Nome, AK, US</description>
            <language>en-us</language>
            <lastBuildDate>Sat, 21 Apr 2018 07:18 AM AKDT</lastBuildDate>
            <ttl>60</ttl>
            <yweather:location
                xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                city="Nome" country="United States" region=" AK"/>
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
                <title>Conditions for Nome, AK, US at 06:00 AM AKDT</title>
                <geo:lat xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">64.499474</geo:lat>
                <geo:long xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">-165.405792</geo:long>
                <link>http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2460286/</link>
                <pubDate>Sat, 21 Apr 2018 06:00 AM AKDT</pubDate>
                <yweather:condition
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="31" date="Sat, 21 Apr 2018 06:00 AM AKDT"
                    temp="17" text="Clear"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="23" date="21 Apr 2018" day="Sat" high="27"
                    low="17" text="Breezy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="34" date="22 Apr 2018" day="Sun" high="38"
                    low="22" text="Mostly Sunny"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="28" date="23 Apr 2018" day="Mon" high="33"
                    low="28" text="Mostly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="28" date="24 Apr 2018" day="Tue" high="36"
                    low="29" text="Mostly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="28" date="25 Apr 2018" day="Wed" high="35"
                    low="26" text="Mostly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="28" date="26 Apr 2018" day="Thu" high="34"
                    low="31" text="Mostly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="30" date="27 Apr 2018" day="Fri" high="34"
                    low="29" text="Partly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="28" date="28 Apr 2018" day="Sat" high="33"
                    low="30" text="Mostly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="28" date="29 Apr 2018" day="Sun" high="34"
                    low="31" text="Mostly Cloudy"/>
                <yweather:forecast
                    xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    code="26" date="30 Apr 2018" day="Mon" high="37"
                    low="29" text="Cloudy"/>
                <description>&lt;![CDATA[&lt;img src="http://l.yimg.com/a/i/us/we/52/31.gif"/&gt;
&lt;BR /&gt;
&lt;b&gt;Current Conditions:&lt;/b&gt;
&lt;BR /&gt;Clear
&lt;BR /&gt;
&lt;BR /&gt;
&lt;b&gt;Forecast:&lt;/b&gt;
&lt;BR /&gt; Sat - Breezy. High: 27Low: 17
&lt;BR /&gt; Sun - Mostly Sunny. High: 38Low: 22
&lt;BR /&gt; Mon - Mostly Cloudy. High: 33Low: 28
&lt;BR /&gt; Tue - Mostly Cloudy. High: 36Low: 29
&lt;BR /&gt; Wed - Mostly Cloudy. High: 35Low: 26
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

json_o = """{
 "query": {
  "count": 1,
  "created": "2018-04-21T15:21:01Z",
  "lang": "en-IN",
  "results": {
   "channel": {
    "units": {
     "distance": "mi",
     "pressure": "in",
     "speed": "mph",
     "temperature": "F"
    },
    "title": "Yahoo! Weather - Nome, AK, US",
    "link": "http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2460286/",
    "description": "Yahoo! Weather for Nome, AK, US",
    "language": "en-us",
    "lastBuildDate": "Sat, 21 Apr 2018 07:21 AM AKDT",
    "ttl": "60",
    "location": {
     "city": "Nome",
     "country": "United States",
     "region": " AK"
    },
    "wind": {
     "chill": "3",
     "direction": "23",
     "speed": "22"
    },
    "atmosphere": {
     "humidity": "71",
     "pressure": "1007.0",
     "rising": "0",
     "visibility": "16.1"
    },
    "astronomy": {
     "sunrise": "7:6 am",
     "sunset": "10:56 pm"
    },
    "image": {
     "title": "Yahoo! Weather",
     "width": "142",
     "height": "18",
     "link": "http://weather.yahoo.com",
     "url": "http://l.yimg.com/a/i/brand/purplelogo//uh/us/news-wea.gif"
    },
    "item": {
     "title": "Conditions for Nome, AK, US at 06:00 AM AKDT",
     "lat": "64.499474",
     "long": "-165.405792",
     "link": "http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2460286/",
     "pubDate": "Sat, 21 Apr 2018 06:00 AM AKDT",
     "condition": {
      "code": "31",
      "date": "Sat, 21 Apr 2018 06:00 AM AKDT",
      "temp": "17",
      "text": "Clear"
     },
     "forecast": [
      {
       "code": "23",
       "date": "21 Apr 2018",
       "day": "Sat",
       "high": "27",
       "low": "17",
       "text": "Breezy"
      },
      {
       "code": "34",
       "date": "22 Apr 2018",
       "day": "Sun",
       "high": "38",
       "low": "22",
       "text": "Mostly Sunny"
      },
      {
       "code": "28",
       "date": "23 Apr 2018",
       "day": "Mon",
       "high": "33",
       "low": "28",
       "text": "Mostly Cloudy"
      },
      {
       "code": "28",
       "date": "24 Apr 2018",
       "day": "Tue",
       "high": "36",
       "low": "29",
       "text": "Mostly Cloudy"
      },
      {
       "code": "28",
       "date": "25 Apr 2018",
       "day": "Wed",
       "high": "35",
       "low": "26",
       "text": "Mostly Cloudy"
      },
      {
       "code": "28",
       "date": "26 Apr 2018",
       "day": "Thu",
       "high": "34",
       "low": "31",
       "text": "Mostly Cloudy"
      },
      {
       "code": "30",
       "date": "27 Apr 2018",
       "day": "Fri",
       "high": "34",
       "low": "29",
       "text": "Partly Cloudy"
      },
      {
       "code": "28",
       "date": "28 Apr 2018",
       "day": "Sat",
       "high": "33",
       "low": "30",
       "text": "Mostly Cloudy"
      },
      {
       "code": "28",
       "date": "29 Apr 2018",
       "day": "Sun",
       "high": "34",
       "low": "31",
       "text": "Mostly Cloudy"
      },
      {
       "code": "26",
       "date": "30 Apr 2018",
       "day": "Mon",
       "high": "37",
       "low": "29",
       "text": "Cloudy"
      }
     ],
     "description": "<![CDATA[<img src=\\"http://l.yimg.com/a/i/us/we/52/31.gif\\"/>\\n<BR />\\n<b>Current Conditions:</b>\\n<BR />Clear\\n<BR />\\n<BR />\\n<b>Forecast:</b>\\n<BR /> Sat - Breezy. High: 27Low: 17\\n<BR /> Sun - Mostly Sunny. High: 38Low: 22\\n<BR /> Mon - Mostly Cloudy. High: 33Low: 28\\n<BR /> Tue - Mostly Cloudy. High: 36Low: 29\\n<BR /> Wed - Mostly Cloudy. High: 35Low: 26\\n<BR />\\n<BR />\\n<a href=\\"http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-2460286/\\">Full Forecast at Yahoo! Weather</a>\\n<BR />\\n<BR />\\n<BR />\\n]]>",
     "guid": {
      "isPermaLink": "false"
     }
    }
   }
  }
 }
}"""



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    headers_json = {'Content-Type':'application/json'}
    headers_xml = {'Content-Type':'application/xml'}
    #print(path, request.args)
    if "format" in request.args and request.args["format"] == "xml":
        return xml_o, 200 ,headers_xml
    else:        
        return json_o, 200 ,headers_json

  


if __name__ == '__main__':
    app.run()
    
'''
http://localhost:5000/query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22nome%2C%20ak%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys
http://localhost:5000/query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22nome%2C%20ak%22)&format=xml&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys



'''