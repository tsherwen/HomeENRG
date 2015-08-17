import numpy as np
#from scipy.optimize import leastsq
import scipy.optimize as optimize
from pylab import *
from scipy import *
from math import atan2
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
import glob
import time
import pandas as pd
import datetime

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

def daily_total_read(wd=None,fn=None,reader=None, rm_last=False):

    # set file
    if isinstance( fn, type(None) ):
        fn = wd+'getDailyTotals_all.csv'
    else:
        fn = wd + fn

    # read csv file
    df = pd.read_csv( fn, 'r' , delimiter=',')
    titles = df.columns
    df.index = pd.to_datetime(df['Date'])
    print df.index

    # get moving averages on a 5, 10, 15 scale
    day_kwh = df[' Generated (kW h)'].values
    y_av     =  movingaverage(day_kwh, 5)
    y_av_II  = movingaverage(day_kwh, 10)
    y_av_III = movingaverage(day_kwh, 15)
    labels = [ num2month(i.month) for i in df.index ]

#    if (rm_last):
#        dates, day_kwh, y_av, y_av_II, y_av_III  = [ i[:-1]for i in [dates, day_kwh, y_av, y_av_II, y_av_III  ] ]
#    return [np.array(i) for i in df.index.values, day_kwh, labels, y_av, y_av_II, y_av_III , 5,10, 15  ]
    return df.index.values, day_kwh, labels, y_av, y_av_II, y_av_III , 5,10, 15 #win_, win_II, win_III 

def num2month(input, reverse=False):

    d={
        1: 'Jan',
         2: 'Feb',
         3: 'Mar',
         4: 'Apr',
         5: 'May',
         6: 'Jun',
         7: 'Jul',
         8: 'Aug',
         9: 'Sep',
         10: 'Oct',
         11: 'Nov',
         12: 'Dec'
    }

    if reverse:
        d= {
        'Jan' : 1,
        'Feb' : 2,
        'Mar' : 3,
        'Apr' : 4,
        'May' : 5,
        'Jun' : 6,
        'Jul' : 7,
        'Aug' : 8,
        'Sep' : 9, 
        'Oct' : 10,
        'Nov' : 11,
        'Dec' : 12 
        }

    return d[input]

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
    data_p = np.concatenate( data_p, axis = 1 )
    return data_p, titles

def daily_detail_read(wd=None, reader=None):
    if (reader == None):
        files =  glob.glob(wd+'getDailyDetails_*')
    data=[]                                                                                                                                              
    for file in files:
        reader = open(file)
        print file
        for row in reader:
            data.append( np.array([ item.split(',') for item in row.splitlines()] )[0][:, np.newaxis] )    
    data = np.concatenate(data, axis=1)
    data, titles  = remove_titles(data)
    dates = data[0,:]
    min_15_kwh = data[1,:] 
    dates, labels = time_2_num_and_labels(dates)
    return dates, min_15_kwh, titles, labels

def fit_sine(data, t):
    guess_a, guess_b, guess_c = np.mean(data), 3*np.std(data)/(2**0.5), 0
    data_first_guess = guess_b*np.sin(t+guess_c) + guess_a
    optimize_func = lambda x: x[0]*np.sin(t+x[2]) + x[1] - data
    est_a, est_b, est_c = leastsq(optimize_func, [guess_a, guess_b, guess_c])[0]
    print  est_a, est_b, est_c 
    data_fit = est_a*np.sin(t+est_c) + est_b
    return data_fit, data_first_guess

def fitSine(tList,yList,freq):
   '''
       freq in Hz
       tList in sec
   returns
       phase in degrees
   '''
   b = matrix(yList).T
   rows = [ [sin(freq*2*pi*t), cos(freq*2*pi*t), 1] for t in tList]
   A = matrix(rows)
   (w,residuals,rank,sing_vals) = lstsq(A,b)
   phase = atan2(w[1,0],w[0,0])*180/pi
   amplitude = norm([w[0,0],w[1,0]],2)
   bias = w[2,0]
   return (phase,amplitude,bias)
