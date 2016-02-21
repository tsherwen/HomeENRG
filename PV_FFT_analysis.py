import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from PV_read_tools import *
from scipy import *
#from scipy import gplt
from scipy import fftpack

# settings
data_analysis = True

# Get data
try:
    wd = sys.argv[1]
except:
    wd ='./'#'<insert_default_directory_here>'
print wd

fn = 'getDailyTotals_all.csv'
dates, day_kwh, labels, y_av, y_av_II, y_av_III , win_, win_II, win_III   = daily_total_read(wd, fn)

# Setup figure
fig = plt.figure(figsize=(20,10), dpi=80, facecolor='w', edgecolor='k')
ax1 = fig.add_subplot(111)

if data_analysis:

    year=dates
    wolfer=day_kwh
    
    Y=fft(wolfer)

    n=len(Y)
    power = abs(Y[1:(n/2)])**2
    nyquist=1./2
    freq=array(range(n/2))/(n/2.0)*nyquist

    period=1./freq
    plt.plot(period[1:len(period)], power)#,'title "Meas" with linespoints')

    plt.xlabel('Period [year]')
    plt.ylabel('|FFT|**2')
    plt.grid("off")
    plt.show()

