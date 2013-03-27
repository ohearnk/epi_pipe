def create_ego_adj_list(fp):
    ego_adj_dict = { }

    for line in fp:
        # read and tokenize line, convert to integers for sorting
        line = [ int(elem) for elem in line.split() ]
        # ensure ego, if present, is in position 0 by sorting in place
        line.sort()
        # ego
        if line[0] <= 10000:
            # add key if not present
            if not line[0] in ego_adj_dict:
                ego_adj_dict[line[0]] = [ ]
            # add non-ego nodes
            for i in xrange(1, len(line)):
                ego_adj_dict[line[0]].append(line[i])

    return ego_adj_dict

# file to process
FILES=[ '/opt2/D4D/data/SET4/raw/tsv/GRAPHS_'+str(i)+'.TSV' \
    for i in xrange(0,10) ]

for i in xrange(0,len(FILES)):
    # create a file pointer, open data file for reading
    fp_in = open(FILES[i], 'r')

    # generate dictionary of egos and connected nodes
    ego_adj_dict = create_ego_adj_list(fp_in)

    # create a file pointer for ego adjacency lists
    fp_out = open('set4_t'+str(i)+'_ego_adj_list.txt', 'w')

    # 1) create a list of all keys in ego dictionary and sort
    # 2) create strings of each ego adjacency list, creating lists
    #    and sorting along the way as necessary
    # 3) write strings to file
    ego_list = ego_adj_dict.keys()
    ego_list.sort()

    for ego in ego_list:
        s = str(ego)
        non_ego_list = ego_adj_dict[ego]
        non_ego_list.sort()
        for non_ego in non_ego_list:
            s = s + ' ' + str(non_ego)
        s = s + '\n'
        fp_out.write(s)
    
    # close file pointers
    fp_out.close()
    fp_in.close()
