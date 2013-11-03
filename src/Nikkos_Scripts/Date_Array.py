import numpy as np
import csv
import datetime

'''
Program Name:   Create Date Array of Data Set 3
Program File:   Date_Array.py
Purpose:        To construct a supporting data set containing the dates durring
                which data set 3 was recorded
Output File:    date_Array_Table.csv
Authors:        Nicholas Vogel (Nikko)
Date Modified:  10/11/2013
'''

################################################################################
#  Record, sort and save the dates durring which data set 3 was recorded       #
################################################################################
def create_date_array(files):
    days = []
    #count=0
    for f in files:
        fp=open(f,'rb')
        for line in fp:
            #count=count+1
            line = line.strip('\n"\r').split("\t")
            #print line
            day = line[1].split(" ")[0]
            #print day
            if day not in days:
                days.append(day)
        fp.close()
    dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in days]
    dates.sort()
    days = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates]
    print days
    fout = open('date_Array_Table.csv','wb')
    writer = csv.writer(fout, delimiter=',')
    writer.writerow(days)
    fout.close()

################################################################################
#Test and Execute                                                              #
################################################################################
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

create_date_array(files)
