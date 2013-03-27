import numpy as np

def create_2hop_adj_list(fp):
    two_hop_adj_dict = { }

    # loop through data, creating ego nodes, ego to 1-hop links,
    # and 1-hop nodes in the dictionary
    for line in fp:
        # read and tokenize line, convert to integers for sorting
        line = [ int(elem) for elem in line.split() ]
        # ensure ego, if present, is in position 0 by sorting in place
        line.sort()
        # ego
        if line[0] <= 10000:
            # add key if not present
            if not line[0] in two_hop_adj_dict:
                two_hop_adj_dict[line[0]] = [ ]
            # add non-ego nodes
            for i in xrange(1, len(line)):
                # add non-ego
                two_hop_adj_dict[line[0]].append(line[i])
                # add non-ego key, if not present (for next loop through file)
                if not line[i] in two_hop_adj_dict:
                    two_hop_adj_dict[line[i]] = [ ]
    
    # reset the file pointer to the beginning (byte 0) of the file
    fp.seek(0)

    # add in the 1-hop to 1-hop links
    for line in fp:
        # read and tokenize line, convert to integers for sorting
        line = [ int(elem) for elem in line.split() ]
        # ensure ego, if present, is in position 0 by sorting in place
        line.sort()
        # non-ego pairs both as keys in the dictionary -> add link
        if len(line) == 2 and line[0] > 10000 \
        and line[0] in two_hop_adj_dict and line[1] in two_hop_adj_dict:
            two_hop_adj_dict[line[0]].append(line[1])
    
    # reset the file pointer to the beginning (byte 0) of the file
    fp.seek(0)

    # add the 1-hop to 2-hop links and 2-hop nodes
    for line in fp:
        # read and tokenize line, convert to integers for sorting
        line = [ int(elem) for elem in line.split() ]
        # sort in place
        line.sort()
        if len(line) == 2 and line[0] > 10000 \
        and line[0] in two_hop_adj_dict and line[1] not in two_hop_adj_dict:
            two_hop_adj_dict[line[0]].append(line[1])
            two_hop_adj_dict[line[1]] = [ ]

    return two_hop_adj_dict


def write_1hop_adj_list(one_hop_adj_list, fp):
    # 1) create a list of all keys in dictionary and sort
    # 2) create strings of each adjacency list, creating lists
    #    and sorting along the way as necessary
    # 3) write strings to file
    one_hop_list = two_hop_adj_dict.keys()
    one_hop_list.sort()

    for node in one_hop_list:
        s = str(node)
        link_list = two_hop_adj_dict[node]
        link_list.sort()
        for link in link_list:
            s = s + ' ' + str(link)
        # don't forget the newline with write( )!
        s = s + '\n'
        fp.write(s)


def write_adj_matrix(adj_dict, FILE_BASE):
    # extract all keys
    ego_list = adj_dict.keys()

    # remove all elements greater than 10000
    # note: this is a built-in function that adopts
    # from functional programming
    def f(x): return x <= 10000
    ego_list = filter(f, ego_list)

    # sort the ego list
    ego_list.sort()

    # create the adjaency matrix for the 1-hop network
    # around each ego
    for ego in ego_list:
        # create sorted list of all nodes in 1-hop network
        ego_adj_list = [ ego ] + adj_dict[ego]
        ego_adj_list.sort()

        # create adjacency matrix        
        adj_mat = np.zeros((len(ego_adj_list),
            len(ego_adj_list)), dtype=int)

        # add links
        for node in ego_adj_list:
            for node2 in adj_dict[node]:
                adj_mat[ego_adj_list.index(node), 
                    ego_adj_list.index(node2)] = \
                adj_mat[ego_adj_list.index(node2),
                    ego_adj_list.index(node)] = 1

        np.savetxt(FILE_BASE+str(ego)+'_2hop_adj_mat.txt', adj_mat,
        fmt='%d', delimiter=' ')

        # write adjency matrix
        fp = open(FILE_BASE+str(ego)+'_2hop_adj_mat.txt', 'a')

        s = '\n' + str(ego_adj_list[0])
        for i in xrange(1, len(ego_adj_list)):
            s = s + ' ' + str(ego_adj_list[i])
        fp.write(s)

        fp.close()


#### BEGIN MAIN ####
# files to process
IN_FILES=[ '/opt2/D4D/data/SET4/raw/tsv/GRAPHS_'+str(i)+'.TSV' \
    for i in xrange(0,10) ]
OUT_FILES=[ 'set4_t'+str(i)+'_2hop_adj_list.txt' \
    for i in xrange(0,10) ]
OUT_FILES2_BASE=[ 'set4_t'+str(i)+'_id' \
    for i in xrange(0,10) ]

for i in xrange(0,len(IN_FILES)):
    # create a file pointer, open data file for reading
    fp_in = open(IN_FILES[i], 'r')

    # generate dictionary of all links in 1 hop network around ego
    two_hop_adj_dict = create_2hop_adj_list(fp_in)

    # create a file pointer for ego adjacency lists
    fp_out = open(OUT_FILES[i], 'w')

    # write the adjacency lists
#    write_1hop_adj_list(two_hop_adj_dict, fp_out)

    write_adj_matrix(two_hop_adj_dict, OUT_FILES2_BASE[i])

    # close file pointers
    fp_out.close()
    fp_in.close()
