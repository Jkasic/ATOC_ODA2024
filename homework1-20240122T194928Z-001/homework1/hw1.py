# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 17:42:43 2024

@author: jfk3
"""

import matplotlib   # library for plotting
import matplotlib.pyplot as plt # basic plotting; later you will type plt.$COMMAND
import numpy as np # basic math library  you will type np.$STUFF  e.g., np.cos(1)
import scipy.stats as stats # imports stats functions https://docs.scipy.org/doc/scipy/reference/stats.html  
import pandas as pd
# from igor.binarywave import load as loadibw

# def load_ch4_c2h6():
#     '''
#     Load carbon monoxide data from air-sampling station.
#     (igor binary file)
#     OUTPUT:
#         co = (Pandas dataframe) ppbv CO vs time
#     '''
#     d_ch4 = r'PointSensors/CH4 and C2H6'
#     fname = r'/CH4_noSpikes_1min.ibw'
#     ppb_ch4 = loadibw(d_ch4 + fname)['wave']['wData']
#     time = loadibw(d_ch4 + r'/CH4_time_UTC_1min.ibw')['wave']['wData']
#     time = pd.to_datetime(time, unit='s')
#     time -= pd.to_timedelta(24107, unit='D')
#     ch4 = pd.Series(ppb_ch4, index=time)
#     fname = r'/C2H6_noSpikes_1min.ibw'
#     ppb_c2h6 = loadibw(d_ch4 + fname)['wave']['wData']
#     c2h6 = pd.Series(ppb_c2h6, index=time)
#     return ch4, c2h6

#Load data
DCS = pd.read_csv(r'cuny_data_20231108.csv')
Point = pd.read_csv(r'TILDAS_CH4.csv')

# Create a datetime column from an existing column 
Point['datetime_column'] = pd.to_datetime(Point['Time'])
DCS['datetime_column'] = pd.to_datetime(DCS['Unnamed: 0'])

# Set the new datetime column as the index
Point.set_index('datetime_column', inplace=True)
DCS.set_index('datetime_column', inplace=True)

# Resample to hourly averages
Point = Point['CH4.0'].resample('1H').mean()
DCS = DCS['x_ch4_dry'].resample('1H').mean()

#Select only daily averages
Point = Point[ (Point.index.hour >=11) & (Point.index.hour <=16) ]
DCS = DCS[ (DCS.index.hour >=11) & (DCS.index.hour <=16) ]

# Set timeframe
start_date = '2023-07-1' 
end_date = '2023-08-20'  

# Filter DataFrame for the chosen date range
Point = Point[(Point.index >= start_date) & (Point.index <= end_date)] 
DCS = DCS[(DCS.index >= start_date) & (DCS.index <= end_date)] 


# Plot the two time series
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
plt.scatter(DCS.index, DCS, label='DCS')
plt.scatter(Point.index, Point, label='Point Sensor')
plt.xlabel('Datetime')
plt.ylabel('CH4 (PPB)')
plt.title('Path vs Point Measurement of CH4')
plt.legend()  # Show legend

# Display the plot
plt.show()