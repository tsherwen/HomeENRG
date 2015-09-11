import pandas as pd
import matplotlib.pyplot as plt

def main():
    """ Plot up data by month as box plots """
    # get daily totals
    dates, data = get_PV_daily_data()

    # plot up as monthly values
    plot_monthly_boxplots( dates, data )

    #
    
    
    
def get_PV_daily_data( fn=None, column=r' Generated (kW h)'):
    """ Extract PV data from CSV using pandas read_csv """

    # Get data
    try:
        wd = sys.argv[1]
    except:
        wd ='./'#'<insert_default_directory_here>'
    print wd

    # Set file
    if isinstance( fn, type(None) ):
        fn = wd+'getDailyTotals_all.csv'
    else:
        fn = wd + fn

    # read csv file
    df = pd.read_csv( fn, 'r' , delimiter=',')
    titles = df.columns
    df.index = pd.to_datetime(df['Date'])
    return  df[column], df.index

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
    
    