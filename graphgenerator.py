#! *_* coding: utf-8 *_*

from matplotlib import pyplot as plt
from scipy.interpolate import interp1d as spline
import numpy as np

# Import the CVS and get all data

fileIn = open('docs/all_data.tsv', 'r')

rows = fileIn.read().split('\n')
res_obj = {}

cats = []

for cat in rows[0].split('\t'):

    print cat

    res_obj[cat] = []
    cats.append(cat)

for row in rows[1:]:

    for index, val in enumerate(row.split('\t')):

        if val != "":
            res_obj[cats[index]].append(val.replace(',','.'))



# Famiglia di curve della risposta dinamica
x = [float(elem) for elem in res_obj['X']]
x.reverse()
x_new = np.linspace(-0.3, 0.3, 100)
maxs = []

print x
print x_new

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
plt.xticks([0.01*k for k in range(-30, 30, 3)])
plt.plot([max_x, max_x], [0,100])
plt.grid()
plt.show()


