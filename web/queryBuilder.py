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
def generalSearch(search):
    global sortedresult
    print search
    search['offset'] = int(search['offset'])
    if search['sort_by_date'] and search['offset'] > 0 and len(sortedresult) > 0:
        return sortedresult[search['offset']: search['offset'] + 10]
    s = Search(using=es)
    s = s.index('job_index')
    s = s.query(Q('match_all'))

    # title
    if search.has_key('jobtitle'):
        s = s.query('multi_match', query = search['jobtitle'], type = 'cross_fields', fields = ['title', 'summary'], operator = 'and')

    # job description
    if search.has_key('description') or search.has_key('jobtitle'):
        summary = ""
        if search.has_key('jobtitle'):
            summary += search["jobtitle"]
            if search.has_key('description'):
                summary += " " + search['description']
        else:
            summary = search['description']
        s = s.query('match', summary = summary)

    # company
    if search.has_key('company'):
        s = s.query('match', company=search['company'])

    # location
    if search.has_key('state'):
        s = s.query('match_phrase', state = search['state'])
    if search.has_key('city'):
        s = s.query('match', city = search['city'])

    # jobtype
    if search.has_key('type'):
        s = s.query('match', jobtype=search['type'])

    # salary
    if search.has_key('salary'):
        search['salary'] = int(search['salary'])
        s = s.query('range', salary = {'gte': search['salary']})

    # date
    if search.has_key('date'):
        days = re.findall(r"(\d+)", search['date'])[0]
        days = int(days)
        today = datetime.datetime.now().toordinal()
        s = s.query('range', date = {'gte': today - days})

    pp = pprint.PrettyPrinter(depth = 6)
    pp.pprint(s.to_dict())

    if search['sort_by_date']:
        s = s[0:3000]
        response = s.execute()
        resultlist = []
        print response.hits.total
        for hit in response.hits:
            result = {}
            result['id'] = hit.meta.id
            result['score'] = hit.meta.score
            result['title'] = hit['title']
            result['summary'] = hit['summary'][:300]
            result['url'] = 'www.indeed.com' + hit['url']
            result['company'] = hit['company']
            result['location'] = hit['location']
            result['postingdate'] = str(datetime.datetime.fromordinal(hit['date']))
            resultlist.append(result)
        sortedresult = sorted(resultlist, key=lambda d : d['postingdate'], reverse = 1)
        params = {}
        params['joblist'] = sortedresult[search['offset']: search['offset']+10]
        params['hitsnum'] = response.hits.total
        return params
    else:
        s = s[search['offset']: search['offset']+10]
        response = s.execute()

        resultlist = []
        print response.hits.total
        for hit in response.hits:
            result = {}
            result['id'] = hit.meta.id
            result['score'] = hit.meta.score
            result['title'] = hit['title']
            result['summary'] = hit['summary'][:200]
            result['url'] = 'www.indeed.com' + hit['url']
            result['company'] = hit['company']
            result['location'] = hit['location']
            result['postingdate'] = str(datetime.datetime.fromordinal(hit['date']))
            resultlist.append(result)

        params = {}
        params['joblist'] = resultlist
        params['hitsnum'] = response.hits.total
        return params


# search for the jobs posted by the company
def companySearch(search):
    s = Search(using=es)
    search['offset'] = int(search['offset'])
    s = s.index('job_index')
    s = s.query('match_phrase', company=search['company'])
    s = s[search['offset']: search['offset'] +10]
    response = s.execute()

    resultlist = []
    print response.hits.total
    for hit in response.hits:
        result = {}
        result['id'] = hit.meta.id
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
def recommendationSearch(search):
    s = Search(using=es)
    s = s.index('job_index')
    search['offset'] = int(search['offset'])

    condition = []
    #location
    if search.has_key('state'):
        qState = Q('match_phrase', state=search['state'])
        condition.append(qState)
    if search.has_key('city'):
        qCity = Q('match', city=search['city'])
        condition.append(qCity)

    # professional & education background
    if search.has_key('pbg') or search.has_key('degree') or search.has_key('major'):
        qBG = Q('multi_match', query=search['pbg'] + ' ' + str(search['degree']) + " " + str(search['major']), type='cross_fields', fields=['title', 'summary'])
        condition.append(qBG)

    # jobtype
    if search.has_key('type'):
        qType = Q('match', jobtype=search['type'])
        condition.append(qType)

    # salary
    if search.has_key('salary'):
        search['salary'] = int(search['salary'])
        qSalary = Q('range', salary={'gte': search['salary']})
        condition.append(qSalary)

    q = Q('bool', should = condition, minimum_should_match = 1)
    s = s.query(q)

    s = s[search['offset'] : search['offset'] + 10]
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint(s.to_dict())
    response = s.execute()

    resultlist = []
    print response.hits.total
    for hit in response.hits:
        result = {}
        result['id'] = hit.meta.id
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
    job['id'] = id
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