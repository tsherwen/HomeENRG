import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from PV_read_tools import *
import sys

# Where is the data?
try:
    wd = sys.argv[1]
except:
    wd ='<insert_default_directory_here>'
print wd

# What to plot?
daily_totals, daily_breakdown = True, False

# Get data
if (daily_breakdown):
    dates_I, min_15_kwh, titles, labels = daily_detail_read(wd)
    print titles , len(min_15_kwh), len(dates_I) , len(dates_I)/4/24
if (daily_totals ):
    dates, day_kwh, labels, y_av, y_av_II, y_av_III , win_, win_II, win_III   = daily_total_read(wd)
    print len(day_kwh),len(dates)

# Plot data
fig = plt.figure(figsize=(20,10), dpi=80, facecolor='w', edgecolor='k')
ax1 = fig.add_subplot(111)

if (daily_totals):
    plt.plot(dates_I, min_15_kwh, color='purple')
    plt.plot(dates, day_kwh, marker='x', color='b', alpha=0.3)
    plt.plot(dates[win_:-win_], y_av[win_:-win_], color='green', ls='dashed', label = '5 day moving avg.' )
    plt.plot(dates[win_II:-win_II], y_av_II[win_II:-win_II], color='orange' ,ls ='dashed' , label = '10 day moving avg.' )
    plt.plot(dates[win_III:-win_III], y_av_III[win_III:-win_III], color='r' ,ls ='dashed' , label = '15 day moving avg.' )
    plt.xticks(dates[2::31], labels[2::31])
    plt.xlim(dates[0]-1, dates[-1]+1 )
    plt.ylabel( 'Daily kWh output' )
    plt.legend(loc='upper right',prop=font_manager.FontProperties(size=20))

if (daily_breakdown): # plot on second y
    ax2 = ax1.twinx()
    ax2.plot(dates_I, min_15_kwh, color='purple')

plt.rcParams.update({'font.size': 20})
plt.title('PV output, York (3.6 kW SunPower )')

plt.show()
