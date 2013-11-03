import numpy as np
import csv
#sys.argv
#argparse

'''
Program Name:   Calls by each CallerID Made in each Sub Prefecture
Program File:   Caller_Calls_in_Prefs.py

Purpose:    To generate a data set to record the number of calls, in data set 3,
        made in each sub prefecture by each caller. The assumption was made that
        the sub prefecture in which a caller madethe most calls is their home
        sub prefecture.

Output File:    Caller_Calls_in_Prefs_Table.csv
Authors:        Nicholas Vogel (Nikko)
Date Modified:  10/17/2013
'''

################################################################################
#Create an array of the number of calls each Caller ID made a call in each     #
#Sub-Prefecture                                                                #
################################################################################
def caller_Movement(files):
    callerLocs = np.zeros((500000,255))
    for f in files:
        fp=open(f,'rb')
        for line in fp:
            line = line.strip('\n"\r').split('\t')
            if(int(line[2]) != -1 and int(line[0]) != -1):
                callerLocs[int(line[0]) - 1][int(line[2]) - 1] += int(1)
        fp.close()
    return callerLocs


################################################################################
#Determine the Home Prefecture of each CallerID, then create a table containing#
#the CallerID, their home prefecture, and the number of calls they made in each#
#sub prefecture                                                                #
################################################################################
def caller_call_loc_info(files):
    callerLocs = caller_Movement(files)
    callerCallsinPrefs = np.zeros((500000,257))
    for callerID in range(1,500001):
        homePref = np.argmax(callerLocs[callerID-1])
        callerCallsinPrefs[callerID-1][0] = callerID
        callerCallsinPrefs[callerID-1][1] = homePref
	for i in range(0,255):
            callerCallsinPrefs[callerID-1][i+2] = callerLocs[callerID-1][i]
    	print callerCallsinPrefs[callerID-1]
    fout = open('Caller_Calls_in_Prefs_Table.csv','wb')
    writer = csv.writer(fout, delimiter = ',')
    for caller in callerCallsinPrefs:
        writer.writerow(caller)
    fout.close()


################################################################################
#Test and Execute                                                              #
################################################################################
files=["/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_A.TSV"]#,
'''
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_B.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_C.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_D.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_E.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_F.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_G.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_H.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_I.TSV",
        "/opt2/D4D/data/SET3/raw/SUBPREF_POS_SAMPLE_J.TSV"]
'''
caller_call_loc_info(files)

