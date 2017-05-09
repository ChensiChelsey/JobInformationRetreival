# -*- coding=UTF-8 -*-
import json
import sys

'''
this file is used to add new job postings from indeed in real time.
It runs in background and crawl the latest job postings every hour.
'''


# Search settings
KEYWORD_FILTER = ['IT', 'Software', 'engineer', 'developer', 'scientist', 'computer', 'researcher','technician', 'data', 'specialist', 'designer']
LOCATION_FILTER = ""

# Other settings
MAX_PAGES_COMPANIES = 1000
MAX_PAGES_REVIEWS = 100

import indeed
import datetime
import time
from index import prepareIndex



while True:
    # get current time
    starttime = datetime.datetime.now()
    jobs = {}
    id = 0
    # do searching and crawling the postings of last hour
    for key in KEYWORD_FILTER:
        id = indeed.get_jobs(key, LOCATION_FILTER, MAX_PAGES_COMPANIES, id, jobs, starttime)

    # add the index into elasticsearch
    prepareIndex(jobs)

    # sleep until next hour
    current = datetime.datetime.now()
    dif = 3600 - (current - starttime).total_seconds()
    time.sleep(dif)