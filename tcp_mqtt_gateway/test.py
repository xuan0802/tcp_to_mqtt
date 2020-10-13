import datetime
from datetime import timedelta
import string
import time as t_gps
import time as t_bat

def cal_diff_time(input_date_curr,input_data_prev):
    input_date = input_date_curr.split('+')
    time_data  = input_date[0]
    date_data  = input_date[1]

    time1 = time_data.split(':')
    hh = time1[0]
    mmin = time1[1]
    ss = time1[2]

    date1 = date_data.split('-')
    dd = date1[0]
    mm = date1[1]
    yy = date1[2]

    format_date_curr = '20' + yy + '-' + mm + '-' + dd + ' ' + hh + ':' + mmin + ':' + ss

    input_date = input_data_prev.split('+')
    time_data = input_date[0]
    date_data = input_date[1]

    time1 = time_data.split(':')
    hh = time1[0]
    mmin = time1[1]
    ss = time1[2]

    date1 = date_data.split('-')
    dd = date1[0]
    mm = date1[1]
    yy = date1[2]

    format_date_prev = '20' + yy + '-' + mm + '-' + dd + ' ' + hh + ':' + mmin + ':' + ss

    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    diff = datetime.datetime.strptime(format_date_curr, datetimeFormat) - datetime.datetime.strptime(format_date_prev, datetimeFormat)

    return diff.seconds

date1_mictrack = '23:00:06+10-06-20'
date2_mictrack = '00:00:09+11-06-20'

diff_seconds =   cal_diff_time(date2_mictrack,date1_mictrack)
print("Seconds:",diff_seconds)

start_bat = t_bat.time()
start_gps = t_gps.time()
print(start_bat)
print(start_gps)
for i in range(1000):
    print(i)
stop_bat = t_bat.time()
time_bat = stop_bat - start_bat
print(time_bat)
start_bat = stop_bat
print(start_bat)
for i in range(1000):
    print(i)

stop_bat = t_bat.time()
time_bat = stop_bat - start_bat
print(time_bat)

stop_gps = t_gps.time()
time_gps = stop_gps - start_gps
print(time_gps)


