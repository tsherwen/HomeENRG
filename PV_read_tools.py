import numpy as np
import matplotlib as mpl
import datetime
import time

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

