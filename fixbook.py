import json

with open('oldbook.json') as f:
	old = json.load(f)

new = {}
for k, v in old.items():
	n = k.replace('_', ' ').replace('-', ' ')
	if n.startswith('i ') or n.startswith('ii ') or n.startswith('iii '):
		continue

	n = n.replace(' ', '')
	if n in new and new[n] != v:
		print('Mismatch', n, new[n], v)
		exit()
	
	new[n] = v

with open('book.json', 'w') as f:
	json.dump(new, f, separators=(',', ':'))