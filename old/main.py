print('// Loading...')
from flask import Flask, render_template, request
import json
from pathlib import Path
# import requests as rq
import gzip
import os
from werkzeug.exceptions import HTTPException

cwd = Path(__file__).parent.resolve()
app = Flask('BIBLE', template_folder=cwd/'templates', static_folder=cwd/'static')
app.secret_key = 'key'

with open(cwd/'../index.json') as f:
	index = json.load(f)
with open(cwd/'../book.json') as f:
	bookcodes = json.load(f)
with open(cwd/'../info.json') as f:
	info = json.load(f)

verses = {}
for t in os.listdir(cwd/'../oldjson'):
	tn = t.split('.')[0]
	# with gzip.open(cwd/f'../oldjson/{t}', 'rt', encoding='utf-8') as f:
	# 	tv = f.read()
	# verses[tn] = json.loads(tv)

	with open(cwd/f'../oldjson/{t}', encoding='utf-8') as f:
		verses[tn] = json.load(f)

def rtt(text, redir=None, rtime=2, ctx=''):
	return f'<body style="margin: 0; background: #000000;"><p style="font-family: monospace; margin: 0; text-align: center; color: #ffffff; font-size: 6vh; line-height: 6vh; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%)">{text}</p><p style="position: absolute; bottom: 2vh; width: 70vw; left: 15vw; font-size: 2.75vh; line-height: 2.75vh; font-family: monospace; margin: 0; text-align: center; color: #ffffff;">{ctx}</p></body>' + (f'<script>setTimeout(function() {{ window.location.href = "{redir}"; }}, {rtime*1000});</script>' if redir is not None else '')

@app.errorhandler(Exception)
def error_handler(e):
	code = 500  # Default to Internal Server Error
	if isinstance(e, HTTPException):
		code = e.code
	return rtt(f'Error {code}', ctx=e), code

def getip(request):
    try:
        if request.headers.getlist("X-Forwarded-For"):
            return request.headers.getlist("X-Forwarded-For")[0]
        elif request.headers.get("X-Real-IP"):
            return request.headers.get("X-Real-IP")
        return request.remote_addr
    except Exception:
        return '???'

@app.route('/')
def bibleindex():
	if 'curl' in request.headers.get('User-Agent').lower():
		return '                    ╭──────────────────────╮                    \n                    │   I believe in one   │                    \n                    │   God, the Father    │                    \n                    │  almighty, maker of  │                    \n                    │ heaven and earth, of │                    \n                    │  all things visible  │                    \n                    │   and invisible. I   │                    \n                    │ believe in one Lord  │                    \n                    │  Jesus Christ, the   │                    \n                    │ Only Begotten Son of │                    \n╭───────────────────╯   God, born of the   ╰───────────────────╮\n│ Father before all ages. God from God, Light from Light, true │\n│  God from true God, begotten, not made, consubstantial with  │\n│ the Father; through him all things were made. For us men and │\n│ for our salvation he came down from heaven, and by the Holy  │\n│ Spirit was incarnate of the Virgin Mary, and became man. For │\n│ our sake he was crucified under Pontius Pilate, he suffered  │\n│   death and was buried, and rose again on the third day in   │\n│ accordance with the Scriptures. He ascended into heaven and  │\n│   is seated at the right hand of the Father. He will come    │\n╰───────────────────╮  again in glory to   ╭───────────────────╯\n                    │ judge the living and │                    \n                    │   the dead and his   │                    \n                    │ kingdom will have no │                    \n                    │  end. I believe in   │                    \n                    │ the Holy Spirit, the │                    \n                    │  Lord, the giver of  │                    \n                    │  life, who proceeds  │                    \n                    │ from the Father and  │                    \n                    │  the Son, who with   │                    \n                    │  the Father and the  │                    \n                    │  Son is adored and   │                    \n                    │ glorified, who has   │                    \n                    │  spoken through the  │                    \n                    │ prophets. I believe  │                    \n                    │    in one, holy,     │                    \n                    │     catholic and     │                    \n                    │   apostolic Church.  │                    \n                    │    I confess one     │                    \n                    │   Baptism for the    │                    \n                    │ forgiveness of sins  │                    \n                    │  and I look forward  │                    \n                    │ to the resurrection  │                    \n                    │ of the dead and the  │                    \n                    │  life of the world   │                    \n                    │       to come.       │                    \n                    │                      │                    \n                    │         Amen.        │                    \n                    │                      │                    \n                    ╰──────────────────────╯                    \n'
	return rtt('Coming Soon...')

@app.route('/ping')
def ping():
    return rtt('Pong')

@app.route('/v')
def version():
	vern, updl = '1.4.8', 'Added more translations: ESV, MSG, and NLT'
	if 'curl' in request.headers.get('User-Agent').lower():
		return f'bible.pythonanywhere.com\nVersion {vern}\n- {updl}\n'
	return rtt(f'V{vern}', ctx=updl)

def numbers(num: str, string: bool=False) -> list[int]:
	resp, nums = [], num.split(';')
	for i in nums:
		if '-' in i: resp.extend(range(int(i.split('-')[0]), int(i.split('-')[1])+1))
		else: resp.append(i)
	if not string: return [int(i) for i in resp]
	return [str(i) for i in resp]

def book(bn: str) -> str | None: return bookcodes[bn.lower()] if bn.lower() in bookcodes.keys() else None

def vc2(tr, rcode):
	code = ['il' if tr == '' else tr, ':'.join(rcode.split(':')[1:])]
	if code[0].lower() not in verses.keys(): return 'Invalid Translation '+code[0]

	if ':' not in code[1]:
		try:
			return [[code[0].lower(), book(verses[code[0].lower()][i]['short-book']), verses[code[0].lower()][i]['chapter'], verses[code[0].lower()][i]['verse-number']] for i in numbers(code[1])]
		except Exception: pass
	code = [code[0], code[1].split(':')]
	if len(code[1]) == 1:
		resp, rresp = [], [[[code[0].lower(), book(code[1][0]), i, j] for j in info[code[0].lower()][book(code[1][0])][i]] for i in info[code[0].lower()][book(code[1][0])]]
		for i in rresp: resp.extend(i)
	elif len(code[1]) == 2:
		resp, rresp = [], [[[code[0].lower(), book(code[1][0]), i, j] for j in info[code[0].lower()][book(code[1][0])][i]] for i in numbers(code[1][1], True)]
		for i in rresp: resp.extend(i)
	elif len(code[1]) == 3:
		resp = [[code[0].lower(), book(code[1][0]), code[1][1], i] for i in numbers(code[1][2])]
	return resp

def vc(rcode):
	fresp = []

	if rcode[0] in '!=':
		tr = [j for i in rcode[1:].split(':')[0].split(';') for j in (verses.keys() if i == '*' else [i])]  # rcode[1:].split(':')[0].split(';')
		grid_columns = len(tr)
		vc2r = None
		for tri in tr:
			try:
				vc2r = vc2(tri, rcode[1:])
				break
			except Exception: pass
		if vc2r is None: raise ValueError('Cannot find book/chapters in any supplied translations')
		resp = [[['il' if j == '' else j, *i[1:]] for j in tr] for i in vc2r]
		for i in resp: fresp.extend(i)
	else:
		grid_columns = 1
		for tr in [j for i in rcode.split(':')[0].split(';') for j in (verses.keys() if i == '*' else [i])]:
			fresp.extend(vc2(tr, rcode))

	final = []
	for i in fresp:
		try: final.append([i[0], index[i[1]][i[2]][str(i[3])][i[0]]])
		except IndexError: pass
	return {'': 1, '!': 1, '=': grid_columns}[rcode[0] if rcode[0] in '!=' else ''], final

def guess_lang(canon: str) -> str:
	return 'hebrew' if canon == 'Old Testament' or canon == 'Apocrypha' else 'greek'

@app.route('/verse')
def verse_build():
	return render_template('verse_build.html')

def verse_table_format(table: list) -> str:
	column_widths = [max([len(i[n]) for i in table]) for n in range(len(table[0]))]
	return '\n'.join([' | '.join([eval(f"f'{{c:{(['^'] if len(column_widths) <= 1 else ['>', *['^']*(len(column_widths)-2), '<'])[n]}{{column_widths[n]}}}}'") for n, c in enumerate(r)]) for r in table])

def verse_to_copy_text(verse: str | list, include: list[int]=[0, 1, 1]) -> str:
	if isinstance(verse, str):
		ver = verse.replace('<b>', '').replace('</b>', '')
		ver = [(i[:-2] if i[-2:] == '</' else (i if i[-1] != '<' else i[:-1]), i[-2:] == '</') for i in ver.split('table>') if i != '']
		ver = ''.join([i[0] if not i[1] else '\n'+verse_table_format([j[4:-5].split('</td><td>') for j in i[0][4:-5].split('</tr><tr>')])+'\n' for i in ver])
		return ver
	elif isinstance(verse, list):
		return ' '.join([
			' '.join([
				j for j in [
					None if i[1] == '' or not include[1] else i[1],
					None if i[0] == '' or not include[0] else f'[{i[0]}]',
					None if i[2] == '' or not include[2] else f'({i[2]})'
				] if j is not None
			])
		for i in verse])
	return ''

@app.route('/verse/<verse_code>')
def verse(verse_code):
	# TODO: MAKE SCRAPE FOR IL USE ALL IL BOOKS, SCRAPE THE BOOKS FROM BIBLEHUB TO MAKE SURE
	# AND ALSO FIX THE THING WHERE LANGUAGE ISNT COMING UP IDK WHY
	# TODO: MAYBE Filter duplicate verses (text not index) before viewing (only if together)
	# So if we had verse1 verse1 verse2 it would remove 1 verse1 (even if different verse indexes), but not here: verse1 verse2 verse1
	# TODO: Create settings menu in template and save settings in cookies (or some way to save settings)

	# rq.get(f'https://xdroid.net/api/message?k={os.getenv("XDROID")}&t={getip(request)}&c={verse_code}&u=https://iplocation.io/ip/{getip(request)}')

	vcs, vlid = [], -1
	for i in verse_code.split(','):
		vci, rvci = vc(i), []
		for j in vci[1]:
			vlid += 1
			rvci.append([j[0], j[1], vlid])
		vcs.append((vci[0], rvci))
	if 'curl' in request.headers.get('User-Agent').lower():
		return ('\n\n'.join(['\n\n'.join([f"{verses[i[0]][i[1]]['book']} {verses[i[0]][i[1]]['chapter']}:{verses[i[0]][i[1]]['verse-number-text']} ({i[0].upper()})\n{verse_to_copy_text(verses[i[0]][i[1]]['verse'])}" for i in j[1]]) for j in vcs]))+'\n'
	return render_template('verse.html', verses=[{'columns': j[0], 'verses': [{
		'translation': i[0].upper(),
		'lang': guess_lang(verses[i[0]][i[1]]['canon']) if i[0] == 'il' and verses[i[0]][i[1]]['canon'] != 'None' else ('eng' if verses[i[0]][i[1]]['canon'] != 'None' else 'None'),  # verses[i[0]][i[1]]['lang']
		'book': verses[i[0]][i[1]]['book'],
		'book-info': verses[i[0]][i[1]]['book-desc'].replace('The Gospel According to', 'The Holy Gospel According to'),
		'chapter': verses[i[0]][i[1]]['chapter'],
		'verse-number-text': verses[i[0]][i[1]]['verse-number-text'],
		'book-desc': verses[i[0]][i[1]]['heading'],
		'footnotes': verses[i[0]][i[1]]['footnotes'],
		'chapter-footnotes': verses[i[0]][i[1]]['chapter-footnotes'],
		'verse': verses[i[0]][i[1]]['verse'] if i[0] == 'il' else verses[i[0]][i[1]]['verse'].replace('\n', '<br>'),
		'vlid': i[2],
		'copy-text': verse_to_copy_text(verses[i[0]][i[1]]['verse']),
		'link': f"https://bible.pythonanywhere.com/verse/{i[0].upper()}:{verses[i[0]][i[1]]['short-book'].capitalize()}:{verses[i[0]][i[1]]['chapter'].upper()}:{verses[i[0]][i[1]]['verse-number']}"
	} for i in j[1]]} for j in vcs])

print('// Done')

#####

app.run()