from queryBuilder import generalSearch, companySearch, recommendationSearch

#resultlist = generalSearch('Software Developer Seattle', '', 'NC', 'Raleigh-Durham', 'Amazon', 'full-time', 0, '100', 0)
#resultlist = companySearch('Amazon', 0)

resultlist = recommendationSearch('New York', '', 'java developer', 'Master', 'Computer Science', 6000, 'full-time', 0)

print resultlist
print len(resultlist)