import sys
from calibre.library import db

oneAtATime = False

api = None
try:
    api = db(sys.argv[1]).new_api
except:
    print('no library path supplied or failed to find library')
    
volOnes = api.search('identifiers:=cmoa: series_index:=1')
# print(volOnes)

for v1 in volOnes:
    v1m = api.get_proxy_metadata(v1)
    if (v1m.series == None): continue
    
    print(f'book: {v1} - {v1m.series} [{v1m.series_index}]')
    series = v1m.identifiers['cmoa'].split('-')[0]
    anyChanged = False
    
    seriesId, = api.field_ids_for('series', v1)
    for book in api.books_for_field('series', seriesId):
        bookM = api.get_metadata(book)
        print (bookM.title)
        
        if (bookM.series_index == 1):
            print(f'skipping master volume {bookM.title}')
            continue
        
        if ('cmoa' in bookM.identifiers):
            print(f'skipping {bookM.title} as it already has cmoa id set')
            continue
        
        bookM.identifiers['cmoa'] = f'{series}-{int(bookM.series_index)}'
        api.set_metadata(book, bookM)
        anyChanged = True
    
    if (oneAtATime and anyChanged): break
    
    
    