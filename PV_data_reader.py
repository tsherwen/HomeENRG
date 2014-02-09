import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import datetime
import time

file_n ='/Users/Tomas/Dropbox/Personal/Ele_and_Tomas_s_Shared_Folder/PV_panels_dat_files/getDailyTotals_all.csv'

reader = open(file_n, 'rb')

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

def daily_total_read(reader):
    data=[]
    for row in reader:       
        print row
        data.append( np.array([ item.split(',') for item in row.splitlines()] )[0][:, np.newaxis] )
    data = np.concatenate(data, axis=1)
    titles, dates, day_kwh = data[:,0], data[0,1:] , data[1,1:]
    labels = [ time.strftime('%b', i) for i in  [time.strptime(date, '%Y-%m-%d') for date in dates]  ]
    dates = np.array( [mpl.dates.datestr2num(date) for date in dates] )#, np.float )
    day_kwh = np.array(day_kwh,    np.float )
    x,    y                  = dates, day_kwh
    win_, win_II, win_III    = 5,  10, 15   
    y_av, y_av_II, y_av_III  =  movingaverage(y, win_), movingaverage(y, win_II), movingaverage(y, win_III)

    return dates, day_kwh, labels, y_av, y_av_II, y_av_III , win_, win_II, win_III 

def 15_min_PV_data_read(reader):
    




dates, day_kwh, labels, y_av, y_av_II, y_av_III , win_, win_II, win_III   = daily_total_read(reader)

fig = plt.figure(figsize=(20,10), dpi=80, facecolor='w', edgecolor='k')
ax1 = fig.add_subplot(111)
plt.plot(dates, day_kwh, marker='x', color='b', alpha=0.3)
plt.plot(dates[win_:-win_], y_av[win_:-win_], color='green', ls='dashed', label = '5 day moving avg.' )
plt.plot(dates[win_II:-win_II], y_av_II[win_II:-win_II], color='orange' ,ls ='dashed' , label = '10 day moving avg.' )
plt.plot(dates[win_III:-win_III], y_av_III[win_III:-win_III], color='r' ,ls ='dashed' , label = '15 day moving avg.' )
plt.xticks(dates[2::31], labels[2::31])
plt.xlim(dates[0]-1, dates[-1]+1 )
plt.ylabel( 'Daily kWh output' )
plt.legend(loc='upper right',prop=font_manager.FontProperties(size=20))
plt.rcParams.update({'font.size': 20})
plt.title('PV output, York (3.6 kW SunPower )')

plt.show()
