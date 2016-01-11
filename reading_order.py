import sys
import os
from collections import defaultdict
from marvel.marvel import Marvel
from config import public_key, private_key

m = Marvel(public_key, private_key)

series = sys.argv[1:]

def ordinal(n):
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
       return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, "th")

def all_comics_for_series(id):
    series = m.get_single_series(id).data.results[0]

    LIMIT = 100
    offset = 0
    total = None
    comics = []
    while total is None or len(comics) < total:
        response = series.get_comics(
            format='comic',
            formatType='comic',
            noVariants=True,
            limit=LIMIT,
            offset=offset,
            orderBy='issueNumber'
        ).data
        comics += response.results
        total = response.total
        offset += LIMIT

    return comics

comics_ordered = defaultdict(list)

for series_id in series:
    for comic in all_comics_for_series(series_id):
        comic_date = [d for d in comic.dates if d.type == 'onsaleDate'][0].date
        comic_title = comic.title
        comics_ordered[comic_date].append(comic_title)
        
for date in sorted(comics_ordered):
    for comic in comics_ordered[date]:
        print '{} ({})'.format(
            comic, 
            date.strftime('%B ') + ordinal(date.day) + date.strftime(', %Y'))

