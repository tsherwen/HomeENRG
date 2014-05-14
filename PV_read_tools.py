import numpy as np
import matplotlib as mpl
#from scipy.optimize import leastsq
import scipy.optimize as optimize
from pylab import *
from scipy import *
from math import atan2
import matplotlib.pyplot as plt
import datetime
import glob
import time

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

def daily_total_read(wd=None,fn=None,reader=None, rm_last=False):
    if (reader == None ):
        if ( fn == None ):
            reader = open(wd+'getDailyTotals_all.csv', 'rb')
        else:
            reader = open(wd+fn, 'rb')
    data=[]
    for row in reader:       
        data.append( np.array([ item.split(',') for item in row.splitlines()] )[0][:, np.newaxis] )
    data = np.concatenate(data, axis=1)
    titles, dates, day_kwh = data[:,0], data[0,1:] , data[1,1:]
    dates, labels  = time_2_num_and_labels(dates)
    day_kwh = np.array(day_kwh,    np.float )
    x,    y                  = dates, day_kwh
    win_, win_II, win_III    = 5,  10, 15   
    y_av, y_av_II, y_av_III  =  movingaverage(y, win_), movingaverage(y, win_II), movingaverage(y, win_III)
    if (rm_last):
        dates, day_kwh, y_av, y_av_II, y_av_III  = [ i[:-1]for i in [dates, day_kwh, y_av, y_av_II, y_av_III  ] ]
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
