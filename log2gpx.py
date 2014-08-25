
# coding: utf-8

# https://github.com/tkrajina/gpxpy
# 

# In[1]:

import glob
import gzip
import os
import zipfile
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

modes = { zipfile.ZIP_DEFLATED: 'deflated',
          zipfile.ZIP_STORED:   'stored',
          }

import csv
import gpxpy
import gpxpy.gpx


import urllib2
from datetime import datetime,timedelta


# csv format
# file name is: MMDDYY_HHMM_SS.csv.gz
# line data is: lat, long, compass, speed(kph), distance (kms), time (milliseconds), 
# and finally an input field for optional points of interest.
# other reference: 
# http://www.doughellmann.com/PyMOTW/zipfile/
# https://developers.google.com/kml/documentation/kmzarchives

    
def millisec_to_time(ms):
    d = 0
    s = 0
    while ms >= 1000:
        s += 1
        ms -= 1000
        if s >= 3600*24:
            d += 1
            s -= 3600*24
    return timedelta(days=d,seconds=s,milliseconds=ms)   


# In[2]:

os.chdir('2014')


# In[3]:

#os.chdir('2014')

#https://docs.python.org/2/library/datetime.html

log_files = glob.glob('*.csv.gz')
anti_map_headers = ['latitude','longitude', 'bearing', 'speed', 'distance', 'time','label']
DOWNSAMPLE = 300 # logged at 30 points/sec so just keep one per 10 second
for log_file in log_files:
    
    print log_file
    time_start = datetime.strptime(log_file.split('.')[0], '%d%m%y_%H%M_%S')
    
    print 'log start:', time_start
    gpx_file = log_file.replace('csv.gz','gpx')
    
    gpx_file = time_start.strftime('%y%m%d_%H%M_%S')+'.gpx'
    #print gpx_file
    #break
    gpx_path = gpx_file
    if os.path.exists(gpx_path):
        print 'file exists: skipping', gpx_path
        continue
    gpx = gpxpy.gpx.GPX()

    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # Create first segment in our GPX track:
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    
    log_fh = gzip.open(log_file,'rb')
    idx = -1
    coordinates = ''
    for row in csv.DictReader(log_fh,fieldnames=anti_map_headers):
        idx += 1
        if idx % DOWNSAMPLE != 0:
            continue
        row_time = millisec_to_time(int(row['time']))
        timestamp = time_start + row_time
        #coordinates += '''%s,%s ''' % (row["longitude"],row["latitude"])
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(row["latitude"], row["longitude"], time=timestamp))

    
    #gpx_folder = gpx_file.split('.')[0]
    #if os.path.exists(gpx_folder) and os.path.isdir(gpx_folder):
    #    print gpx_folder, 'exists'
    #else:
    #    os.mkdir(gpx_folder)
    #gpx_path = os.path.join(gpx_folder,gpx_file)    
    
    
    gpx_writer = open(gpx_path,'w')
    gpx_writer.write(gpx.to_xml())
    gpx_writer.close()


# In[4]:

get_ipython().magic(u'pinfo gpxpy.gpx.GPXTrackPoint')



# In[ ]:



