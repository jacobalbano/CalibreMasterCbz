# CalibreMasterCbz
Simple filetype plugin for calibre to make managing CBZs easier

Designed for my personal use with cmoa.jp and shared in case it's useful. I don't plan to implement features or fix bugs for other people; use at your own risk.

Also, python sucks.

## How this works
The use-case for this plugin is that you want to import multiple books into the same series, all of will have a bunch of fields (author, tags, etc) in common.
Manually editing metadata is a pain in the butt. 

Here's what you need in order for this to work:

### Book Setup
The plugin assumes your library will contain a "master volume" in each series. This is where the metadata will be copied from when you import a new book. However, when you import a master volume for the first time, obviously none of its fields will be present, and there won't be anywhere to copy them from. 

To prepare for later entries in the series, set the following fields in your master volume:
- series
- series_index - **to 1**
- authors
- author_sort

See the Retrofitting section below for an additional step for setting up a master volume that was in your library prior to installing the plugin.

### Importing
- The CBZ or ZIP files you want to import must have a filename that contains a string in the format `cmoa<cid>-<volume>`, otherwise it will not be processed by this plugin
	- Both of these fields should be trimmed of leading zeros
	- The cid field should be the numeric series ID on cmoa.jp; for example, the series found at https://www.cmoa.jp/title/143087/ has a series ID of 143087
	- The volume field is the volume number

All eligable books will have the following fields set automatically:
- language - to 'Japanese'
- tags - to 'CmoaJP' and 'Manga'
- ids - in the form of `cmoa:<cid>-<volume>`

The following fields from the master volume will be copied to the newly imported book:
- series
- authors
- author_sort

The newly imported book will also have the following fields set:
- title - in the format of `<series> (<series_index>)`
- title_sort - same as title

### Retrofitting
If you have existing books in your library that you want to include in this system, all you have to do is manually add an identifier to the ids field. Again, this should be in the format of `cmoa:<cid>-<volume>`, no leading zeros.

You may also want to run the included utility script (`bulk_apply.py`) to automatically generate ids for each volume in every series with a master volume. In the future I might add a toolbar button for this.
