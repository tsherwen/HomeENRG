import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from PV_read_tools import *
from scipy import *
#from scipy import gplt
from scipy import fftpack

# get data
wd ='/Users/Tomas/Dropbox/Personal/Ele_and_Tomas_s_Shared_Folder/PV_panels_dat_files/'
fn = 'getDailyTotals_all_II_14_03_09.csv'
dates, day_kwh, labels, y_av, y_av_II, y_av_III , win_, win_II, win_III   = daily_total_read(wd, fn)

# plot
fig = plt.figure(figsize=(20,10), dpi=80, facecolor='w', edgecolor='k')
ax1 = fig.add_subplot(111)
#plt.plot(dates, day_kwh, marker='x', color='b', alpha=0.3)
#plt.plot(dates[win_:-win_], y_av[win_:-win_], color='green', ls='dashed', label = '5 day moving avg.' )
#plt.plot(dates[win_II:-win_II], y_av_II[win_II:-win_II], color='orange' ,ls ='dashed' , label = '10 day moving avg.' )
#plt.plot(dates[win_III:-win_III], y_av_III[win_III:-win_III], color='r' ,ls ='dashed' , label = '15 day moving avg.' )
#plt.xticks(dates[2::31], labels[2::31])
#plt.xlim(dates[0]-1, dates[-1]+1 )

curve_fit = False # add sinododal fit
if (curve_fit):
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
data_analysis = True
if ( data_analysis ):
#from scipy import gplt
#from scipy import fftpack
    year=dates
    wolfer=day_kwh

    Y=fft(wolfer)

    n=len(Y)
    power = abs(Y[1:(n/2)])**2
    nyquist=1./2
    freq=array(range(n/2))/(n/2.0)*nyquist

    period=1./freq
    plt.plot(period[1:len(period)], power)#,'title "Meas" with linespoints')
#    plt.xaxis((0,40))
    plt.xlabel('Period [year]')
    plt.ylabel('|FFT|**2')
    plt.grid("off")
    plt.show()
#    plt.output('sunspot_period.png','png medium transparent picsize 600 400')

plt.ylabel( 'Daily kWh output' )
plt.legend(loc='upper right',prop=font_manager.FontProperties(size=20))
plt.rcParams.update({'font.size': 20})
plt.title('PV output, York (3.6 kW SunPower + GOODWE inverter)')
#plt.show()
