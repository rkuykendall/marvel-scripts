import os
import marvelous

# Your own config file to keep your private key local and secret
from config import public_key, private_key

# All the series IDs of comics I'm not interested in reading
# I pull these out of the resulting pulls.txt file, then rerun this script
IGNORE = set([
    19709, 20256, 19379, 19062, 19486, 19242, 19371, 19210, 20930, 21328,
    20834, 18826, 20933, 20365, 20928, 21129, 20786, 21402, 21018, 14803,
    21285, 12212, 21434, 21020, 19512, 19367, 21607, 21131
])

# Authenticate with Marvel, with keys I got from http://developer.marvel.com/
m = marvelous.api(public_key, private_key)

# Get all comics from this week, sorted alphabetically by title
pulls = sorted(m.comics({
    'format': "comic",
    'formatType': "comic",
    'noVariants': True,
    'dateDescriptor': "thisWeek",
    'limit': 100}),
    key=lambda comic: comic.title)

# Grab the sale date of any of the comics for the current week
week = pulls[0].dates.on_sale.strftime('%m/%d')

print("New comics for the week of {}:".format(week))
# Check each comic that came out this week
for comic in pulls:
    # If this series isn't in my ignore list
    if comic.series.id not in IGNORE:
        # Write a line to the file with the name of the issue, and the
        # id of the series incase I want to add it to my ignore list
        print('- {} (series #{})'.format(comic.title, comic.series.id))
