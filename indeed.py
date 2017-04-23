import datetime
import requests
from lxml import html
import re
import unirest
import string


base_url = "http://www.indeed.com"

def build_url(url, *filters):
    return url + ''.join(["&" + param + "=" + val for param,val in filters])

def build_search_url(keywords, location):
    query = "/jobs?"
    keyword_filter = "q", keywords
    location_filter = "l", location
    date_filter = 'fromage', 'last' # only get the latest postings
    return build_url(base_url + query, keyword_filter, location_filter, date_filter)


def build_detail(job_url):
    summary = ""
    try:
        request = requests.get(base_url + job_url)
        url = str(request.url)
        if url.find("www.indeed.com") > 0:
            tree = html.fromstring(request.text)
            node = tree.xpath('.//span[contains(@class,"summary")]//text()')
            summary = '\n'.join(node)
            print summary
    except Exception,e:
        print Exception,":",e
    return summary



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

def parse_job(job):
    #print job.xpath('.//span//text()')
    job_title = parse_xpath(job.xpath('.//h2[contains(@class,"jobtitle")]/a/@title'))
    job_url = parse_xpath(job.xpath('.//h2[contains(@class,"jobtitle")]/a/@href'))
    job_date = parse_date(parse_xpath(job.xpath('.//span[contains(@class,"date")]/text()')))
    company = parse_xpath(job.xpath('.//span[contains(@class,"company")]//text()'))
    company = company.replace('\\n', '')
    company = re.sub("[\.\!\/_,$%^*(+\"\'\[\]]+", "", company)
    company = company.strip(' ')
    location = parse_xpath(job.xpath('.//span[contains(@class,"location")]//text()'))
    job_summary = build_detail(job_url)

    if(len(job_summary) < 10):
        return {}
    return {'job_url':job_url, 'job_title':job_title, 'company':company,
            'location':location, 'job_date':str(job_date), 'job_summary': job_summary}

def get_jobs(keywords, location, max_pages=1):

    tree = html.fromstring(requests.get(build_search_url(keywords, location)).text)

    jobs = {}
    id = 1
    for i in range(max_pages):
        jobs_divs = tree.xpath('//div[contains(@itemtype,"JobPosting")]')
        for job in jobs_divs:
            p_j = parse_job(job)
            if p_j != {}:
                jobs[str(id)] = p_j
                id = id + 1
                if id > 100:
                    break

        if id > 100:
            break
        next_page = tree.xpath('//div[contains(@class,"pagination")]//span[contains(text(),"Next")]/../../@href')
        if len(next_page) == 0:
            print "Last page: ", i + 1
            break
        else: next_page = base_url + next_page[0]

        tree = html.fromstring(requests.get(next_page).text)

    return jobs
