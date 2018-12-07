import os
import re
import urllib.request

from bs4 import BeautifulSoup as Soup
from datetime import date
from subprocess import Popen

# Constants for fetching the page and images
CALENDAR_URL = 'https://www.theatlantic.com/photo/2018/12/2018-hubble-space-telescope-advent-calendar/577129/'
CDN_URL = 'https://cdn.theatlantic.com/assets/media/img/photo/2018/12/2018-hubble-space-telescope-advent'

# Constant for setting wallpaper by day of month
DAY_OF_MONTH = date.today().day

# Constant for creating and storing images
STORE_DIRECTORY = os.path.join(os.path.expanduser('~'), 'Pictures/Wallpapers/Hubble Space Advent Calendar 2018')

# Constant for matching filepaths/filenames on CDN
VALID_IMAGE = re.compile(r'.*/a\d{1,2}.*')

# Make the required directories
os.makedirs(STORE_DIRECTORY, exist_ok=True)

# Fetch the page for parsing
page = Soup(urllib.request.urlopen(CALENDAR_URL), 'html.parser')

# Find the containers
images = page.findAll('li', id=re.compile('img(\d{1,2})'))

# Create an empty dictionary to store the valid image URLs
valid_images = {}

# Find the valid image URLs
for image in images:
    image_url = image.find('source', attrs={'data-srcset': re.compile('main_1500')}).get('data-srcset')
    if VALID_IMAGE.match(image_url):
        valid_images[len(valid_images) + 1] = image_url

for image in valid_images:
    image_filepath = STORE_DIRECTORY + '/space' + str(image) + '.jpg'
    urllib.request.urlretrieve(valid_images[image], image_filepath)
    if image == DAY_OF_MONTH:
        call = 'tell application "Finder" to set desktop picture to POSIX file "' + image_filepath + '"'
        Popen(['osascript', '-e', call])
