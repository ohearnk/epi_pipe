import numpy as np
import csv

'''
Program Name:   Calls by each sub prefecture population Made in each Sub
                Prefecture
Program File:   pref_Population_Movement_Calls.py

Purpose:    To generate a data set to record the number of calls, in data set 3,
        made in each sub prefecture by callers from each home sub prefecture.
        The assumption was made that the sub prefecture in which a caller made
        the most calls is their home sub prefecture.  With this assumption was
        used to characterize the home sub prefecture and determine each sub
        prefectures call activity in each sub prefecture.

Output File:    pref_Population_Movement_Calls_Table.csv
Authors:        Nicholas Vogel (Nikko)
Date Modified:  10/11/2013
'''

################################################################################
#Create an array of the number of calls each Caller ID made a call in each     #
#Sub-Prefecture                                                                #
################################################################################
def caller_Movement(files):
    callerLocs = np.zeros((500000,255))
    for f in files:
        fp=open(f,'rb')
        try:
            for line in fp:
                line = line.strip('\n"\r').split('\t')
                if(int(line[2]) != -1 and int(line[0]) != -1):
                    callerLocs[int(line[0]) - 1][int(line[2]) - 1] += 1
        except IndexError:
            print line
            sys.exit(1)
        fp.close()
    return callerLocs


################################################################################
#Create an array of the number of calls made in each prefecture (column), by   #
#callers from each prefecture (Row)                                            #
################################################################################
def prefPopMove(files):
    callerLocs = caller_Movement(files)
    prefArray = np.zeros((255,255))
    for caller in callerLocs:
        homePref = np.argmax(caller)
        prefArray[homePref] = np.sum([caller,prefArray[homePref]], axis = 0)
    fout = open('pref_Population_Movement_Calls_Table.csv','wb')
    writer = csv.writer(fout, delimiter = ',')
    for pref in prefArray:
        writer.writerow(pref)
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
prefPopMove(files)
