#! *_* coding: utf-8 *_*

from matplotlib import pyplot as plt
from scipy.interpolate import interp1d as spline
from scipy.stats import linregress
import numpy as np

# Import the CVS and get all data

fileIn = open('docs/all_data.csv', 'r')

rows = fileIn.read().split('\n')
res_obj = {}

cats = []

for cat in rows[0].split(';'):

    cat = cat.replace('\r','')
    res_obj[cat] = []
    cats.append(cat)

for row in rows[1:]:

    for index, val in enumerate(row.split(';')):

        if val != "":
            res_obj[cats[index]].append(val.replace(',','.'))


def plotDinamicResponse(res_obj):

# Famiglia di curve della risposta dinamica
    x = [float(elem) for elem in res_obj['X']]
    x.reverse()
    x_new = np.linspace(-0.3, 0.3, 100)
    maxs = []

    for key in "1,6/2/2,5/2,8".split("/"):

        y = [float(elem) for elem in res_obj[key]]

        spl = spline(x,y, kind="cubic")
        y_plt = spl(x_new)
        x_plt = x_new[::-1]

        max_y = max(y_plt)
        maxs.append([elem for index, elem in enumerate(x_plt) if  y_plt[index] == max_y][0])


        plt.plot(x_plt, y_plt)

    max_x = sum(maxs) / len(maxs)
    plt.axis([-0.3, 0.3, 0, 80])
    plt.xticks([0.05*k for k in range(-6, 6, 1)])
    plt.xlabel('VDDTest - VRif4', size=18, labelpad=20)
    plt.ylabel('High Light / Low Light', size=18, labelpad=20)
    plt.title('Rapporto Dinamica - Differenza Tensioni', size=22, y=1.05)
    plt.plot([max_x, max_x], [0,100])
    plt.legend(['VDDTest %s V' % tens for tens in "1,6/2/2,5/2,8".split("/")])
    plt.grid()
    plt.show()

colors = ['r', 'g', 'b']

def plotCarateristic(res_obj):

    " We need 3 rows"
    fig, axarr = plt.subplots(2,2)

    fitfunc = lambda p, x: p[0] + p[1] * x   
    errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err

    lightsarr= ['light-ideal', 'light-mixed', 'light-low', 'light-estrapolated']
    row = 0
    col = 0

    for index, light in enumerate(lightsarr):

        # Set the y data (out-1, out-2, out-3)
        y = [float(elem) for elem in res_obj[light]] 

        legend_items = []
        legend_labels = []
        std_labels = []

        for i in range(3):


            print "out-%d" % (i+1)


            x = [float(elem) for elem in res_obj["out-%d" % (i+1)]]

            logx = np.log10(x)
            logy = np.log10(y)

            x_a = np.linspace(logx.min(), logx.max(),1000)

            slope, intercept, r_value, p_value, std_err = linregress(logx, logy)

            subplot, = axarr[row][col].plot(logx, logy, '%so' % colors[i])
            subplot, = axarr[row][col].plot(x_a, fitfunc((intercept, slope), x_a),
                       '%s-' % colors[i])
            legend_items.append(subplot)

            legendString = r"out-{0}: y={1:.02f}x$^{2:0.02f}$".format(i+1, 10**intercept, slope)

            legend_labels.append(legendString)
            std_labels.append(r"out-{0}: std = {1:.05f}".format(i+1, std_err))
            print "%s: out-%d = %f" % (light,i,std_err) 

        axarr[row][col].axis([-2, 2.5, -5, 1.5])
        axarr[row][col].grid()
        legend1 = axarr[row][col].legend(legend_items, std_labels, loc=2)
        axarr[row][col].legend(legend_items, legend_labels, loc=4)
        axarr[row][col].set_title('%s' % light)
        axarr[row][col].add_artist(legend1)

        # Add the column rumber
        col += 1

        if col == 2:
            col = 0
            row += 1

    plt.show()

plotCarateristic(res_obj)
#plotDinamicResponse(res_obj)
