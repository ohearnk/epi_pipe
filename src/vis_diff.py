import csv
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import random as rand

def diff_plot(density,raw_comm,color,ego_id,out_file_base):
    if len(density) != len(raw_comm):
        return

    for i in xrange(len(density)):
        # create a figure with size 6 x 6 inches
        fig = Figure(figsize=(6,6))

        # create a canvas and add figure
        canvas = FigureCanvas(fig)

        # create a subplot
        ax = fig.add_subplot(111)

        # set title
        ax.set_title('RawComm vs. Density, Ego ID ' \
            +str(ego_id)+', Time Period '+str(i+1)+'\n',fontsize=14)

        # set x-axis label
        ax.set_xlabel('RawComm',fontsize=12)

        # set y-axis label
        ax.set_ylabel('Density',fontsize=12)

        # display grid
        ax.grid(True,linestyle='-',color='0.75')

        # generate scatter plot
        if i > 0:
            ax.scatter(raw_comm[:i],density[:i],color=color[0]);
        ax.scatter(raw_comm[i],density[i],color=color[1]);

        # 10 time steps
        for j in xrange(0,i):
            if j < i-1:
                ax.arrow(raw_comm[j], density[j],
                    raw_comm[j+1]-raw_comm[j],
                    density[j+1]-density[j], color=color[0])
            else:
                ax.arrow(raw_comm[j], density[j],
                    raw_comm[j+1]-raw_comm[j],
                    density[j+1]-density[j], color=color[1])
#            head_width=0.05, head_length=0.05)
#            length_includes_head=True)

        # Set the axis
        ax.set_xlim([int(min(raw_comm)),int(max(raw_comm))+1])
        ax.set_ylim([round(min(density),2)-0.05,round(max(density),2)+0.05])

        # save the scatter plot to a PDF file
        canvas.print_figure(out_file_base+'_'+str(i)+'.pdf',dpi=500)


def read_csv(FILE):
    density = [ ]
    raw_comm = [ ]

    # create CSV reader
    with open(FILE, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',',
            quotechar='|')
        # skip header
        reader.next()
        for RECORD in reader:
            density.append(float(RECORD[0]))
            raw_comm.append(float(RECORD[1]))

    return density, raw_comm


##### main #####
in_file = 'high_avg_raw_comm3.csv'
out_file_base = 'high_avg_raw_comm3'
ego_id = 9627

density, raw_comm = read_csv(in_file)

for i in xrange(0,len(density)/10):
    color = ['blue', 'tomato']
    diff_plot(density[i*10:(i+1)*10], 
        raw_comm[i*10:(i+1)*10],
        color, ego_id,
        out_file_base)
