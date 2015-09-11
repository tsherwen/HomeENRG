import datetime as datetime
import matplotlib.pyplot as plt
import pandas as pd 

# ---  Setings
start_date =  [2015, 03, 20 ]
end_date = [2015, 03, 21]
start_date, end_date = [ datetime.datetime( *i ) for i in start_date, end_date]
wd = '/Users/Tomas/PV_panels_dat_files/'
file = 'getDailyDetails_15_03.csv'

# --- Get Data
df = pd.read_csv(wd+file, parse_dates=True )# date_format='%Y-%m-%d %H:%M')
print df
print type(df['Date'][0] ), df['Date'][0] 
df.index = pd.to_datetime(df['Date'])

print df
print  start_date, end_date
print type(df.index[0] ), df.index[0] 
df =df[ start_date:end_date]
print df
# --- Acculate over a day
#df = df.cumsum()
print df.columns
print df[r' Generated (kW h)']

# --- plot up
fig = plt.figure(figsize=(20,10), dpi=80, facecolor='w', edgecolor='k')
ax1 = fig.add_subplot(111)
plt.plot(df.index, df[r' Generated (kW h)'])
plt.ylabel( 'kWh output' )
plt.rcParams.update({'font.size': 20})
plt.title('PV output, York (3.6 kW SunPower + GOODWE inverter)')
plt.show()