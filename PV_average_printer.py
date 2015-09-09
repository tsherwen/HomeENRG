import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from PV_read_tools import *
import  numpy  as np
import sys

try:
    wd = sys.argv[1]
except:
    wd = './'#'<insert_default_directory_here>'
print wd

# Get data
data  = daily_total_read(wd)
dates, day_kwh, labels, y_av, y_av_II, y_av_III , win_, win_II, win_III  = data

# Select data
_15_day = y_av_III[win_III:-win_III]
_10_day = y_av_II[win_II:-win_II]
_5_day  = y_av[win_:-win_]
last_d = day_kwh 

# Print data to screen 
prt_str = '{:<25}'*6
print prt_str.format('last day' , '5 day mv. avg.','10 day mv. avg.','15 day mv. avg.', 'total so far', 'max')
print prt_str.format( *[ i[-1]  \
    for i in [ last_d, _5_day, _10_day, _15_day,  \
    [np.sum(day_kwh)], [np.max(day_kwh)] ]    ])
