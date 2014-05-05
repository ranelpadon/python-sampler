import urllib, json

ZOOM_LEVEL_MIN = 3
ZOOM_LEVEL_MAX = 8
IMAGE_WIDTH = "600"
IMAGE_HEIGHT = "600"
count = 0

with open('COUNTRIES.txt') as countries:
  for country in countries:
    country = country.strip()

    # Other countries could not be geocoded properly.
    if country == "Congo, the Democratic Republic of the":
      country = "DR Congo"

    elif country == "Palestinian":
      country = "Palestine"

    elif country == "Virgin Islands, British":
      country = "British Virgin Islands"

    print "Processing: " + country + " Country"

    country = urllib.quote_plus(country)

    url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + country + "&sensor=false"

    response = urllib.urlopen(url);
    data = json.loads(response.read())

    LATITUDE = data["results"][0]["geometry"]["location"]["lat"]
    LONGITUDE = data["results"][0]["geometry"]["location"]["lng"]

    for zoom in range(ZOOM_LEVEL_MIN, ZOOM_LEVEL_MAX+1):
      print "\tGenerating Zoom Level: " + str(zoom)

      filename = country + " - " + str(zoom) + ".png"

      urllib.urlretrieve("http://image.maps.cit.api.here.com/mia/1.6/?app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg&w=" + IMAGE_WIDTH + "&h="+ IMAGE_HEIGHT + "&t=8&z=" + str(zoom) + "&lat=" + str(LATITUDE) + "&lon=" + str(LONGITUDE), filename)

    print














