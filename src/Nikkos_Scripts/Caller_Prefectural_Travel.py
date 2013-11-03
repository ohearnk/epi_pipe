import numpy as np
import csv

'''
Program Name:   Cronological order of prefectures CallerID made calls in
Program File:   Caller_Prefectural_Travel.py

Purpose:    To generate a data set of the chronological shifts in sub prefectural
        locality of each caller ID durring the recording period of data set 3
        based upon the sub prefectures in which they made calls of data set 3.

Output File:    Caller_Prefectural_Travel_Table.csv
Authors:        Nicholas Vogel (Nikko)
Date Modified:  10/11/2013
'''

################################################################################
#For each Caller ID create a cronological record of prefectures in which calls #
#were made in, excluding any concurrent prefecture calls.                      #
################################################################################
def caller_Movement(files):
    callerLocs = [[] for x in xrange(500000)]
    for x in range(0,500000):
        callerLocs[x].append(x+1)
    for f in files:
        fp=open(f,'rb')
        try:
            for line in fp:
                line = line.strip('\n"\r').split('\t')
                if(int(line[2]) != -1 and int(line[0]) != -1 and
                       callerLocs[int(line[0]) - 1][-1] != int(line[2])):
                    callerLocs[int(line[0]) - 1].append(int(line[2]))
        except IndexError:
            print line
            sys.exit(1)
        fp.close()
    fout = open('Caller_Prefectural_Travel_Table.csv','wb')
    writer = csv.writer(fout, delimiter = ',')
    for caller in callerLocs:
        writer.writerow(caller)
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
caller_Movement(files)
