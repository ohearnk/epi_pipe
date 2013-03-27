import argparse
import csv
import glob
import networkx as nx
import numpy as np
import pygraphviz as pgv
from texttable import Texttable

import preprocessing


NUM_FILES=10

IN_FILES=[ '/opt2/D4D/data/SET4/raw/tsv/GRAPHS_'+str(i)+'.TSV' \
    for i in xrange(0,NUM_FILES) ]
OUT_FILES_BASE=[ 'set4_t'+str(i)+'_id' \
    for i in xrange(0,10) ]
ADJ_MAT_OUT_FILES=[ 'set4_t'+str(i)+'_adj_mat.txt'
    for i in xrange(0,NUM_FILES) ]

#ADJ_MAT_FILES = glob.glob('/opt2/D4D/data/SET4/adj_matrices/2hop/*')

# create command-line argument parser object
parser = argparse.ArgumentParser()

# add accepted positional arguments

# add accepted optional arguments
parser.add_argument("-v", "--verbosity", action='count',
                    help="increase output verbosity")
parser.add_argument("--create_2hop_graphs", 
                    metavar='BASE_DIR', nargs=1, type=str, 
                    default=None,
                    help="generate PDFs of 2-hop network graphs using PyGraphviz")
parser.add_argument("--get_stats", 
                    action='store_true', 
                    help="analyze network graphs for a variety of statistics"+
                        " (e.g., node count, ego degree, density)")

# parse arguments
args = parser.parse_args()

####### NEED TO UPDATE #######
#for i in xrange(0,len(IN_FILES)):
    # create a file pointer
    #fp = open(IN_FILES[i], 'r')

    # create NetworkX graph object
    #nx_obj = tsv_to_nx(fp)

    # create PyGraphviz graph object
    #pgv_obj = tsv_to_pgv(fp)

    # generate graph
    #print 'Generating visualization for '+IN_FILES[i]+'...'
    #draw_pgv('set4_t'+str(i)+'.pdf')
    #print 'Done!'

    
    # convert PyGraphviz object to NetworkX object
    #nx_obj = nx.from_agraph(pgv_obj)

    # generate adjacency list from NetworkX object
    #adj_list = nx_to_adj_list(nx_obj)

    # write adjacency list to file
    #print 'Generating adjacency lists for '+IN_FILES[i]+'...'
    #write_adj_list('set4_t'+str(i), adj_list)
    #print 'Done!'

    # create adjacency matrix
    #node_list, adj_mat = nx_to_adj_mat(nx_obj)

    # write out adjacency matrix and node list
    #write_adj_mat(node_list, adj_mat, ADJ_MAT_OUT_FILES[i])

    #write_gml_format(nx_obj, 'set4_t'+str(i)+'.gml')

    # generate dictionary of all links in 1 hop network around ego
    #one_hop_adj_dict = create_1hop_adj_list(fp_in)

    # create a file pointer for ego adjacency lists
    #fp_out = open(OUT_FILES[i], 'w')

    # write the adjacency lists
    #write_1hop_adj_list(one_hop_adj_dict, fp_out)

    #write_1hop_adj_matrix(one_hop_adj_dict, OUT_FILES2_BASE[i])

    # convert NetworkX graph object to a dictionary of dictionaries
    # representing adjacency info.
    #adj_dict = nx.to_dict_of_dicts(nx_obj)

    # write out adjacency matrices for the 2-hop network for each ego
    #write_2hop_adj_matrix(adj_dict, OUT_FILES_BASE[i])

    # close file pointer
    #fp.close

# create 2-hop network graphs using PyGraphviz
if args.create_2hop_graphs != None:
    base_dir = args.create_2hop_graphs
    adj_mat_files = glob.glob(base_dir+'/*')

    for FILE in adj_mat_files:
        # read in adjacency matrix and node list
        adj_mat, node_list = load_adj_mat(FILE)
        
        # convert it to a PyGraphviz
        # graph object for drawing
        pgv_obj = adj_mat_to_pgv(adj_mat, node_list)
        # create output filename
        out_file = FILE.replace(base_dir+'/', '')
        out_file = out_file.replace('_2hop_adj_mat.txt', '.pdf')

        # draw graph
        draw_pgv(pgv_obj, out_file)    

# generate stats using NetworkX
if args.get_stats:
    # base directories of 1- and 2-hop adjacency matrices
    oh_base_dir = '/opt2/D4D/data/SET4/adj_matrices/1hop'
    th_base_dir = '/opt2/D4D/data/SET4/adj_matrices/2hop'

    # for each of the ten time periods
    for i in xrange(0,10):
        # get a list of all the adjacency matrices to read in
        oh_adj_mat_files = glob.glob(oh_base_dir+'/set4_t'+str(i)+'_*')
        th_adj_mat_files = glob.glob(th_base_dir+'/set4_t'+str(i)+'_*')

        # sort
        oh_adj_mat_files.sort()
        th_adj_mat_files.sort()

        # for testing, trim to 100 files
        #oh_adj_mat_files = oh_adj_mat_files[0:100]
        #th_adj_mat_files = th_adj_mat_files[0:100]
 
        # quick error check 
        if len(oh_adj_mat_files) != len(th_adj_mat_files):
            print 'ERROR: not the same # of 1- and 2-hop', \
                ' adjacency matrix files.'
            break
 
        # list to hold stats for each graph
        records = [ ]

        # create CSV writer
        

        # read in the adjacency matrices, calculate stats
        for FILES in zip(oh_adj_mat_files, th_adj_mat_files):
            # read in 1-hop adjacency matrix and node list
            oh_adj_mat, oh_node_list = load_adj_mat(FILES[0])
            # read in 2-hop adjacency matrix and node list
            th_adj_mat, th_node_list = load_adj_mat(FILES[1])

            # convert it to NetworkX graph objects
            oh_nx_obj = adj_mat_to_nx(oh_adj_mat, oh_node_list)
            th_nx_obj = adj_mat_to_nx(th_adj_mat, th_node_list)

            # get graph density
            # Note: singletones return 0.0
            oh_density = nx.density(oh_nx_obj)
            th_density = nx.density(th_nx_obj)
            # get node count
            oh_node_count = len(oh_node_list)
            th_node_count = len(th_node_list)
            # get ego degree
            # Note: ego should be the smallest (leftmost)
            # node in sorted node list 
            ego_degree = nx.degree(oh_nx_obj, oh_node_list[0])
     
            # compute the number of triangles
            oh_triangles = 0
            for node in oh_nx_obj.nodes():
                oh_triangles = oh_triangles + nx.triangles(oh_nx_obj, node)
            oh_triangles = oh_triangles / 3
            
            th_triangles = 0
            for node in th_nx_obj.nodes():
                th_triangles = th_triangles + nx.triangles(th_nx_obj, node)
            th_triangles = th_triangles / 3
 
            # code for rawComm
            oh_raw_comm = calc_raw_comm(oh_adj_mat, 1.0, 1.0)
            
            # TODO 
            # # of new friends, 
            # # of lost friends
            # of closed triangles, ...

            # time period, ego ID, ego degree, 1-hop node count, 2-hop node count, 
            # 1-hop # triangles, 2-hop # triangles, 1-hop density, 
            # 2-hop density, 1-hop rawComm
            records.append([i, oh_node_list[0], ego_degree, oh_node_count, 
                th_node_count, oh_triangles, th_triangles, oh_density, 
                th_density, oh_raw_comm])

            # sort by ego ID
            records.sort()

        # create a texttable and add the records
        table = Texttable()
        # set the table style
        table.set_deco(Texttable.HEADER)
        # set column data types in table
        table.set_cols_dtype(['i','i','i','i','i','i','i','f','f','f'])
        # set the table column alignment
        table.set_cols_align(['r','r','r','r','r','r','r','r','r','r'])
        # add table column headers
        header = ['Time Period','Ego ID','Ego Degree','1-Hop Node Count',
            '2-Hop Node Count','1-Hop Triangle Count',
            '2-Hop Triangle Count','1-Hop Density','2-Hop Density',
            '1-Hop RawComm']
        table.header(header)

        # add the records to the table
        if i == 0:
            for RECORD in records:
                table.add_row(RECORD)

        # draw table
#        print "Time Period:",str(i)
#        print table.draw()
#        print

        # create CSV writer
        with open('set4.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(header)
            for RECORD in records:
                writer.writerow(RECORD)
