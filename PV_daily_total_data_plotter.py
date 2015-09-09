import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from PV_read_tools import *
import sys

# ---  Settings
rm_last = False#True#False
curve_fit = False # add sinododal fit
f_size = 20

# Get data directory
try:
    wd = sys.argv[1]
except:
    wd ='./'#'<insert_default_directory_here>'
print wd

# Extract data
dates, day_kwh, labels, y_av, y_av_II, y_av_III , win_, win_II, win_III   = daily_total_read(wd, rm_last=rm_last) 

# Setup figure
fig = plt.figure(figsize=(20,10), dpi=80, facecolor='w', edgecolor='k')
ax1 = fig.add_subplot(111)

# Plot data
plt.plot(dates, day_kwh, marker='x', color='b', alpha=0.3)

# Plott up moving averages <= upgrade this to use pandas. 
plt.plot(dates[win_:-win_], y_av[win_:-win_], color='green', \
    ls='dashed', label = '5 day moving avg.' )
plt.plot(dates[win_II:-win_II], y_av_II[win_II:-win_II], color='orange', \
    ls ='dashed' , label = '10 day moving avg.' )
plt.plot(dates[win_III:-win_III], y_av_III[win_III:-win_III], color='r', \
    ls ='dashed' , label = '15 day moving avg.')

if curve_fit:
    phase = 0#65
    amplitude = 20#3
    bias = -10 #-0.3
    frequency = 1 #365#4
    tList =  dates
    yList   = day_kwh
    (phaseEst,amplitudeEst,biasEst) = fitSine( dates, day_kwh, frequency)
    print ('Phase estimate = %f, Amplitude estimate = %f, Bias estimate = %f'
           % (phaseEst,amplitudeEst,biasEst))

    yEst = amplitudeEst*sin(tList*frequency*2*pi+phaseEst*pi/180.0)+biasEst
    plot(tList,yList,'b')
    plot(tList,yEst,'-g')
    xlabel('seconds')
    legend(['True value','Measured values','Estimated value'])
    grid(True)

# Beautify plot
plt.xticks( dates[2::31], labels[2::31], rotation=90, fontsize=f_size )
plt.xlim( dates[0]-1, dates[-1]+1 )
plt.ylabel( 'Daily kWh output', fontsize=f_size )
plt.legend( loc='upper left', fontsize=f_size )
plt.title( 'PV output, York (3.6 kW SunPower + GOODWE inverter)', \
    fontsize=f_size )
plt.show()
