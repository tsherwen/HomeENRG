
from PV_read_tools import *

# ---  Output settings for direct main call
DEBUG=False
VERBOSE=False


def main( verbose=False, debug=False ):

    # Get data
    df = get_PV_daily_data_from_GEO( return_DataFrame=True )    

    # Print moving averages
    prt_mv_averages( df=df )
    
    # Print summary stats
    prt_overall_stats( df=df )
    
def prt_mv_averages( df=None, ):

    # Set Local variables
    titles = '5 day mv. avg.','10 day mv. avg.','15 day mv. avg.',
    mv_avgs = [ 5, 10, 15 ] 
    pstr = '{:<40}'+ '{:<20}'*len( titles )
    npstr = '{:<40}'+ '{:<20,.3f}'*len( titles)
    print pstr.format( 'Variable', *titles )

    # Get stats for each column
    for col in df.columns[1:]:
        
        vars = [ movingaverage( df[ col ].values, i )[-1] for i in mv_avgs ]
        print npstr.format( col, *vars )


def prt_overall_stats( df=None):

    titles = [ 'last day',  'total so far', 'max' ]
    pstr = '{:<40}'+ '{:<20}'*len( titles )
    npstr = '{:<40}'+ '{:<20,.3f}'*len( titles)
    print 
    print pstr.format( 'Variable', *titles )

    # Get stats for each column
    for col in df.columns[1:]:
        
        vars = [  df[ col ].values[-1], np.sum( df[ col ].values ), 
            np.max(df[ col ].values ),   ]
        print npstr.format( col, *vars )
    

if __name__ == "__main__":
    main( verbose=VERBOSE, debug=DEBUG )
