import os
import execjs
import simplejson

from models import Entry, Serializer

APP_TAG = 'vscode'
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
I18N_DIR = os.path.join(SCRIPT_DIR, '../workspace/vscode/i18n')
OUTPUT_JSON_PATH = os.path.join(SCRIPT_DIR, '../generated/vscode.json')

nodejs = execjs.get("Node")

def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            s = os.path.join(root, file)
            yield os.path.join(root, file)

def main():
	pass

if '__main__' in __name__:
	main()