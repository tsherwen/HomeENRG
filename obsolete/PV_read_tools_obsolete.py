
def daily_detail_read(wd=None, reader=None):
    if (reader == None):
        files =  glob.glob(wd+'getDailyDetails_*')
    data=[]                                                                                                                                              
    for file in files:
        reader = open(file)
        print file
        for row in reader:
            data.append( np.array([ item.split(',') \
                for item in row.splitlines()] )[0][:, np.newaxis] )    
    data = np.concatenate(data, axis=1)
    data, titles  = remove_titles(data)
    dates = data[0,:]
    min_15_kwh = data[1,:] 
    dates, labels = time_2_num_and_labels(dates)
    return dates, min_15_kwh, titles, labels
    
def remove_titles(data):
    data_p = []
    titles = data[:,0]
    for i in range( len( data[0,:] ) ):
        if data[0,i] == 'Date':
            print data[:,i]
        else :
            data_p.append( data[:,i][:,np.newaxis] )
    data_p = np.concatenate( data_p, axis = 1 )
    return data_p, titles

def daily_total_read(wd=None,fn=None,reader=None, rm_last=False):


    # set file
    if isinstance( fn, type(None) ):
        fn = wd+'getDailyTotals_all.csv'
    else:
        fn = wd + fn

    # read csv file
    df = pd.read_csv( fn, 'r' , delimiter=',')
    titles = df.columns
    df.index = pd.to_datetime(df['Date'])
    print df.index
    print df.index

    # get moving averages on a 5, 10, 15 scale
    day_kwh = df[' Generated (kW h)'].values
    y_av     =  movingaverage(day_kwh, 5)
    y_av_II  = movingaverage(day_kwh, 10)
    y_av_III = movingaverage(day_kwh, 15)
    labels = [ num2month(i.month) for i in df.index ]

    return df.index.values, day_kwh, labels, y_av, y_av_II, y_av_III , 5,10, 15 