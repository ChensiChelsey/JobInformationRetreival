# -*- coding=UTF-8 -*-
import json
import sys

# Search settings
KEYWORD_FILTER = "IT"
LOCATION_FILTER = ""

# Other settings
MAX_PAGES_COMPANIES = 1000
MAX_PAGES_REVIEWS = 100

import os
import re
from datetime import datetime
import indeed

jobs = indeed.get_jobs(KEYWORD_FILTER, LOCATION_FILTER, MAX_PAGES_COMPANIES)
#print jobs
reload(sys)
sys.setdefaultencoding('utf-8')

f = open("jobcorpus100.json", "w+")
jsontext = json.dumps(jobs, ensure_ascii=False, indent=4)
f.write(jsontext)
f.close()
