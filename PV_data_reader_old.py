#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime

#file_n='/Users/Tomas/Dropbox/Personal/Ele_and_Tomas_s_Shared_Folder/PV_panels_dat_files/getDailyTotals_all.csv'
file_n='/Users/Tomas/Dropbox/Personal/Ele_and_Tomas_s_Shared_Folder/PV_panels_dat_files/getDailyTotals_all_II.csv'
reader= open(file_n, 'rb')
read_data=True

if (read_data):
    for row in reader:       
        print row
        all= row.splitlines()#.split(',')
        print all
    all = [  item.split(',') for item in all]

    print all
    
    titles= all[0][:]
    for i in range(len(all)):
        try:
            dates.append(all[i][0])
        except:
            dates=[]# all[i][0] ]
    print dates
    #
    for i in range(len(all)):
        try:
            day_kwh.append(all[i][1])
        except:
            day_kwh=[]# all[i][1] ]

print 'titles', titles
print 'dates', dates
print 'day_kwh', day_kwh

#dates = [ date.split('/') for date in dates ]
#print dates
#dates = [mpl.dates.date2num(date) for date in dates] 
#print dates
#dates = [ datetime.date(date) for date in dates ]

dates =[mpl.dates.datestr2num(date) for date in dates]

dates= sorted(dates)

print 'dates', len(dates), dates
print 'day_kwh', len( day_kwh), day_kwh

plt.plot(dates, day_kwh)
#plt.show()
