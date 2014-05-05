# Import the file and http utilities.
import os, urllib, json

# Specify the filenames to be used as input.
# Store it in a list structure.
FILES = []
FILES += ["COUNTRIES.txt"]
FILES += ["CITIES.txt"]

# Specify the map parameters to be used.
ZOOM_LEVEL_MIN = 4
ZOOM_LEVEL_MAX = 6
IMAGE_WIDTH = "400"
IMAGE_HEIGHT = "400"

# Function to create folder given a path or folder name.
def create_folder(path):
  # Check if the target storage folder exists, create if not yet existing.
  if not os.path.isdir(path):
    os.mkdir(path)

# Create the root directory of the map folder and its subfolders.
create_folder("generated_maps")
create_folder("generated_maps/countries")
create_folder("generated_maps/cities")

for FILE in FILES:
  if FILE == "COUNTRIES.txt":
    folder_prefix = "generated_maps/countries/"

  else:
    folder_prefix = "generated_maps/cities/"

  # Open the list of Places to be parsed.
  # The 'with' keyword has auto-close mechanism when
  #  it has finished reading the input file.
  # Hence, we do not need to add exception handler.
  # Note that it will overwrite the previously fetched map images.
  with open(FILE) as places:
    for place in places:
      # Remove all leading and trailing spaces per line.
      place = place.strip()

      # Some countries could not be geocoded properly.
      # They need some equivalent names.
      if place == "Congo, the Democratic Republic of the":
        place = "DR Congo"

      elif place == "Palestinian":
        place = "Palestine"

      elif place == "Virgin Islands, British":
        place = "British Virgin Islands"

      # Since I/O operations are major bottlenecks, comment this line
      # if you need to accelerate the map fetching.
      print "Processing: " + place

      # This will be used in the filenames of the generated images.
      place_raw = place

      # URL Encode the special characters before we pass it to the Geocoder.
      # This is necessary especially for Macintosh systems.
      place_encoded = urllib.quote_plus(place)

      # Utilize the Google's Geocoding API.
      url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + place_encoded + "&sensor=false"

      # Send a request for the Geocoded object.
      response = urllib.urlopen(url);

      # Read the response and pipe it to the JSON loader.
      data = json.loads(response.read())

      # Retrieve the Latitude and Longitude values from the Geocoded JSON object.
      LATITUDE = data["results"][0]["geometry"]["location"]["lat"]
      LONGITUDE = data["results"][0]["geometry"]["location"]["lng"]

      # Fetch all zoom levels for the current place.
      for zoom in range(ZOOM_LEVEL_MIN, ZOOM_LEVEL_MAX + 1):
        # Since I/O operations are major bottlenecks, comment this line
        # if you need to accelerate the map fetching.
        print "\tGenerating Zoom Level: " + str(zoom)

        # Specify the filenmae structure/format.
        filename = folder_prefix + place_raw + " - " + str(zoom) + ".png"

        # Utilize the static images of Nokia Maps.
        urllib.urlretrieve("http://image.maps.cit.api.here.com/mia/1.6/?app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg&w=" + IMAGE_WIDTH + "&h="+ IMAGE_HEIGHT + "&t=8&z=" + str(zoom) + "&lat=" + str(LATITUDE) + "&lon=" + str(LONGITUDE), filename)

      print
