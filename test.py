from queryBuilder import generalSearch, companySearch, recommendationSearch, jobdetail

search = {}
search['jobtitle'] = 'software'
search['description'] = 'java'
search['state'] = 'MA'
search['jobtype'] = 'Full-time'
search['salary'] = 0
search['date'] = 'Within 3 days'

resultlist = generalSearch(search, 0, True)
#resultlist = companySearch('Amazon', 0)

#resultlist = recommendationSearch('New York', '', 'java developer', 'Master', 'Computer Science', 6000, 'full-time', 0)

#resultlist = jobdetail('AVvujdTUgCRzIHTOpXr-')
print resultlist
for result in resultlist:
    print result['postingdate'] + ' '+ str(result['score'])

# resultlist = generalSearch('', '', 'NY', '', '', 'Full-time', 0, '100', 10, True)
# for result in resultlist:
#     print result['postingdate'] + ' '+ str(result['score'])
print len(resultlist)