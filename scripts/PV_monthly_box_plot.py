import pandas as pd
import matplotlib.pyplot as plt
from PV_read_tools import *

def main():
    """ Plot up data by month as box plots """
    # get daily totals
    dates, data = get_PV_daily_data_from_GEO()

    # plot up as monthly values
    plot_monthly_boxplots( dates, data )


def plot_monthly_boxplots( data, dates, showmeans=True, f_size=20 ):
    """ Plot up PV data by month """

    # Set local variables
    months = range(1, 13)

    # make dataframe
    df = pd.DataFrame( data, index=dates )
    
    # add by month
    def get_month(x):
         return x.month
    df[ 'month'] = df.index.map( get_month ) 
    monthly = [df[ df[ 'month']==i ] for i in months ]

    # Setup plot
    fig = plt.figure(figsize=(14,7), dpi=80, facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111)
    
    # loop months and  plot bocplots
    bp = ax.boxplot( monthly, months, showmeans=showmeans )

    # Beautify
    [ ax.text( months[n], 0.1, 'n = {}'.format(len(monthly[n])), 
            fontsize=f_size*.75) for n, v in enumerate( months )]   

    plt.show()
    
main()
    
    