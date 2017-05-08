import json
import re
import time

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import DocType, Text, Float, Date
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import tokenizer, analyzer, token_filter
from dateutil import parser


# connect to local host server
connections.create_connection(hosts=['127.0.0.1'])

# establish elasticsearch
es = Elasticsearch()

# define analyzers
name_synonym = token_filter('state_synonym',
                            type='synonym',
                            synonyms_path="state_syn.txt")
summary_analyzer = analyzer('custom',
                            tokenizer='standard',
                            filter=['lowercase', 'stop', 'snowball'])
lowerCase_analyzer = analyzer('custom',
                              tokenizer='standard',
                              filter=['lowercase'])

# define Movie class mapping
class Job(DocType):
    title = Text(analyzer = lowerCase_analyzer)
    company = Text(analyzer = lowerCase_analyzer)
    summary = Text(analyzer = summary_analyzer)
    jobtype = Text()
    location = Text()
    state = Text()
    city = Text()
    zipcode = Text()
    salary = Float()
    date = Date()
    
    class Meta:
        index = 'job_index'
        doc_type = 'job'

    def save(self, *args, **kwargs):
        return super(Job, self).save(*args, **kwargs)

# Extract state info from location
def stateOf(location):
    if "," in location:
        state_location = location.split(",")[1]
        state = re.findall(r"[a-zA-z]+", state_location)
        if state:
            return state[0]
    return ""
    
# Extract city info from location
def cityOf(location):
    if "," in location: return location.split(",")[0]
    else: return location
    
# Extract zip info from location
def zipOf(location):
    if "," in location:
        state_location = location.split(",")[1]
        zipcode = re.findall(r"(\d+)", state_location)
        if zipcode:
            return zipcode[0]
    return ""
    
# store movie data into elastic search structure
def prepareIndex():
    # If outdate version index exists delete the old one and create new
    if es.indices.exists(index='job_index'):
        es.indices.delete(index='job_index')   
    es.indices.create(index = 'job_index')
        
    # initialize mapping
    es.indices.close(index='job_index') # For enable analyzer modify close index firstly
    Job.init()
    es.indices.open(index='job_index')
    
    # open json file and store data into elastic search
    filename = raw_input("Please input corpus' name(without extension name): ")
    with open(filename + '.json') as data_file:
        jobs = json.load(data_file)
        
    # Bulk Load
    actions = [
        {
            "_index": "job_index",
            "_type": "job",
            "_id": jid,
            "title":jobs[jid]['title'],
            "company":jobs[jid]['company'],
            "summary":jobs[jid]['summary'],
            "jobtype":jobs[jid]['type'].lstrip(), # remove the beginning spaces in job type
            "location":jobs[jid]['location'],
            "state":stateOf(jobs[jid]['location']),
            "city":cityOf(jobs[jid]['location']),
            "zipcode":zipOf(jobs[jid]['location']),
            "salary":float(jobs[jid]['salary']),
            "date":parser.parse(jobs[jid]['date'])
        }
        for jid in jobs
    ]
    helpers.bulk(es, actions) 
    
def main():
    start_time = time.time()
    prepareIndex()
    print("--- ElasticSearch Prepared. Running time is %s seconds ---" % (time.time() - start_time))
        
if __name__ == '__main__':
    main()   
