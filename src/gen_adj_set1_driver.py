import numpy as np
import preprocessing

NUM_FILES=10

IN_FILES=[ '/opt2/D4D/data/SET1/raw/SET1TSV_'+str(i)+'.TSV' \
    for i in xrange(0,NUM_FILES) ]
CALLS_OUT_FILES=[ 'set1_t'+str(i)+'_cum_num_calls' \
    for i in xrange(0,10) ]
TIME_OUT_FILES=[ 'set1_t'+str(i)+'_cum_call_time' \
    for i in xrange(0,10) ]

# open files in set1 and process
for i in xrange(0,len(IN_FILES)):
    # read data into numpy ndarrays (adjacency matrices containing
    #   # calls, cum. time in seconds between pairs of antennas
    #   for a complete time period)
    fp = open(IN_FILES[i], 'r')
    calls, time = preprocessing.set1_tsv_to_adj_mat(fp)
    fp.close

    # write out to binary numpy archives
    preprocessing.write_bin_adj_mat(CALLS_OUT_FILES[i], calls)
    preprocessing.write_bin_adj_mat(TIME_OUT_FILES[i], time)
