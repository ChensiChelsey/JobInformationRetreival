from index import Job
from elasticsearch_dsl import Search, Q
import re
import datetime

# input: jobtitle, description, state, city, jobtype, salary, date
# index:
def search(jobtitle, description, state, city, jobtype, salary, date):
    search = Job.search()
    s = search.query(Q('match_all'))
    if len(jobtitle) != 0 and len(description) != 0:
        s = search.query('multi_match', query = jobtitle + " " + description, type = 'cross_fields', fields=['title', 'summary'], operator = 'and')

    # location
    if len(state) > 0:
        s = s.query('match', state = state)
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

    print s.to_dict()
    response = s.execute()

    resultlist = []
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

