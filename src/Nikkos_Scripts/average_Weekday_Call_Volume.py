import numpy as np
import csv
import datetime

'''
Program Name:   Average Weekday Call Volumes of Sub Prefectures
Program File:   average_Weekday_Call_Volume.py
Purpose:        To construct an table of the average volume of calls made in
                each sub prefecture (column) for each day of the week (row).
Output File:    average_Weekday_Call_Volume_Table.csv
Authors:        Nicholas Vogel (Nikko)
Date Modified:  10/11/2013
'''

################################################################################
#  Construct an array for each day of the week of the average call volume in   #
#each prefecture and save it to a file                                         #
################################################################################
def day_o_week_cv_ave(ttdf,df):
    f1 = open(ttdf,'rb')
    f2 = open(df,'rb')
    days = f2.readline().strip('\n\r').split(',')
    numdays = len(days)
    f2.close()
    days = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in days]
    week_day_vol = np.zeros((255,7),dtype=np.int)
    count = 0
    for line in f1:
        line = np.array(line.strip('\n\r').split(",")).astype(int)
        for x in xrange(numdays):
            week_day_vol[count][days[x].weekday()] += line[x]
        count += 1
    f1.close()
    weekday=np.zeros(7,dtype=np.int)
    for x in xrange(numdays):
        weekday[days[x].weekday()] += 1
    fout = open('average_Weekday_Call_Volume_Table.csv','wb')
    writer = csv.writer(fout, delimiter = ',')
    for x in range(255):
        writer.writerow([week_day_vol[x][y]/weekday[y] for y in range(0,7)])
    fout.close()


################################################################################
#Test and Execute                                                              #
################################################################################

#Every file of dataset 3
files = ["/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_A.TSV",
         "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_B.TSV",
         "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_C.TSV",
         "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_D.TSV",
         "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_E.TSV",
         "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_F.TSV",
         "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_G.TSV",
         "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_H.TSV",
         "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_I.TSV",
         "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_J.TSV"]

day_o_week_cv_ave('daily_Call_Volume_Table.csv','date_Array_Table.csv')
