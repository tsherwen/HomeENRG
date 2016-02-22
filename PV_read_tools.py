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
    """ return moving average for given interval + window size """
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

def get_PV_daily_data_from_GEO( fn=None, data_variable=r' Generated (kW h)', \
        return_DataFrame=False ):
    """ Extract PV data from CSV using pandas read_csv """

    # Get data
    try:
        wd = sys.argv[1]
    except:
        wd ='./Geo/'#'<insert_default_directory_here>'
    print wd

    # Set file
    if isinstance( fn, type(None) ):
        fn = wd+'getDailyTotals_all.csv'
    else:
        fn = wd + fn

    # read csv file
    df = pd.read_csv( fn, 'r' , delimiter=',')
    df.index = pd.to_datetime( df['Date'],  dayfirst=True)

    if return_DataFrame:
        return  df
    else:
        return  df[data_variable], df.index


def get_PV_daily_data_from_EmonPi( feed='PV', units='(kWh day$^{-1}$)' ,  \
        data_variable=r' Generated (kW h)',  reverse_accumaltion=False, \
        return_DataFrame=False, verbose=False, debug=False,  ):
    
    # What is the feed number?
    feed_ID = get_feed_ID( feed=feed, units=units )
    
    # Extract all files?
    df = get_Emon_feed_df( feed_ID, data_variable=data_variable )

    # Reverse accumulation. 
    if reverse_accumaltion:
        df['prev_val'] =  np.concatenate( (np.array( [0.0 ] ), \
            df[ data_variable ].values[:-1]),  axis=0) 
        # Subtract previous value
        df[ data_variable ] = df[ data_variable ] - df['prev_val']
        df = df.drop('prev_val', 1)

    if return_DataFrame:
        return  df
    else:
        return  df.values, df.index
    
def get_Emon_feed_df( feed_ID, data_variable=r' Generated (kW h)', ):

    # Get Directory
    try:
        wd = sys.argv[1]
    except:
        wd ='./EmonPi/PV/'#'<insert_default_directory_here>'
    print wd

    files  = glob.glob( wd + '*{}*'.format( feed_ID ) )
    print files
    # process all files.
    # Kludge - Just use first one for now... 
    df = pd.read_csv( files[-1], 'r' , delimiter=',', header=None)
    df.columns = ['dates', data_variable ]  
    df.index = pd.to_datetime( df['dates'], unit='s' )
    df = df.drop('dates', 1)
    print df
    
    return df

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
        labels = [ time.strftime('%b', i) \
            for i in  [time.strptime(date, '%Y-%m-%d') for date in dates]  ]
    except:
        labels = [ time.strftime('%b', i) \
            for i in [time.strptime(date, '%Y-%m-%d %H:%M') for date in dates] ]

    dates = np.array( [mpl.dates.datestr2num(date) for date in dates] )
    return dates, labels 


def fit_sine(data, t):
    """ Fit Sinusoidal to curve """
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
   
   
   
def get_feed_ID( feed='PV', units='(kWh day$^{-1}$)' ):
    """ Dictionary of feed ID numbers """

    d = {
    'GRID': {
    '(kWh day$^{-1}$)':79875, \
    '(Wh)' : 79881, 
    '(W)' : 79815 }, 
    'PV': {
    '(kWh day$^{-1}$)':79879, 
    '(Wh)': 79880, 
    '(W)': 79814}
    }[ feed ]

    return d[ units ]
