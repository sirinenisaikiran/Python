from datetime import datetime, timedelta, date

#make a 2 day limit
datelimit = datetime.today() - timedelta(days=2)
print(datelimit)

yourlist  = ['2018-06-13T13:26:05', '2018-06-19T13:26:05', '2018-08-14T13:26:05', '2020-05-21T00:26:05']

for i in yourlist:
    j = datetime.strptime(i,"%Y-%m-%dT%H:%M:%S")
    if j < datelimit:
        print (j.strftime('%Y-%m-%dT%H:%M:%S'))
        

# for i in yourlist:
    # j = datetime.strptime(i,  "%m/%d/%y")
    # if j < datelimit:
        # print (j.strftime('%d/%m/%Y'))