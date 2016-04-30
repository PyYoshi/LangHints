import os
import urllib.request
from bs4 import BeautifulSoup

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
WORKSPACE_DIR = os.path.join(SCRIPT_DIR, '../workspace/wordpress')
TRANS_URL = 'https://make.wordpress.org/polyglots/teams/'
PO_BASE_URL = 'https://translate.wordpress.org/projects/wp/dev/%s/default/export-translations'

class DownLoadObject(object):
	def __init__(self, version, locale_code, locale_label_en, locale_label, wp_locale):
		self.version = version
		self.wp_locale = wp_locale
		self.locale_label_en = locale_label_en
		self.locale_label = locale_label
		self.url = PO_BASE_URL % locale_code

def scrape_html():
	downloadObjects = []
	with urllib.request.urlopen(TRANS_URL) as res:
		html = res.read()
		soup = BeautifulSoup(html, "lxml")
		translators_info = soup.find_all('div', class_='translators-info')
		for translator_info in translators_info:
			tbody = translator_info.find('tbody')
			for tr in tbody.find_all('tr', class_='locale-version latest translated-100'):
				locale_td_left = tr.find('td', attrs={'data-column-title':'Locale'})
				locale_td_right = locale_td_left.find_next('td')
				locale_en = locale_td_left.get_text("|", strip=True)
				locale_label = locale_td_right.get_text("|", strip=True)

				wp_locale_td_left = tr.find('td', attrs={'data-column-title':'WP Locale'})
				wp_locale = wp_locale_td_left.get_text("|", strip=True)
				
				version_td_left = tr.find('td', attrs={'data-column-title':'Version'})
				version = version_td_left.get_text("|", strip=True)

				glotpress_td_left = tr.find('td', attrs={'data-column-title':'GlotPress'})
				glotpress_td_right = glotpress_td_left.find_next('td')
				locale_code = glotpress_td_right.get_text("|", strip=True)

				downloadObjects.append(DownLoadObject(version, locale_code, locale_en, locale_label, wp_locale))
	return downloadObjects

def po_download(downloadObject):
	fpath = os.path.join(WORKSPACE_DIR, downloadObject.wp_locale+'.po')
	urllib.request.urlretrieve(downloadObject.url, fpath)

def main():
	if not os.path.exists(WORKSPACE_DIR):
		os.makedirs(WORKSPACE_DIR)
		
	downloadObjects = scrape_html()
	for downloadObject in downloadObjects:
		po_download(downloadObject)

if '__main__' in __name__:
	main()
