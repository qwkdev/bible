import json
import os
translations = ['gnbdk', 'il', 'csb', 'esv', 'kjv', 'msg', 'niv', 'nkjv', 'nlt']

_ = {
	"id": 1,
	"short-canon": "ot",
	"canon": "Old Testament",
	"short-book": "gen",
	"book": "Genesis",
	"book-desc": "The First Book of Moses called Genesis",
	"chapter-index": 0,
	"chapter": "1",
	"heading": "The Story of Creation",
	"verse-index": 0,
	"verse-number": 1,
	"verse-number-text": "1",
	"verse": "In the beginning, when God created the universe,",
	"footnotes": "1.1 In the beginning\u2026 the universe; or In the beginning God created the universe; or When God began to create the universe.",
	"chapter-footnotes": ""
}
_ = {
	"id": 1,
	"short-canon": "ot",
	"canon": "Old Testament",
	"short-book": "gen",
	"book": "Genesis",
	"book-desc": "The First Book of Moses called Genesis",
	"chapter-index": 0,
	"chapter": "1",
	"heading": "The Beginning",
	"verse-index": 0,
	"verse-number": 1,
	"verse-number-text": "1",
	"verse": [
		["b\u0259\u00b7r\u00ea\u00b7\u0161\u00ee\u1e6f", "\u05d1\u05b0\u05bc\u05e8\u05b5\u05d0\u05e9\u05b4\u05c1\u0596\u05d9\u05ea", "In the beginning"],
		["b\u0101\u00b7r\u0101", "\u05d1\u05b8\u05bc\u05e8\u05b8\u05a3\u05d0", "created"],
		["\u2019\u0115\u00b7l\u014d\u00b7h\u00eem;", "\u05d0\u05b1\u05dc\u05b9\u05d4\u05b4\u0591\u05d9\u05dd", "God"],
		["\u2019\u00ea\u1e6f", "\u05d0\u05b5\u05a5\u05ea", ""],
		["ha\u0161\u00b7\u0161\u0101\u00b7ma\u00b7yim", "\u05d4\u05b7\u05e9\u05b8\u05bc\u05c1\u05de\u05b7\u0596\u05d9\u05b4\u05dd", "the heavens"],
		["w\u0259\u00b7\u2019\u00ea\u1e6f", "\u05d5\u05b0\u05d0\u05b5\u05a5\u05ea", "and"],
		["h\u0101\u00b7\u2019\u0101\u00b7re\u1e63.", "\u05d4\u05b8\u05d0\u05b8\u05bd\u05e8\u05b6\u05e5\u05c3", "the earth"],
		["", ".", ""]
	],
	"footnotes": "",
	"chapter-footnotes": "John 1:1-5"}

def rstrip(array: list, delimiter) -> list:
	for i in range(len(array)-1, -1, -1):
		if array[i] != delimiter:
			return array[:i+1]

def fn(s: str, force: bool=False) -> str | None:
	if not s:
		if force: 
			print('Invalid param')
			exit()
		else:
			return None
	return s

def check(b, s):
	if not s.isdigit(): print(b, s)

def main(translation: str, interlinear: bool=False) -> None:
	print(f'Formatting {translation}...')
	with open(f'oldjson/{translation}.json', encoding='utf-8') as f:
		data = json.load(f)

	books = {}

	text = {}
	for v in data:
		if v['canon'] == 'None': continue
		bk = v['short-book']

		if bk not in text:
			text[bk] = {'info': {
				'short-canon': v['short-canon'],
				'canon': v['canon'],
				'name': v['book'],
				'desc': fn(v['book-desc'].replace('The Gospel According to', 'The Holy Gospel According to')),
				'interlinear': interlinear
			}}

			books[bk] = set()
		
		if bk in books:
			books[bk].add(fn(v['book-desc']))

		if v['chapter'] not in text[bk]:
			text[bk][v['chapter']] = {}

		# check(bk, v['chapter'])
		# check(bk, v['verse-number-text'])

		text[bk][v['chapter']][v['verse-number-text']] = rstrip([
			v['verse'], fn(v['footnotes']), fn(v['chapter-footnotes'])
		], None)

		
	for b, d in books.items():
		if len(d) > 1: print('Multiple Book Descriptions:', b, d)

	try: os.mkdir(f'text/{translation}')
	except Exception: pass
	for n, b in text.items():
		with open(f'text/{translation}/{n}.json', 'w', encoding='utf-8') as f:
			json.dump(b, f, separators=(',', ':'))

[main(t, t == 'il') for t in translations]
print('Done')