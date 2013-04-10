import matplotlib.pyplot as plt
import numpy as np
import preprocessing as pp


def inter_indiv_call_ratios(adj_mat, t, indiv_call_ratios, 
        cum_call_ratios, num_no_calls):
    # calculate the ratios for all antennas
    indiv_ratios = []
    for i in xrange(adj_mat.shape[0]):
        row_sum = np.sum(adj_mat[i,:])
        if row_sum > 0:
            indiv_ratios.append(float(adj_mat[i,i])/row_sum)
        # tempoary fix to avoid division by zero
        else:
            indiv_ratios.append(0.0)
            num_no_calls[t] += 1
    indiv_call_ratios.append(indiv_ratios)

    # calculate cumulative ratios
    num_inner_calls = np.trace(adj_mat)
    num_outer_calls = 0
    for i in xrange(adj_mat.shape[0]):
        for j in xrange(adj_mat.shape[1]):
            if i < j:
                num_outer_calls = num_outer_calls + adj_mat[i,j]
    cum_call_ratios.append(float(num_inner_calls) / (num_inner_calls+num_outer_calls))
    
    # plot the sorted individual call data
    # note: use the local indiv_ratios list instead of the multi-time period indiv_call_ratios
    # list since this plot required the data be manipulated in-place
    indiv_ratios.sort()
    indiv_ratios.reverse()
    plt.plot([j for j in xrange(len(indiv_ratios))], indiv_ratios)
    plt.title("Inter-Antenna Ratios In Decreasing Order, Time Period %d" % t)
    plt.xlabel("Antenna IDs (Scrambled After Sorting)")
    plt.ylabel("Ratio of Inter-Antenna Calls to All Calls")
    plt.savefig("inter_antenna_sorted_t%d.pdf" % t)
    # clear the state of the current figure and release memory
    plt.close()

    return indiv_call_ratios, cum_call_ratios, num_no_calls


if __name__ == "__main__":
    indiv_call_ratios = []
    indiv_time_ratios = []
    cum_call_ratios = []
    cum_time_ratios = []
    CALL_FILES = [ '/opt2/D4D/data/SET1/adj_mats/cum_num_calls/set1_t%d_cum_num_calls.npy' % i
        for i in xrange(10) ]
    TIME_FILES = [ '/opt2/D4D/data/SET1/adj_mats/cum_num_calls/set1_t%d_cum_call_time.npy' % i
        for i in xrange(10) ]
    num_no_calls = [ 0 for i in xrange(10) ]

    # process all of the adjacency matrices
    for i, FILE in enumerate(CALL_FILES):
        adj_mat = pp.load_bin_adj_mat(FILE)

        # calculate and plot the call ratios for this time period
        indiv_call_ratios, cum_call_ratios, num_no_calls = \
                inter_indiv_call_ratios(adj_mat, i, indiv_call_ratios, cum_call_ratios, num_no_calls)

    print "Cumulative ratios:"
    for i in xrange(len(cum_call_ratios)):
        print "\tTime period %d: %f" % (i, cum_call_ratios[i])
        print "\t\tNumber of antennas without any calls: %d" % num_no_calls[i]
