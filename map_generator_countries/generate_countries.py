import os, urllib, json

# Specify the filename to used as input.
FILENAME = "COUNTRIES.txt"

# Specify the map parameters to be used.
ZOOM_LEVEL_MIN = 3
ZOOM_LEVEL_MAX = 8
IMAGE_WIDTH = "600"
IMAGE_HEIGHT = "600"

# Check if the target storage folder exists, create if not yet existing.
if not os.path.isdir("generated_maps"):
  os.mkdir("generated_maps")

# Open the list of Countries to be parsed.
# The 'with' keyword has auto-close mechanism when
#  it has finisihed reading the input file.
# Hence, we do not need to add exception handler.
# Note that it will overwrite the previously fetched map images.
with open(FILENAME) as countries:
  for country in countries:
    # Remove all leading and trailing spaces per line.
    country = country.strip()

    # Some countries could not be geocoded properly.
    # They need some equivalent names.
    if country == "Congo, the Democratic Republic of the":
      country = "DR Congo"

    elif country == "Palestinian":
      country = "Palestine"

    elif country == "Virgin Islands, British":
      country = "British Virgin Islands"

    # Since I/O operations are major bottlenecks, comment this line
    # if you need to accelerate the map fetching.
    print "Processing: " + country + " Country"

    # This will be used in the filenames of the generated images.
    country_raw = country

    # URL Encode special charcters before we pass it to the Geocoder.
    # This is necessary especially for Macintosh systems.
    country_encoded = urllib.quote_plus(country)

    # Utilize the Google's Geocoding API.
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + country_encoded + "&sensor=false"

    # Send a request for the Geocoded object.
    response = urllib.urlopen(url);

    # Read the response and pipe it to the JSON loader.
    data = json.loads(response.read())

    # Retrieve the Latitude and Longitude values from the Geocoded JSON object.
    LATITUDE = data["results"][0]["geometry"]["location"]["lat"]
    LONGITUDE = data["results"][0]["geometry"]["location"]["lng"]

    # Fetch all zoom levels for the current country.
    for zoom in range(ZOOM_LEVEL_MIN, ZOOM_LEVEL_MAX + 1):
      # Since I/O operations are major bottlenecks, comment this line
      # if you need to accelerate the map fetching.
      print "\tGenerating Zoom Level: " + str(zoom)

      # Specify the filenmae structure/format.
      filename = "generated_maps/" + country_raw + " - " + str(zoom) + ".png"

      # Utilize the static images of Nokia Maps.
      urllib.urlretrieve("http://image.maps.cit.api.here.com/mia/1.6/?app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg&w=" + IMAGE_WIDTH + "&h="+ IMAGE_HEIGHT + "&t=8&z=" + str(zoom) + "&lat=" + str(LATITUDE) + "&lon=" + str(LONGITUDE), filename)

    print
