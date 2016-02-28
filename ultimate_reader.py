import os
from collections import defaultdict

import marvelous

from config import public_key, private_key

m = marvelous.api(public_key, private_key, cache=True)

SERIES = set([
    466, # Ultimate Spider-Man
    474, # Ultimate X-Men
    13831, # Ultimate Comics Spider-man
    8509, # Ultimate Comics Spider-Man
    664, # Ultimates v1 <-- TODO: None date causing problems, fix in lib.
    709, # Ultimates v2
    702, # Ultimate Fantastic Four
    18508, # Miles Morales: Ultimate Spider-MAN
    5744, # ULTIMATE X-MEN/ULTIMATE FANTASTIC FOUR ANNUAL (2008)
    11272, # ULTIMATE COMICS THOR
    19658, # Ultimate End
    1054, # ULTIMATE SPIDER-MAN ANNUAL
    760, # ULTIMATE NIGHTMARE
    838, # ULTIMATE SECRET
    759, # ULTIMATE EXTINCTION
])

def ordinal(n):
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
       return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, "th")

def all_comics_for_series(id):
    series = m.series(id)

    LIMIT = 100
    offset = 0
    total = None
    comics = []
    while total is None or len(comics) < total:
        response = series.comics({
            'format': 'comic',
            'formatType': 'comic',
            'noVariants': True,
            'limit': LIMIT,
            'offset': offset,
            'orderBy': 'issueNumber'
        })
        comics += response.comics
        total = response.response['data']['total']
        offset += LIMIT
    
    return comics
    
comics_ordered = defaultdict(list)
    
for series_id in SERIES:
    for comic in all_comics_for_series(series_id):
        if comic.dates.on_sale is not None:
            comics_ordered[comic.dates.on_sale].append(comic.title)
        
for date in sorted(comics_ordered):
    for comic in comics_ordered[date]:
        print '{} ({})'.format(
            comic, 
            date.strftime('%B ') + ordinal(date.day) + date.strftime(', %Y'))
