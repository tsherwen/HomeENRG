import numpy as np
import matplotlib as mpl
import datetime
import glob
import time

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

def daily_total_read(wd=None,reader=None):
    if (reader == None ):
        reader = open(wd+'getDailyTotals_all.csv', 'rb')
    data=[]
    for row in reader:       
#        print row
        data.append( np.array([ item.split(',') for item in row.splitlines()] )[0][:, np.newaxis] )
    data = np.concatenate(data, axis=1)
    titles, dates, day_kwh = data[:,0], data[0,1:] , data[1,1:]
    dates, labels  = time_2_num_and_labels(dates)
    day_kwh = np.array(day_kwh,    np.float )
    x,    y                  = dates, day_kwh
    win_, win_II, win_III    = 5,  10, 15   
    y_av, y_av_II, y_av_III  =  movingaverage(y, win_), movingaverage(y, win_II), movingaverage(y, win_III)
    return dates, day_kwh, labels, y_av, y_av_II, y_av_III , win_, win_II, win_III 

def time_2_num_and_labels(dates):
    try:
        labels = [ time.strftime('%b', i) for i in  [time.strptime(date, '%Y-%m-%d') for date in dates]  ]
    except:
        labels = [ time.strftime('%b', i) for i in  [time.strptime(date, '%Y-%m-%d %H:%M') for date in dates]  ]

    dates = np.array( [mpl.dates.datestr2num(date) for date in dates] )
    return dates, labels 

def remove_titles(data):
    data_p = []
    titles = data[:,0]
    for i in range( len( data[0,:] ) ):
        if data[0,i] == 'Date':
            print data[:,i]
        else :
            data_p.append( data[:,i][:,np.newaxis] )
#    print len( data ), data.shape, titles
    data_p = np.concatenate( data_p, axis = 1 )
    return data_p, titles

def daily_detail_read(wd=None,reader=None):
    if (reader == None):
        files =  glob.glob(wd+'getDailyDetails_*')
    data=[]                                                                                                                                              
    for file in files:
        reader = open(file)
        print file
        for row in reader:
#            print row
            data.append( np.array([ item.split(',') for item in row.splitlines()] )[0][:, np.newaxis] )    
#    print len(data), len(data[0])
    data = np.concatenate(data, axis=1)
#    print data.shape
    data, titles  = remove_titles(data)
    dates = data[0,:]
#    print dates
    min_15_kwh = data[1,:] 
    dates, labels = time_2_num_and_labels(dates)
    return dates, min_15_kwh, titles, labels
