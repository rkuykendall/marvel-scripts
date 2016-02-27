import os
import marvelous
from config import public_key, private_key

IGNORE = set([
    19709, 20256, 19379, 19062, 19486, 19242, 19371, 19210, 20930, 21328,
    20834, 18826, 20933, 20365, 20928, 21129, 20786, 21402, 21018
])

m = marvelous.api(public_key, private_key)

pulls = sorted(m.comics({
    'format': "comic",
    'formatType': "comic",
    'noVariants': True,
    'dateDescriptor': "thisWeek"}),
    key=lambda comic: comic.title)

directory = pulls[0].dates.on_sale.strftime('%m-%d')

if not os.path.exists(directory):
    os.makedirs(directory)

with open(directory + '/pulls.txt', 'w') as pull_checklist:
    for comic in pulls:
        if comic.series.id not in IGNORE:
            pull_checklist.write('{} (series #{})\n'.format(
                comic.title.encode('utf-8'), comic.series.id))
