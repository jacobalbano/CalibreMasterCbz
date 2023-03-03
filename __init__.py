import re

from calibre.customize import FileTypePlugin
from calibre.constants import DEBUG

class CmoaCbz(FileTypePlugin):
    name                	= 'CMOA.jp CBZ processor'
    description         	= 'Set a cmoa id based on filename, then copy various fields from another volume in the series'
    supported_platforms 	= ['windows', 'osx', 'linux']
    author              	= 'Jacob Albano'
    version             	= (1, 1, 0)
    file_types          	= set(['cbz', 'zip'])
    on_postimport      		= True
    minimum_calibre_version = (0, 7, 53)
    
    pattern = re.compile('cmoa(\\d+)-(\\d+)')

    def postimport(self, book_id, _, db):
        db = db.new_api
        
        thisBookTitle = db.field_for('title', book_id)
        if (thisBookTitle is None):
            if DEBUG: print('no book title')
            pass
        
        match = self.pattern.search(thisBookTitle)
        if (match is None):
            if DEBUG: print(f'no regex match for book title {thisBookTitle}')
            pass
        
        seriesId = int(match.group(1))
        volNum = int(match.group(2))
        if DEBUG: print((seriesId, volNum))
        
        thisMeta = db.get_metadata(book_id)
        thisMeta.set_identifier('cmoa', f'{seriesId}-{volNum}')
        thisMeta.tags = ['CmoaJP','Manga']
        thisMeta.languages = ['jpn']
        
        searchResults = db.search(f'identifiers:=cmoa:~^{seriesId}-')
        
        if (len(searchResults) > 0):
            if DEBUG: print('copying metadata from existing volume')
            otherMeta = db.get_metadata(min(searchResults))
            thisMeta.series = otherMeta.series
            thisMeta.series_index = volNum
            thisMeta.authors = otherMeta.authors
            thisMeta.author_sort = otherMeta.author_sort
            thisMeta.title = f'{otherMeta.series} ({volNum})'
            thisMeta.title_sort = thisMeta.title
            
        db.set_metadata(book_id, thisMeta)
