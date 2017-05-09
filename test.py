from queryBuilder import generalSearch, companySearch, recommendationSearch, jobdetail

resultlist = generalSearch('', '', 'NY', '', '', 'full-time', 0, '100', 0, True)
#resultlist = companySearch('Amazon', 0)

#resultlist = recommendationSearch('New York', '', 'java developer', 'Master', 'Computer Science', 6000, 'full-time', 0)

#resultlist = jobdetail('AVvujdTUgCRzIHTOpXr-')
for result in resultlist:
    print result['postingdate'] + ' '+ str(result['score'])

resultlist = generalSearch('', '', 'NY', '', '', 'full-time', 0, '100', 10, True)
for result in resultlist:
    print result['postingdate'] + ' '+ str(result['score'])
print len(resultlist)