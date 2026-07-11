import requests as rq
from bs4 import BeautifulSoup
import os
import json

BOOKS = {'gn':'gen','genesis':'gen','gen':'gen','ge':'gen','ex':'exo','exod':'exo','exo':'exo','exodus':'exo','leviticus':'lev','le':'lev','lv':'lev','lev':'lev','num':'num','nu':'num','numbers':'num','nb':'num','nm':'num','deuteronomy':'deu','dt':'deu','de':'deu','deu':'deu','deut':'deu','jsh':'jos','jos':'jos','joshua':'jos','josh':'jos','jdgs':'jdg','judges':'jdg','jg':'jdg','jdg':'jdg','judg':'jdg','ru':'rut','ruth':'rut','rut':'rut','rth':'rut','1s':'1sa','1stsam':'1sa','1sm':'1sa','1samuel':'1sa','1sam':'1sa','firstsam':'1sa','1stsamuel':'1sa','firstsamuel':'1sa','1sa':'1sa','2s':'2sa','secondsamuel':'2sa','2ndsamuel':'2sa','2sam':'2sa','2sa':'2sa','secondsam':'2sa','2ndsam':'2sa','2samuel':'2sa','2sm':'2sa','firstkgs':'1ki','1stkings':'1ki','1stkgs':'1ki','1kings':'1ki','1kgs':'1ki','1k':'1ki','1ki':'1ki','1kin':'1ki','firstkings':'1ki','2k':'2ki','2ndkings':'2ki','2kin':'2ki','2ki':'2ki','2kgs':'2ki','2kings':'2ki','secondkings':'2ki','secondkgs':'2ki','2ndkgs':'2ki','1chron':'1ch','1chr':'1ch','1ch':'1ch','1stchron':'1ch','firstchron':'1ch','1stchronicles':'1ch','1chronicles':'1ch','firstchronicles':'1ch','2ndchronicles':'2ch','2chron':'2ch','2ch':'2ch','2chr':'2ch','2ndchron':'2ch','2chronicles':'2ch','secondchronicles':'2ch','secondchron':'2ch','ezr':'ezr','ezra':'ezr','ez':'ezr','neh':'neh','ne':'neh','nehemiah':'neh','addes':'est','restofesther':'est','aes':'est','est':'est','additionstoesther':'est','addesth':'est','therestofesther':'est','job':'job','jb':'job','psa':'psa','pss':'psa','psm':'psa','psalms':'psa','psalm':'psa','ps':'psa','pslm':'psa','prov':'pro','pro':'pro','proverbs':'pro','pr':'pro','prv':'pro','ecc':'ecc','eccles':'ecc','eccle':'ecc','qoh':'ecc','ecclesiastes':'ecc','ec':'ecc','canticleofcanticles':'sng','so':'sng','sng':'sng','canticles':'sng','sos':'sng','songofsolomon':'sng','cant':'sng','songofsongs':'sng','song':'sng','isa':'isa','is':'isa','isaiah':'isa','jr':'jer','jeremiah':'jer','jer':'jer','je':'jer','lam':'lam','la':'lam','lamentations':'lam','ezek':'ezk','ezk':'ezk','eze':'ezk','ezekiel':'ezk','daniel':'dan','dn':'dan','dan':'dan','da':'dan','ho':'hos','hosea':'hos','hos':'hos','joel':'jol','jl':'jol','jol':'jol','amo':'amo','am':'amo','amos':'amo','obadiah':'oba','ob':'oba','oba':'oba','obad':'oba','jonah':'jon','jon':'jon','jnh':'jon','micah':'mic','mc':'mic','mic':'mic','nah':'nam','nahum':'nam','na':'nam','nam':'nam','hab':'hab','hb':'hab','habakkuk':'hab','zp':'zep','zephaniah':'zep','zep':'zep','zeph':'zep','haggai':'hag','hag':'hag','hg':'hag','zech':'zec','zc':'zec','zechariah':'zec','zec':'zec','ml':'mal','mal':'mal','malachi':'mal','mat':'mat','matthew':'mat','matt':'mat','mt':'mat','mrk':'mrk','mark':'mrk','mk':'mrk','mr':'mrk','mar':'mrk','luk':'luk','lk':'luk','luke':'luk','joh':'jhn','jn':'jhn','john':'jhn','jhn':'jhn','ac':'act','act':'act','acts':'act','rom':'rom','rm':'rom','romans':'rom','ro':'rom','1corinthians':'1co','1cor':'1co','1co':'1co','firstcorinthians':'1co','1stcorinthians':'1co','2cor':'2co','2ndcorinthians':'2co','2corinthians':'2co','2co':'2co','secondcorinthians':'2co','ga':'gal','gal':'gal','galatians':'gal','eph':'eph','ephes':'eph','ephesians':'eph','philippians':'php','phil':'php','php':'php','pp':'php','colossians':'col','col':'col','co':'col','firstthess':'1th','1thessalonians':'1th','1thess':'1th','1thes':'1th','1stthessalonians':'1th','1stthess':'1th','1th':'1th','firstthessalonians':'1th','2thes':'2th','2ndthessalonians':'2th','2thess':'2th','2ndthess':'2th','2thessalonians':'2th','secondthess':'2th','secondthessalonians':'2th','2th':'2th','1ti':'1ti','firsttimothy':'1ti','firsttim':'1ti','1timothy':'1ti','1tim':'1ti','1sttimothy':'1ti','1sttim':'1ti','2timothy':'2ti','2ndtimothy':'2ti','2ti':'2ti','2tim':'2ti','secondtimothy':'2ti','2ndtim':'2ti','secondtim':'2ti','ti':'tit','tit':'tit','titus':'tit','pm':'phm','phm':'phm','phi':'phm','philemon':'phm','philem':'phm','heb':'heb','hebrews':'heb','jas':'jas','jm':'jas','james':'jas','1pe':'1pe','firstpeter':'1pe','1pt':'1pe','1p':'1pe','1peter':'1pe','1stpeter':'1pe','1pet':'1pe','2pt':'2pe','2pe':'2pe','2peter':'2pe','2pet':'2pe','2p':'2pe','secondpeter':'2pe','2ndpeter':'2pe','1jn':'1jn','1j':'1jn','1jhn':'1jn','1john':'1jn','1jo':'1jn','1stjohn':'1jn','firstjohn':'1jn','1joh':'1jn','secondjohn':'2jn','2jhn':'2jn','2j':'2jn','2jo':'2jn','2jn':'2jn','2joh':'2jn','2john':'2jn','2ndjohn':'2jn','3jn':'3jn','3rdjohn':'3jn','3joh':'3jn','3john':'3jn','3j':'3jn','3jo':'3jn','thirdjohn':'3jn','3jhn':'3jn','jd':'jud','jude':'jud','jud':'jud','therevelation':'rev','rev':'rev','re':'rev','revelation':'rev','mostcommon:rev':'rev','tob':'tob','tb':'tob','tobit':'tob','jdth':'jdt','judith':'jdt','jdt':'jdt','jth':'jdt','ws':'wis','wisdom':'wis','wis':'wis','wisd.ofsol':'wis','wisdomofsolomon':'wis','sir':'sir','ecclus':'sir','ecclesiasticus':'sir','bar':'bar','baruch':'bar','1mac':'1ma','1m':'1ma','1macc':'1ma','1stmaccabees':'1ma','1maccabees':'1ma','firstmaccabees':'1ma','1ma':'1ma','2mac':'2ma','2maccabees':'2ma','2macc':'2ma','2ma':'2ma','2ndmaccabees':'2ma','2m':'2ma','secondmaccabees':'2ma'}

canon = {
	'OT': ['ot', 'Old Testament'],
	'NT': ['nt', 'New Testament']
}

curbook = None
data = {}

for translation in [
	'NIV'
]:
	os.system('cls')
	print(translation)

	chapterdata = {BOOKS.get(i['display'].lower().replace(' ', '')): i['testament'] for i in rq.get(f'https://www.biblegateway.com/passage/bcv/?version={translation}').json()['data'][0]}
	
	# r = rq.get(f'https://www.biblegateway.com/passage/?search=Genesis%201&version={translation}').content
	r = rq.get(f'https://www.biblegateway.com/passage/?search=1%20Chronicles%201&version={translation}').content
	soup = BeautifulSoup(r, 'html.parser')

	book = ' '.join(soup.select_one('.dropdown-display-text').text.split(' ')[:-1])
	realbook = BOOKS.get(book.lower().replace(' ', ''))
	if not realbook: raise Exception(f'Couldn\'t identify book {book}')
	if realbook != curbook:
		if curbook:
			try: os.mkdir(f'scrape/{translation.lower()}')
			except Exception: pass

			with open(f'scrape/{translation.lower()}/{realbook}.json', 'w', encoding='utf-8') as f:
				json.dump(data, f, separators=(',', ':'))
			print(book)

		data = {
			'info': {
				'short-canon': canon[chapterdata[realbook]][0],
				'canon': canon[chapterdata[realbook]][1],
				'name': book,
				'desc': None,
				'interlinear': False,
				'rtl': False
			}
		}

	text = [i for i in [
		soup.select_one('.std-text'),
		soup.select_one('.passage-text>div>div')
	] if i][0]

	for child in text.children:
		if not child.name: continue
		print(child.name)
	