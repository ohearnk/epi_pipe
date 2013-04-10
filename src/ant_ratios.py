import matplotlib.pyplot as plt
import numpy as np
import preprocessing as pp

ant_ratios = []
cum_ratios = []
FILES = [ '/opt2/D4D/data/SET1/adj_mats/cum_num_calls/set1_t'+str(i)+'_cum_num_calls.npy'
    for i in xrange(10) ]

# process all of the adjacency matrices
for FILE in FILES:
    adj_mat = pp.load_bin_adj_mat(FILE)

    indiv_ratios = []
    for i in xrange(adj_mat.shape[0]):
        row_sum = np.sum(adj_mat[i,:])
        if row_sum > 0:
            indiv_ratios.append(float(adj_mat[i,i])/row_sum)
        # tempoary fix to avoid division by zero
        else:
            indiv_ratios.append(0.0)
    ant_ratios.append(indiv_ratios)

    # calculate cumulative ratios
    num_inner_calls = np.trace(adj_mat)
    num_outer_calls = 0
    for i in xrange(adj_mat.shape[0]):
        for j in xrange(adj_mat.shape[1]):
            if i < j:
                num_outer_calls = num_outer_calls + adj_mat[i,j]
    cum_ratios.append(float(num_inner_calls) / (num_inner_calls+num_outer_calls))

#print "Individual ratios:"
#print ant_ratios
#print
print "Cumulative ratios:"
for i in xrange(len(cum_ratios)):
    print "\tTime period %d: %f" % (i, cum_ratios[i])

for i in xrange(10):
#    plt.plot([j for j in xrange(len(ant_ratios[i]))], ant_ratios[i])
#    plt.title("Inter-Antenna Ratios by Antenna, Time Period "+str(i))
#    plt.xlabel("Antenna ID")
#    plt.ylabel("Ratio of Inter-Antenna Calls to All Calls")
    ant_ratios[i].sort()
    ant_ratios[i].reverse()
    plt.plot([j for j in xrange(len(ant_ratios[i]))], ant_ratios[i])
    plt.title("Inter-Antenna Ratios by Decreasing Ratio, Time Period "+str(i))
    plt.xlabel("Meaningless Number")
    plt.ylabel("Ratio of Inter-Antenna Calls to All Calls")
    plt.show()
