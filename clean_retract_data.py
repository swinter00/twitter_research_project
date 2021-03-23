import os
import json
import re

with open(os.path.dirname(os.path.abspath(__file__)) + "/retracted_articles1.tsv", "r") as f:
	lines = f.readlines()

article_info = []

for line in lines:
	info = {}
	title = line.split("\t")[0].replace(',”', '').replace('”', '').replace('“', '')

	search = re.search(r'(https://.+)\s+(https://.+)', line.strip())
	if search:
		url = search.group(1).replace('\t', '').replace('N/A', '')
		doi = search.group(2)
	else:
		search = re.search(r'(https://.+)\s+N/A', line.strip())
		if search:
			url = search.group(1).replace('\tN/A', '')
		else:
			url = None
		doi = None

	info['title'] = title
	info['url'] = url
	info['doi'] = doi
	article_info.append(info)

info_json = json.dumps(article_info)

with open(os.path.dirname(os.path.abspath(__file__)) + "/article_info.json", "w") as f:
	f.write(info_json)
