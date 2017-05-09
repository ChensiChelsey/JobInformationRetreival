from index import Job
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, A
import re
import datetime
import pprint

es = Elasticsearch(['localhost'], http_auth=('elastic', 'changeme'), port=9200)

# input: jobtitle, description, state, city, jobtype, salary, date
# index:
def generalSearch(jobtitle, description, state, city, company, jobtype, salary, date, startpos):
    search = Job.search()
    s = Search(using=es)
    s = s.index('job_index')
    s = s.query(Q('match_all'))

    # title
    if len(jobtitle) > 0:
        s = s.query('multi_match', query = jobtitle, type = 'cross_fields', fields = ['title', 'summary'], operator = 'and')

    # job description
    if len(description) > 0:
        s = s.query('match', summary = jobtitle + " " + description)

    # company
    if len(company) > 0:
        s = s.query('match', company=company)

    # location
    if len(state) > 0:
        s = s.query('match_phrase', state = state)
    if len(city) > 0:
        s = s.query('match', city = city)

    # jobtype
    if len(jobtype) > 0:
        s = s.query('match', jobtype=jobtype)

    # salary
    if salary > 0:
        s = s.query('range', salary = {'gte': salary})

    # date
    if len(date) > 0:
        days = re.findall(r"(\d+)", date)[0]
        days = int(days)
        today = datetime.datetime.now().toordinal()
        s = s.query('range', date = {'gte': today - days})

    pp = pprint.PrettyPrinter(depth = 6)
    pp.pprint(s.to_dict())

    s = s[startpos * 10: (startpos+1) * 10]
    response = s.execute()

    resultlist = []
    print response.hits.total
    for hit in response.hits:
        result = {}
        result['score'] = hit.meta.score
        result['title'] = hit['title']
        result['summary'] = hit['summary'][:200]
        result['url'] = 'www.indeed.com' + hit['url']
        result['company'] = hit['company']
        result['location'] = hit['location']
        result['postingdate'] = str(datetime.datetime.fromordinal(hit['date']))
        resultlist.append(result)

    return resultlist

def companySearch(company, startpos):
    search = Job.search()
    s = Search(using=es)
    s = s.index('job_index')
    s = s.query('match', company=company)
    s = s[startpos * 10: (startpos + 1) * 10]
    response = s.execute()

    resultlist = []
    print response.hits.total
    for hit in response.hits:
        result = {}
        result['score'] = hit.meta.score
        result['title'] = hit['title']
        result['summary'] = hit['summary'][:200]
        result['url'] = 'www.indeed.com' + hit['url']
        result['company'] = hit['company']
        result['location'] = hit['location']
        result['postingdate'] = str(datetime.datetime.fromordinal(hit['date']))
        resultlist.append(result)

    return resultlist

def recommendationSearch(state, city, proBG, eduBG_degree, eduBG_major, salary, jobtype, startpos):
    search = Job.search()
    s = Search(using=es)
    s = s.index('job_index')

    condition = []
    #location
    if len(state) > 0:
        qState = Q('match_phrase', state=state)
        condition.append(qState)
    if len(city) > 0:
        qCity = Q('match', city=city)
        condition.append(qCity)

    # professional & education background
    if len(proBG) > 0:
        qBG = Q('multi_match', query=proBG + ' ' + eduBG_degree + " " + eduBG_major, type='cross_fields', fields=['title', 'summary'])
        condition.append(qBG)

    # jobtype
    if len(jobtype) > 0:
        qType = Q('match', jobtype=jobtype)
        condition.append(qType)

    # salary
    if salary > 0:
        qSalary = Q('range', salary={'gte': salary})
        condition.append(qSalary)

    q = Q('bool', should = condition, minimum_should_match = 1)
    s = s.query(q)

    s = s[startpos * 10: (startpos + 1) * 10]
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint(s.to_dict())
    response = s.execute()

    resultlist = []
    print response.hits.total
    for hit in response.hits:
        result = {}
        result['score'] = hit.meta.score
        result['title'] = hit['title']
        result['summary'] = hit['summary'][:200]
        result['url'] = 'www.indeed.com' + hit['url']
        result['company'] = hit['company']
        result['location'] = hit['location']
        result['postingdate'] = str(datetime.datetime.fromordinal(hit['date']))
        resultlist.append(result)

    return resultlist


