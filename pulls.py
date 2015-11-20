import os
from marvel.marvel import Marvel
from config import public_key, private_key

IGNORE = set([
    19709, 20256, 19379, 19062, 19486, 19242, 19371, 19210, 20930
])

m = Marvel(public_key, private_key)

pulls = sorted(m.get_comics(
    format="comic",
    formatType="comic",
    noVariants=True,
    dateDescriptor="thisWeek").data.results,
    key=lambda comic: comic.title)

on_sale = [d for d in pulls[0].dates if d.type == 'onsaleDate'][0].date
directory = on_sale.strftime('%m-%d')

if not os.path.exists(directory):
    os.makedirs(directory)

with open(directory + '/pulls.txt', 'w') as pull_checklist:
    for comic in pulls:
        series_num = int(comic.series['resourceURI'].split('/')[-1])
        if series_num not in IGNORE:
            pull_checklist.write('{} (series #{})\n'.format(
                comic.title, series_num))
