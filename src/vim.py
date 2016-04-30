import os
import polib
import simplejson

from models import Entry, Serializer

APP_TAG = 'vim'
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
VIM_LOCALES_DIR = os.path.join(SCRIPT_DIR, '../workspace/vim/src/po')
OUTPUT_JSON_PATH = os.path.join(SCRIPT_DIR, '../generated/vim.json')

def po_listup():
	poFilePaths = []
	for p in os.listdir(VIM_LOCALES_DIR):
		c = p.split('.')
		if len(c) == 2 and c[-1] == 'po':
			file_path = os.path.join(VIM_LOCALES_DIR, p)
			if os.path.isfile(file_path):
				poFilePaths.append(file_path)
	return poFilePaths

def po_parse(loc, po_path):
	po = polib.pofile(po_path)
	entries = []
	for entry in po:
		entries.append(Entry(APP_TAG, loc, entry.msgid, entry.msgstr))
	return entries

def main():
	catalogs = {}
	for poFilePath in po_listup():
		loc = poFilePath.split('/')[-1].split('.')[0]
		entries = po_parse(loc, poFilePath)
		catalogs[loc] = entries
	with open(OUTPUT_JSON_PATH, 'w') as fp:
		j = simplejson.dumps(catalogs, cls=Serializer, sort_keys=True, indent=2 * ' ')
		fp.write(j)

if '__main__' in __name__:
	main()
