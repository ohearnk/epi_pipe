import numpy as np
import csv

'''
Program Name:   Number of Calls Made by Each CallerID
Program File:   caller_Num_Calls.py

Purpose:    To generate a data set to record the number of calls, in data set 3,
        made by each CallerID in the country (not -1).  This data set is
        generated as a supporting data set for future calculations.

Output File:    caller_Num_Calls_Table.csv
Authors:        Nicholas Vogel (Nikko)
Date Modified:  10/17/2013
'''

################################################################################
#Create an array of the number of calls made by each Caller ID                 #
################################################################################
def caller_Calls(files):
    callerCalls = np.zeros((500000,2))
    for x in range(1,500001):
        callerCalls[x-1][0] = x
    for f in files:
        fp=open(f,'rb')
        for line in fp:
            line = line.strip('\n"\r').split('\t')
            if (int(line[2]) != -1 and int(line[0]) != -1):
                callerCalls[int(line[0])-1][1] += 1
        fp.close()
    fout = open('caller_Num_Calls_Table.csv','wb')
    writer = csv.writer(fout, delimiter = ',')
    for x in range(0,500000):
        writer.writerow(callerCalls[x])
    fout.close()



################################################################################
#Test and Execute                                                              #
################################################################################
files=["/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_A.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_B.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_C.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_D.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_E.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_F.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_G.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_H.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_I.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_J.TSV"]
caller_Calls(files)
