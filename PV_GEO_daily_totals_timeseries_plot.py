import matplotlib.pyplot as plt
from PV_read_tools import *

# ---  Output settings for direct main call
DEBUG=False
VERBOSE=False

def main( rm_last=False, curve_fit=False, f_size=20, \
    data_variable=r' Generated (kW h)', use_GEO_data=True,  \
    verbose=False, debug=False ):
    """ Plot up data from GEO PV output monitor 
    NOTES:
        - A sinosodal curve is fitted if "curve_fit" == True
        - The last days input can be removed with "rm_last"
    """

#    use_GEO_data=False

    # Get data
    if use_GEO_data:
        df = get_PV_daily_data_from_GEO( \
            data_variable=data_variable, return_DataFrame=True )
    else:
        df = get_PV_daily_data_from_EmonPi( \
            data_variable=data_variable, return_DataFrame=True )

    # Setup figure, and Plot up
    fig = plt.figure(figsize=(20,10), dpi=80, facecolor='w', edgecolor='k')
    ax1 = fig.add_subplot(111)    
    plt.plot( df.index, df[data_variable], marker='x', color='b', alpha=0.3)

    # Add moving averages
    add_moving_averages( dates=df.index, data=df[data_variable] )

    # Add curve fit?
    if curve_fit:
        add_curve_fit( dates=df.index, data=df[data_variable] )

    # Beautify plot
    beatify_plot( dates=df.index, data=df[data_variable], f_size=f_size )

    # Get averages
    plt.show()
    
    
def add_moving_averages( data=None, dates=None ):

    # Local variables
    mv_avgs = [ 5, 10, 15 ] 
    titles = ['5 day moving avg.', '10 day moving avg.', '15 day moving avg.' ]
    color_list= [ 'green', 'orange', 'r']

    # Loop 
    for n, size in enumerate( mv_avgs ):
        avg = movingaverage( data, size)

        plt.plot( dates[ mv_avgs[n]:-mv_avgs[n] ], avg[ mv_avgs[n]:-mv_avgs[n]], 
            color_list[n], label =titles[n], ls='dashed'   )

def add_curve_fit( dates=None, data=None ):

    phase = 0#65
    amplitude = 20#3
    bias = -10 #-0.3
    frequency = 1 #365#4
    tList =  dates
    yList   = data
    (phaseEst,amplitudeEst,biasEst) = fitSine( dates, data, frequency)
    print ('Phase estimate = %f, Amplitude estimate = %f, Bias estimate = %f'
           % (phaseEst,amplitudeEst,biasEst))

    yEst = amplitudeEst*sin(tList*frequency*2*pi+phaseEst*pi/180.0)+biasEst
    plot(tList,yList,'b')
    plot(tList,yEst,'-g')
    xlabel('seconds')
    legend(['True value','Measured values','Estimated value'])
    grid(True)

def beatify_plot( data=None, dates=None, f_size=20 ):

    # Beautify plot
#    plt.xticks( dates[2::31], labels[2::31], rotation=90, fontsize=f_size )
#    plt.xlim( dates[0]-1, dates[-1]+1 )
    plt.ylabel( 'Daily kWh output', fontsize=f_size )
    plt.legend( loc='upper left', fontsize=f_size )
    plt.title( 'PV output, York (3.6 kW SunPower + GOODWE inverter)', \
        fontsize=f_size )

if __name__ == "__main__":
    main( verbose=VERBOSE, debug=DEBUG )

