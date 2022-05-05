import re

from calibre.customize import FileTypePlugin, InterfaceActionBase
from calibre.constants import DEBUG

class CmoaCbz(FileTypePlugin):
    name                	= 'CMOA.jp CBZ processor'
    description         	= 'Set a cmoa id based on filename, then copy various fields from the first volume in the series'
    supported_platforms 	= ['windows', 'osx', 'linux']
    author              	= 'Jacob Albano'
    version             	= (1, 0, 0)
    file_types          	= set(['cbz', 'zip'])
    on_postimport      		= True
    minimum_calibre_version = (0, 7, 53)
    
    pattern = re.compile('cmoa(\\d+)-(\\d+)')

    def postimport(self, book_id, book_format, db):
        db = db.new_api
        
        thisBookTitle = db.field_for('title', book_id)
        if (thisBookTitle is None):
            print('no book title')
            pass
        
        match = self.pattern.search(thisBookTitle)
        if (match is None):
            if DEBUG: print(f'no regex match for book title {thisBookTitle}')
            pass
        
        seriesId = int(match.group(1))
        volNum = int(match.group(2))
        print((seriesId, volNum))
        
        thisMeta = db.get_metadata(book_id)
        thisMeta.set_identifier('cmoa', f'{seriesId}-{volNum}')
        thisMeta.tags = ['CmoaJP','Manga']
        thisMeta.languages = ['jpn']
        
        if (volNum != 1):
            searchResults = db.search(f'identifiers:=cmoa:={seriesId}-1')
            if (len(searchResults) == 1):
                if DEBUG: print('copying metadata from first volume')
                v1Meta = db.get_metadata(min(searchResults))
                thisMeta.series = v1Meta.series
                thisMeta.series_index = volNum
                thisMeta.authors = v1Meta.authors
                thisMeta.author_sort = v1Meta.author_sort
                thisMeta.title = f'{v1Meta.series} ({volNum})'
                thisMeta.title_sort = thisMeta.title
            else:
                if DEBUG: print('found more than one first volume, skipping')
        else:
            if DEBUG: print('skipping metadata copy for volume 1')
            
        db.set_metadata(book_id, thisMeta)
