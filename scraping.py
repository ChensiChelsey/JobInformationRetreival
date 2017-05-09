# -*- coding=UTF-8 -*-
import json
import sys

# Search settings
KEYWORD_FILTER = ['IT', 'Software', 'engineer', 'developer', 'scientist', 'computer', 'researcher','technician', 'data', 'specialist', 'designer']
LOCATION_FILTER = ""

# Other settings
MAX_PAGES_COMPANIES = 1000
MAX_PAGES_REVIEWS = 100


import indeed

jobs = {}
id = 0
for key in KEYWORD_FILTER:
    id = indeed.get_jobs(key, LOCATION_FILTER, MAX_PAGES_COMPANIES, id, jobs)
    if id > 3000:
        break
#print jobs
reload(sys)
sys.setdefaultencoding('utf-8')

f = open("jobcorpusupdate.json", "w+")
jsontext = json.dumps(jobs, ensure_ascii=False, indent=4)
f.write(jsontext)
f.close()
