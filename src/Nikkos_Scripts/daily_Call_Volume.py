import numpy as np
import csv
import datetime

'''
Program Name:   Volume of Calls in each Sub Prefectures
Program File:   daily_Call_Volume.py
Purpose:        To construct a data set containing the volume of calls of data
                set 3 made in each prefecture during each day
Output File:    daily_Call_Volume_Table.csv
Authors:        Nicholas Vogel (Nikko)
Date Modified:  10/11/2013
'''

################################################################################
#  Read in a TSV (tab separated value) file and create a 2D array file where   #
#each row represents a day and each column represents the number of calls made #
#in that prefecture during that day                                            #                             
################################################################################
def tsv_to_day_files(files,df):
    af = open(df,'rb')
    days = af.readline().strip('\n\r').split(',')
    af.close()
    days_vol = np.zeros((255,len(days)),dtype=np.uint32)
    for f in files:
        fp=open(f,'rb')
        for line in fp:
            line = line.strip('\n"\r').split('\t')
            day = line[1].split(" ")[0]
            pref = int(line[2])
            if pref>0:
                days_vol[pref-1][days.index(day)] += 1
        fp.close()
    print 'Finished filling in days_vol array, now writing'
    fout = open('daily_Call_Volume_Table.csv','wb')
    writer = csv.writer(fout, delimiter=',')
    for x in range(255):
        writer.writerow(days_vol[x])
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

tsv_to_day_files(files,'date_Array_Table.csv')
