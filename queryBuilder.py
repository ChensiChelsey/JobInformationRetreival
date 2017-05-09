from index import Job
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, A
import re
import datetime
import pprint


'''
in this file are functions used to build elasticsearch queries
'''


es = Elasticsearch(['localhost'], http_auth=('elastic', 'changeme'), port=9200)
global sortedresult
sortedresult = []

# do general search
# input: jobtitle, description, state, city, jobtype, salary, date
# output: list of results
def generalSearch(search,  startpos, latest):
    global sortedresult
    if latest and startpos > 0 and len(sortedresult) > 0:
        return sortedresult[startpos: startpos + 10]
    search = Job.search()
    s = Search(using=es)
    s = s.index('job_index')
    s = s.query(Q('match_all'))

    # title
    if len(search['jobtitle']) > 0:
        s = s.query('multi_match', query = search['jobtitle'], type = 'cross_fields', fields = ['title', 'summary'], operator = 'and')

    # job description
    if len(search['description']) > 0 or len(search['jobtitle']) > 0:
        s = s.query('match', summary = search['jobtitle'] + " " + search['description'])

    # company
    if len(search['company']) > 0:
        s = s.query('match', company=search['company'])

    # location
    if len(search['state']) > 0:
        s = s.query('match_phrase', state = search['state'])
    if len(search['city']) > 0:
        s = s.query('match', city = search['city'])

    # jobtype
    if len(search['jobtype']) > 0:
        s = s.query('match', jobtype=search['jobtype'])

    # salary
    if search['salary'] > 0:
        s = s.query('range', salary = {'gte': search['salary']})

    # date
    if len(search['date']) > 0:
        days = re.findall(r"(\d+)", search['date'])[0]
        days = int(days)
        today = datetime.datetime.now().toordinal()
        s = s.query('range', date = {'gte': today - days})

    pp = pprint.PrettyPrinter(depth = 6)
    pp.pprint(s.to_dict())

    if latest:
        s = s[0:100]
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
        sortedresult = sorted(resultlist, key=lambda d : d['postingdate'], reverse = 1)
        return sortedresult[startpos: startpos+10]
    else:
        s = s[startpos: startpos+10]
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


# search for the jobs posted by the company
def companySearch(company, startpos):
    s = Search(using=es)
    s = s.index('job_index')
    s = s.query('match', company=company)
    s = s[startpos: startpos +10]
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

# recommend jobs based on user's resume
def recommendationSearch(search, startpos):
    s = Search(using=es)
    s = s.index('job_index')

    condition = []
    #location
    if len(search['state']) > 0:
        qState = Q('match_phrase', state=search['state'])
        condition.append(qState)
    if len(search['city']) > 0:
        qCity = Q('match', city=search['city'])
        condition.append(qCity)

    # professional & education background
    if len(search['proBG']) > 0 or len(search['degree']) > 0 or len(search['major']) > 0:
        qBG = Q('multi_match', query=search['proBG'] + ' ' + len(search['degree']) + " " + len(search['major']), type='cross_fields', fields=['title', 'summary'])
        condition.append(qBG)

    # jobtype
    if len(len(search['jobtype'])) > 0:
        qType = Q('match', jobtype=search['jobtype'])
        condition.append(qType)

    # salary
    if search['salary'] > 0:
        qSalary = Q('range', salary={'gte': search['salary']})
        condition.append(qSalary)

    q = Q('bool', should = condition, minimum_should_match = 1)
    s = s.query(q)

    s = s[startpos : startpos + 10]
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

# return one job's detail information based on its id
def jobdetail(id):
    s = Search(using=es)
    s = s.index('job_index')
    s = s.filter('term', _id=id)
    ret = s.execute()
    hit = ret.hits[0].to_dict()
    job = {}
    job['title'] = hit['title']
    job['summary'] = hit['summary']
    job['url'] = 'www.indeed.com' + hit['url']
    job['company'] = hit['company']
    job['location'] = hit['location']
    if hit['salary'] == '':
        job['salary'] = 'Unknown'
    else:
        job['salary'] = hit['salary']
    job['jobtype'] = hit['jobtype']
    return job