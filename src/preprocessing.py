import networkx as nx
import numpy as np
import pygraphviz as pgv

# read in TSV (tab separated value) file and convert to
# a PyGraphviz graph object
def tsv_to_pgv_obj(fp):
    # create an empty graph object
    s4_pgv=pgv.AGraph()
    s4_pgv.node_attr['style']='filled'
    
    # add the nodes and edges
    for line in fp:
        # read and tokenize line, convert to integers for sorting
        line = [ int(elem) for elem in line.split() ]
        # sort to guarentee smallest node is first
        line.sort()
        # pair -- add both nodes and edge
        if len(line) == 2:
            # ego - color red
            if line[0] <= 10000:
                s4_pgv.add_node(line[0],fillcolor='red')
                s4_pgv.add_node(line[1])
            # add edge
            #  note: adds both nodes by default
            #  if they don't exist
            s4_pgv.add_edge(line)
        # singleton (must be ego)
        elif len(line) == 1:
            s4_pgv.add_node(line[0],fillcolor='red')
    
    return s4_pgv


# read in TSV file and convert to
# a NetworkX graph object
def tsv_to_nx(fp):
    # create an empty graph object
    nx_obj = nx.Graph()
    
    # add the nodes and edges
    for line in fp:
        # read and tokenize line, convert to integers for sorting
        line = [ int(elem) for elem in line.split() ]
        # sort to guarentee smallest node is first
        line.sort()
        # pair -- add both nodes and edge
        if len(line) == 2:
            # add edge
            nx_obj.add_edge(line[0], line[1])
        # singleton (must be ego)
        elif len(line) == 1:
            nx_obj.add_node(line[0])
    
    return nx_obj


# render a PyGraphviz graph object
# to a file in the format specified by
# out_file
def draw_pgv(pgv_obj, out_file):
    # set the layout to neato
    pgv_obj.layout()

    # write the graph to PDF with PyGraphviz
    pgv_obj.draw(out_file)


# convert a NetworkX graph object to an
# adjacency list
def nx_to_adj_list(nx_obj):
    # generate adjacency list
    adj_list = nx.generate_adjlist(nx_obj, delimiter=' ')

    return adj_list


def write_adj_list(output_file, adj_list):
    # write to ASCII file
    f = open(output_file+'_adjlist.txt', 'w')
    # iterate over the sorted generator object
    for line in sorted(adj_list):
        f.write(line+'\n')
    f.close

    # write adjacenty list in NetworkX adjacency format
    #nx.write_adjlist(s4_nx, output_file+'.adjlist')


# convert a NetworkX graph object to an
# adjanecy matrix
def nx_to_adj_mat(nx_obj):
    # get of sorted list of nodes in the graph
    node_list = nx_obj.nodes()
    node_list.sort()

    # generate the adjacency matrix
    #  -returned object is a NumPy matrix
    #  -nodelist kwarg determines row-columns order
    #  -weight kwarg determines whether entries in matrix
    #   are binary or edge weights in the graph 
    adj_mat = nx.adjacency_matrix(nx_obj, 
        nodelist=node_list)

    return node_list, adj_mat


def write_adj_mat(node_list, adj_mat, out_file):
    # write out the adjacency matrix
    np.savetxt(out_file, adj_mat,
    fmt='%d', delimiter=' ')

    # append the node list
    fp = open(out_file, 'a')

    s = '\n' + str(node_list[0])
    for i in xrange(1, len(node_list)):
        s = s + ' ' + str(node_list[i])
    fp.write(s)
    
    fp.close() 


def write_gml_format(nx_obj, out_file):
    nx.write_gml(nx_obj, out_file)


def create_1hop_adj_list(fp):
    one_hop_adj_dict = { }

    # loop through data, creating ego adjacency lists and non-ego keys
    # in a dictionary
    for line in fp:
        # read and tokenize line, convert to integers for sorting
        line = [ int(elem) for elem in line.split() ]
        # ensure ego, if present, is in position 0 by sorting in place
        line.sort()
        # ego
        if line[0] <= 10000:
            # add key if not present
            if not line[0] in one_hop_adj_dict:
                one_hop_adj_dict[line[0]] = [ ]
            # add non-ego nodes
            for i in xrange(1, len(line)):
                # add non-ego
                one_hop_adj_dict[line[0]].append(line[i])
                # add non-ego key, if not present (for next loop through file)
                if not line[i] in one_hop_adj_dict:
                    one_hop_adj_dict[line[i]] = [ ]
    
    # reset the file pointer to the beginning (byte 0) of the file
    fp.seek(0)

    # add in the non-ego adjacency lists
    for line in fp:
        # read and tokenize line, convert to integers for sorting
        line = [ int(elem) for elem in line.split() ]
        # ensure ego, if present, is in position 0 by sorting in place
        line.sort()
        # non-ego pairs both as keys in the dictionary -> add link
        if len(line) == 2 and line[0] > 10000 \
        and line[0] in one_hop_adj_dict and line[1] in one_hop_adj_dict:
            one_hop_adj_dict[line[0]].append(line[1])

    return one_hop_adj_dict


def write_1hop_adj_list(one_hop_adj_list, fp):
    # 1) create a list of all keys in dictionary and sort
    # 2) create strings of each adjacency list, creating lists
    #    and sorting along the way as necessary
    # 3) write strings to file
    one_hop_list = one_hop_adj_dict.keys()
    one_hop_list.sort()

    for node in one_hop_list:
        s = str(node)
        link_list = one_hop_adj_dict[node]
        link_list.sort()
        for link in link_list:
            s = s + ' ' + str(link)
        # don't forget the newline with write( )!
        s = s + '\n'
        fp.write(s)


def write_1hop_adj_matrix(one_hop_adj_dict, FILE_BASE):
    # extract all keys
    ego_list = one_hop_adj_dict.keys()

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
        ego_adj_list = [ ego ] + one_hop_adj_dict[ego]
        ego_adj_list.sort()

        # create adjacency matrix        
        adj_mat = np.zeros((len(ego_adj_list),
            len(ego_adj_list)), dtype=int)

        # add links
        for node in ego_adj_list:
            for node2 in one_hop_adj_dict[node]:
                adj_mat[ego_adj_list.index(node), 
                    ego_adj_list.index(node2)] = \
                adj_mat[ego_adj_list.index(node2),
                    ego_adj_list.index(node)] = 1

        np.savetxt(FILE_BASE+str(ego)+'_1hop_adj_mat.txt', adj_mat,
        fmt='%d', delimiter=' ')

        # write adjency matrix
        fp = open(FILE_BASE+str(ego)+'_1hop_adj_mat.txt', 'a')

        s = '\n' + str(ego_adj_list[0])
        for i in xrange(1, len(ego_adj_list)):
            s = s + ' ' + str(ego_adj_list[i])
        fp.write(s)

        fp.close()


def write_2hop_adj_matrix(adj_dict, FILE_BASE):
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
        # get the number of nodes in the ego's 2-hop network
        two_hop_nodes = [ego]
        for key in adj_dict[ego].keys():
            two_hop_nodes += [key] + adj_dict[key].keys()
        two_hop_nodes = list(set(two_hop_nodes))
        two_hop_nodes.sort()
        num_nodes = len(two_hop_nodes)

        # create adjacency matrix
        adj_mat = np.zeros((num_nodes,num_nodes), dtype=int)

        # add links
        for node in two_hop_nodes:
            # a bit of overkill...
            for adj_node in adj_dict[node].keys():
                adj_mat[two_hop_nodes.index(node), 
                    two_hop_nodes.index(adj_node)] = \
                adj_mat[two_hop_nodes.index(adj_node),
                    two_hop_nodes.index(node)] = 1

        np.savetxt(FILE_BASE+str(ego)+'_2hop_adj_mat.txt', adj_mat,
        fmt='%d', delimiter=' ')

        # write adjency matrix
        fp = open(FILE_BASE+str(ego)+'_2hop_adj_mat.txt', 'a')

        s = '\n' + str(two_hop_nodes[0])
        for i in xrange(1, len(two_hop_nodes)):
            s = s + ' ' + str(two_hop_nodes[i])
        fp.write(s)

        fp.close()


# read in adjacency matrix and node list from file
def load_adj_mat(FILENAME):
    adj_mat = np.loadtxt(FILENAME, dtype=int)
    # handle singletons differently
    if len(adj_mat.shape) == 1:
        node_list = [ adj_mat[1] ]
        adj_mat = np.matrix([ adj_mat[0] ], dtype=int)
    else:
        # last line is node list
        node_list = list(adj_mat[-1,:])
        adj_mat = adj_mat[:-1,:]

    return adj_mat, node_list


# read in adjacency matrix from the specified
# file and convert it to a PyGraphviz graph object
def adj_mat_to_pgv(adj_mat, node_list):
    # NOTE: it appears that networkx.from_numpy_matrix( ) is not
    # sophisticated enough to incorporate a node list, so we'll
    # do it the hard way

    # create an empty PyGraphviz graph object
    pgv_obj = pgv.AGraph()

    # add nodes
    for node in node_list:
        if node <= 10000:
            pgv_obj.add_node(node, color='red', sep='+2,2', nodesep=2, ranksep=2)
        else:
            pgv_obj.add_node(node, sep='+2,2', nodesep=2, ranksep=2)

    # add edges
    for i in xrange(0,adj_mat.shape[0]):
        # adjacency matrix is symmetric, so only
        # check upper triangular region for edges
        for j in xrange(i,adj_mat.shape[1]):
            if adj_mat[i,j] == 1:
                pgv_obj.add_edge(node_list[i], node_list[j])

    return pgv_obj


# read in adjacency matrix from the specified 
# file and convert it to a NetworkX graph object
def adj_mat_to_nx(adj_mat, node_list):
    # NOTE: it appears that networkx.from_numpy_matrix( ) is not
    # sophisticated enough to incorporate a node list, so we'll
    # do it the hard way

    # create an empty NetworkX graph object
    nx_obj = nx.Graph()

    # add nodes
    for node in node_list:
        nx_obj.add_node(node)

    # add edges
    for i in xrange(0,adj_mat.shape[0]):
        # adjacency matrix is symmetric, so only
        # check upper triangular region for edges
        for j in xrange(i,adj_mat.shape[1]):
            if adj_mat[i,j] == 1:
                nx_obj.add_edge(node_list[i], node_list[j])

    return nx_obj


def calc_raw_comm(adj_mat, p, q):
    raw_comm = 0.0
    
    # avoid division by 0
    # NOTE: correct behavior for singletons?
    if adj_mat.size == 1:
        return 0.0
    else:
        for row_index in np.where(adj_mat[:,0]==1)[0]:
            row_neighbors = adj_mat[row_index,:].sum()-1
            raw_comm = raw_comm + 1.0/ \
                (1.0+p*row_neighbors+(1.0-q)*(adj_mat.shape[0]-row_neighbors-1))
        return raw_comm
