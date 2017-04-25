from index import Job
import pprint

search = Job.search()
s = search.query('match', zipcode="02210")
response = s.execute()
# get the number of results
result_num = response.hits.total
print result_num

for hit in response.hits:
    print hit.location