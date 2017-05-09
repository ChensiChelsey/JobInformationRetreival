import datetime
import requests
from lxml import html
import re
import unirest
import string
from dateutil import parser

'''
this is a web crawler to download job postings from indeed
'''


base_url = "http://www.indeed.com"


# based on indeeds url rule build url
def build_url(url, *filters):
    return url + ''.join(["&" + param + "=" + val for param,val in filters])

# based on indeeds url rule build valid search url
def build_search_url(keywords, location):
    query = "/jobs?"
    keyword_filter = "q", keywords
    location_filter = "l", location
    date_filter = 'fromage', 'last' # only get the latest postings
    return build_url(base_url + query, keyword_filter, location_filter, date_filter)

# get posting's job summary field
def build_detail(job_url):
    summary = ""
    try:
        request = requests.get(base_url + job_url, timeout = 10)
        url = str(request.url)
        if url.find("www.indeed.com") > 0:
            tree = html.fromstring(request.text)
            node = tree.xpath('.//span[contains(@class,"summary")]//text()')
            summary = '\n'.join(node)
            #print summary
    except Exception,e:
        print Exception,":",e
    return summary


# find desired part in html file
def parse_xpath(xpath, type=unicode, unique=True):
    if len(xpath)== 0:
        #print "No elements found by xpath."
        return ''
    if unique and len(xpath) > 1:
        #print "xpath expected 1 element, but found:", str(xpath)
        return str(xpath)

    if unique:
        return type(xpath[0])
    else:
        return [type(x) for x in xpath]

# get the postings date in desired form
def parse_date(job_date):
    hours = re.match(r"(\d+) hours", job_date)
    days = re.match(r"(\d+) days", job_date)
    if hours:
        hours = int(hours.group(1))
    else:
        hours = 0
    if days:
        days = int(days.group(1))
    else:
        days = 0

    job_date_obj = datetime.datetime.today() - datetime.timedelta(days=days, hours=hours)
    return job_date_obj

# analyze job's summary, extract salary and job-type fields
def parse_job_summary(summary, detail):
    lines = summary.split("\n")
    detail['type'] = ''
    detail['salary'] = 0
    for line in lines:
        if line.find('Job Type') >= 0:
            try:
                detail['type'] = line.split(":")[1]
            except Exception, e:
                print Exception, ":", e
        if line.find('Salary') >= 0:
            try:
                text = line.split(":")[1]
                text = re.sub("[\!\/_,$%^*(+\"\'\[\]]+", "", text)
                number = []
                splited = text.split(" ")
                for word in splited:
                    try:
                        number.append(string.atof(word))
                    except Exception, e:
                        continue
                if len(number) == 1:
                    salary = number[0]
                else:
                    salary = (number[0] + number[1])/2
                if text.find('year') > 0:
                    detail['salary'] = salary
                else:
                    if text.find('day') > 0:
                        detail['salary'] = salary * 250
                    else:
                        if text.find('hour') > 0:
                            detail['salary'] = salary * 8 * 250
            except Exception, e:
                print Exception, ":", e
    return detail

# parse the job's web site to get job's detailed information
def parse_job(job):
    detail = {}
    detail['title'] = parse_xpath(job.xpath('.//h2[contains(@class,"jobtitle")]/a/@title'))
    detail['url'] = parse_xpath(job.xpath('.//h2[contains(@class,"jobtitle")]/a/@href'))
    date = str(parse_date(parse_xpath(job.xpath('.//span[contains(@class,"date")]/text()'))))
    detail['date'] = parser.parse(date)
    company = parse_xpath(job.xpath('.//span[contains(@class,"company")]//text()'))
    company = company.replace('\\n', '')
    company = re.sub("[\.\!\/_,$%^*(+\"\'\[\]]+", "", company)
    detail['company'] = company.strip(' ')
    detail['location'] = parse_xpath(job.xpath('.//span[contains(@class,"location")]//text()'))
    summary = build_detail(detail['url'])
    if (len(summary) < 10):
        return {}
    detail['summary'] = summary
    detail = parse_job_summary(summary, detail)
    return detail

# based on the keyword get job postings
def get_jobs(keywords, location, max_pages=1, id = 0, jobs = {}, starttime = 0):
    try:
        tree = html.fromstring(requests.get(build_search_url(keywords, location), timeout=10).text)
        diff = 0
        for i in range(max_pages):
            jobs_divs = tree.xpath('//div[contains(@class,"result") and contains(@class,"row")]')
            for job in jobs_divs:
                p_j = parse_job(job)
                if p_j != {}:
                    if starttime != 0 and starttime > p_j['date']:
                        dif = starttime - p_j['date']
                        print p_j['date']
                        if dif.total_seconds() > 3600:
                            diff = dif
                            break
                    p_j['date'] = str(p_j['date'])
                    jobs[str(id)] = p_j
                    id = id + 1

            if starttime != 0 and diff != 0:
                break
            next_url = build_search_url(keywords, str(i * 10 + 10))
            next_page = next_url.replace("&l=", "&start=")
            print next_page
            tree = html.fromstring(requests.get(next_page, timeout=10).text)
    except Exception, e:
        print Exception, ":", e

    return id
