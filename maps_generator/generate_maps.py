#!/usr/bin/python

# Import the native utilities.
import json
import os
import urllib

# Specify the filenames to be used as input.
# Store it in a list data structure.
files = []

# Comment out this line if you do not want to include the maps of Countries.
files += ["COUNTRIES.txt"]

# Comment out this line if you do not want to include the maps of Cities.
files += ["CITIES.txt"]

# Specify the map parameters to be used.
ZOOM_LEVEL_MIN = 4
ZOOM_LEVEL_MAX = 6
IMAGE_WIDTH = "400"
IMAGE_HEIGHT = "400"

def create_folder(path):
    """Function to create a folder given the path or folder name.

    Arg:
        path: The path that will be processed in string format.
    """

    # Check if the target storage folder exists, create if not yet existing.
    if not os.path.isdir(path):
      # os.mkdir() could not create nested directories on-the-fly.
      # Try os.mkdirs for that.
      os.mkdir(path)

# Create the root directory of the map folder and its subfolders.
create_folder("generated_maps")
create_folder("generated_maps/countries")
create_folder("generated_maps/cities")

# Process each file.
for file in files:
    # Vary the folder prefix depending on the context.
    # It is used in the image filenames of the fetched maps.
    if file == "COUNTRIES.txt":
        folder_prefix = "generated_maps/countries/"

    else:
        folder_prefix = "generated_maps/cities/"

    # Open the list of Places to be parsed.
    # The 'with' Python keyword has auto-close mechanism when
    #  it has finished reading the input file.
    # Hence, we do not need to add exception handler.
    # Note that it will overwrite the previously fetched map images.
    with open(file) as places:
        # Traverse the current file line by line, that is, per row.
        for place in places:
            # Remove all leading and trailing spaces per line/row.
            place = place.strip()

            # Some countries could not be geocoded properly.
            # Hence, they need some equivalent names.
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

            # Set the Google's Geocoding API's base URL.
            base_url_google = "http://maps.googleapis.com/maps/api/geocode/json"

            # Utilize the Google's Geocoding API.
            url = base_url_google + "?address=" + place_encoded + "&sensor=false"

            # Send a request for the Geocoded object.
            response = urllib.urlopen(url);

            # Read the response and pipe it to the JSON loader.
            # data is a dictionary object.
            data = json.loads(response.read())

            # Retrieve the Latitude and Longitude values from the Geocoded JSON object.
            LATITUDE = data["results"][0]["geometry"]["location"]["lat"]
            LONGITUDE = data["results"][0]["geometry"]["location"]["lng"]

            # Fetch all zoom levels for the current place.
            for zoom in range(ZOOM_LEVEL_MIN, ZOOM_LEVEL_MAX + 1):
                # Since I/O operations are major bottlenecks, comment this line
                # if you need to accelerate the map fetching.
                print "\tGenerating Zoom Level: " + str(zoom)

                # Set the Nokia Maps base URL.
                base_url_nokia = "http://image.maps.cit.api.here.com/mia/1.6/"

                # Specify the filename format of the image.
                filename = folder_prefix + place_raw + " - " + str(zoom) + ".png"

                # Utilize the static image of Nokia Maps.
                # Retrieve and save the fetched image using the specified filename.
                urllib.urlretrieve(base_url_nokia + "?app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg" +
                                      "&w=" + IMAGE_WIDTH + "&h=" + IMAGE_HEIGHT + "&t=8&z=" + str(zoom) +
                                      "&lat=" + str(LATITUDE) + "&lon=" + str(LONGITUDE), filename)

            print
