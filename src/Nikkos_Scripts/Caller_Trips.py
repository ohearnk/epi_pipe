import numpy as np
import csv

'''
Program Name:   Trips made by Callers
Program File:   Caller_Trips.py

Purpose:    To generate a data set of the each callerID's trips out of their
        home sub prefecture of each caller ID durring the recording period of
        data set 3.

Output File:    Caller_Trips_Table.csv
Authors:        Nicholas Vogel (Nikko)
Date Modified:  10/11/2013
Tables Referenced: Caller_Prefectural_Travel_Table.csv
'''

################################################################################
#For each Caller ID record every out of home prefecture trip. Where every trip #
#starts and ends in the caller's home prefecture.                              #
################################################################################
def caller_Trips(files):
    callerTrips = [[]]
    fp=open(files,'rb')
    for line in fp:
        line = line.strip('\n"\r').split(',')
        if (len(line)>2):
	    trip = []
            trip.append(int(line[0]))
            trip.append(int(line[1]))
            for x in range(2,len(line)):
                if (int(line[x]) != int(line[1])):
                    trip.append(int(line[x]))
                elif(len(trip) != 0):
                    callerTrips.append(trip)
                    trip = []
                    trip.append(int(line[0]))
                    trip.append(int(line[1]))
    fp.close()
    fout = open('Caller_Trips_Table.csv','wb')
    writer = csv.writer(fout, delimiter = ',')
    for trip in callerTrips:
        writer.writerow(trip)
    fout.close()



################################################################################
#Test and Execute                                                              #
################################################################################
caller_Trips('Caller_Prefectural_Travel_Table.csv')
