import csv
import math
import sys

def read_csv(FILE):
    data = [ ]

    # create CSV reader
    with open(FILE, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',',
            quotechar='|')
        # skip header
        reader.next()
        for RECORD in reader:
            # (ego ID, time period, 1-hop density, 1-hop rawComm)
            data.append(
                [ int(RECORD[1]), int(RECORD[0]),
                  float(RECORD[7]), float(RECORD[9]) ]
            )

    return data


def calc_metrics(ego_data,min_density,min_raw_comm):
    dist_sum = 0.0
    avg_density = 0.0
    avg_raw_comm = 0.0
    eucl_dist = lambda x,y: math.sqrt(x**2+y**2)

    # calculate Euclidean distance of the change over the 10 time periods
    for i in xrange(len(ego_data)-1):
        # apply threshold
        if ego_data[i][2] < min_density or ego_data[i][3] < min_raw_comm:
            dist_sum = None
            break
        # sum scores
        dist_sum = dist_sum + eucl_dist(ego_data[i][2],ego_data[i][3])

    # calculate average density and average rawComm
    for i in xrange(len(ego_data)):
        avg_density = avg_density + ego_data[i][2]
        avg_raw_comm = avg_raw_comm + ego_data[i][3]
    avg_density = avg_density / 10.0
    avg_raw_comm = avg_raw_comm / 10.0

    # (ego ID, dist_sum, avg_raw_comm)
    return (ego_data[0][0], dist_sum, avg_density, avg_raw_comm)


##### main #####
def main():
    if len(sys.argv) == 3:
        # thresholds
        min_density = float(sys.argv[1])
        min_raw_comm = int(sys.argv[2])
    else:
        return

    in_file = 'set4.csv'

    dist_scores = [ ]

    data = read_csv(in_file)
    # sort data by ego ID
    data.sort()

    # calculate sum of distance scores
    for i in xrange(0,len(data)/10):
        dist_scores.append(calc_metrics(data[i*10:(1+i)*10],min_density,min_raw_comm))

    dist_scores_threshold = [ ]
    for score in dist_scores:
        if not score[1] is None:
            dist_scores_threshold.append(score)

    print 'Thresholds:'
    print '\tdensity >=', min_density
    print '\trawComm >=', min_raw_comm
    print 'Num after threshold:',len(dist_scores_threshold)
    print
    print 'Ego : Score'
    for score in dist_scores_threshold:
        print '\t',score[0],':',score[1]
    print
    print 'Minimum score:'
    print '\t', min([score[1] for score in dist_scores_threshold])
    #print '\t',dist_scores_threshold[dist_scores_threshold.index(min([score[1] for score in dist_scores_threshold]))], \
    #    ':',min([score[1] for score in dist_scores_threshold])

    print
    print 'Minimum avg density:'
    print '\t', min([score[2] for score in dist_scores_threshold])
    print 'Maximum avg density:'
    print '\t', max([score[2] for score in dist_scores_threshold])
    print 'Minimum avg rawComm:'
    print '\t', min([score[3] for score in dist_scores_threshold])
    print 'Maximum avg rawComm:'
    print '\t', max([score[3] for score in dist_scores_threshold])


if __name__ == "__main__":
    main()
