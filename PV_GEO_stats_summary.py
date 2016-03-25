
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

    # --- Get stats for each column
    for col in df.columns[1:]:
        
        vars = [  df[ col ].values[-1], np.sum( df[ col ].values ), 
            np.max(df[ col ].values ),   ]
        print npstr.format( col, *vars )

    # --- Print out total days/annual days for whole data years
    str_years = sorted( set([str(i.year) for i in df.index]) )
    num_days = df.shape[0]
    num_years = num_days/365 # whole years
    # setup print strings
    pstr = '{:<40}'+ '{:<20}'* num_years 
    npstr = '{:<40}'+ '{:<20,.3f}'* num_years 
    titles = [ '-'.join(i) for i in chunks( str_years, num_years ) ]
    # number of days and years?
    print
    print 'Number of days: {}, & (whole) years: {}'.format( num_days, num_years ) + \
        ' install date {}'.format( df.index.min() ),  \
        'days left of this period: {}'.format( num_days-(365*num_years) ) 
    print
    print pstr.format( 'Variable', *titles )
    # Loop and print yearly values
    for col in df.columns[1:]:
        vars = [ np.sum( df[ col ][i*365:365+(i*365)].values ) \
                 for i in range( num_years) ]
        print npstr.format( col, *vars )
    # So far this year? ( and as a % of annual average and last year
    titles  = 'Ann. avg', 'this yr.(so far)', '% of ann. avg.', '% of lst. yr.'
    pstr = '{:<40}'+ '{:<20}'* len( titles )
    npstr = '{:<40}'+ '{:<20,.3f}'* len( titles )
    print
    print pstr.format( 'Variable', *titles )
    for col in df.columns[1:]:
        vars = [ np.sum( df[ col ][i*365:365+(i*365)].values ) \
                                  for i in range( num_years) ]
        annual_avg = np.mean( vars )
        last_yr = vars[-1]
        so_far_this_yr = np.sum( df[ col ][365*num_years:].values ) 
        pcent_so_far_of_ann_avg = so_far_this_yr/annual_avg*100
        pcent_so_far_of_lst_yr = so_far_this_yr/last_yr*100
        vars = annual_avg, so_far_this_yr, pcent_so_far_of_ann_avg, pcent_so_far_of_lst_yr
        
        print npstr.format( col, *vars )
        
        
def chunks(l, n):
    """ Split list in chunks - useful for controlling memory usage """
    if n < 1:
        n = 1
    return [l[i:i + n] for i in range(0, len(l), n)]
        
if __name__ == "__main__":
    main( verbose=VERBOSE, debug=DEBUG )
