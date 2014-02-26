import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from PV_read_tools import *

wd ='/Users/Tomas/Dropbox/Personal/Ele_and_Tomas_s_Shared_Folder/PV_panels_dat_files/'

dates, day_kwh, labels, y_av, y_av_II, y_av_III , win_, win_II, win_III   = daily_total_read(wd)


_15_day = y_av_III[win_III:-win_III]
_10_day = y_av_II[win_II:-win_II]
_5_day  = y_av[win_:-win_]
last_d = day_kwh 

prt_str = '{:<25}'*4
print prt_str.format('last day' , '5 day mv. avg.','10 day mv. avg.','15 day mv. avg.')
print prt_str.format( *[ i[-1] for i in [ last_d, _5_day, _10_day, _15_day ] ])
