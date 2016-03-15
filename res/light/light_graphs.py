#! *_* coding: utf-8 *_*


from scipy.interpolate import interp1d as interpolate
import numpy as np
from matplotlib import pyplot as plt

"""
Creare grafici di comparazione dei rapporti tra le diverse
luci, per cercare una andamento comune
"""

fileOpen = open("02/out.csv", 'r')

vals = fileOpen.read().split('\n')[:-1]

asset_obj = {}
errors = {}

for elem in range(1,6):

    asset_obj[elem] = []
    errors[elem] = []
    
cursor = 1
error_templates = [1, 0.631, 0.5012, 0.3981, 0.3162, 0.2512]


for index, elem in enumerate(vals):

    if index % 6 == 0 and index != 0:

        cursor += 1

    asset_obj[cursor].append(float(elem.replace(',','.')))
    errors[cursor].append(0)

for elem in asset_obj:

    first = asset_obj[elem][0]

    for index, val in enumerate(asset_obj[elem]):

        asset_obj[elem][index] = val / first
        error_key = index % 6

        perc = abs(val / first - error_templates[error_key]) / (val/first) *100
        errors[elem][index] = perc

        print asset_obj[elem][index]

        """
        print "%d: %f - %f = %f" % (error_key,
                                    asset_obj[elem][index],
                                    error_templates[error_key],
                                    errors[elem][index])
        """
        

# Plot the results

colors = ['#3498db','#1abc9c','#2ecc71','#f1c40f','#e67e22']

fig, ax = plt.subplots()

"""
for i in range(len(colors)):

    y = errors[i+1]
    # Interpolate the curve
    x_new = np.linspace(1,6,100)
    y_interpolated = interpolate(x,y, kind="cubic")(x_new)
    # Plot the data with markers
    plt.plot(x,y,"%so" % colors[i])
    # Plot the interpolated curve
    plt.plot(x_new, y_interpolated, '%s--' % colors[i])

#plt.axis([2.5,4.5,0.4,0.65])
plt.grid()
plt.show()
"""

def setbarvalue(rects):

    for rect in rects:

        height = 1* rect.get_height() + 0.5 
        width = rect.get_x() + rect.get_width()/2
        text = "{0:.01f}%".format(height)

        ax.text(width, height, text, ha='center', va='bottom')


    

width = 0.20
x = np.arange(5)
legend_labels = []
legend_items = []

for i in range(5):

    heights = [errors[index+1][i] for index in range(5)]


    rects = ax.bar(x + width*i, heights, width, color=colors[i])

    # Set the axis' value
    setbarvalue(rects)

    # Set the legend item & label
    legend_items.append(rects)
    legend_labels.append('Lente %f' % error_templates[i])

ax.legend(legend_items, legend_labels)
ax.set_title('Scarto Percentuale tra valori Reali e Ideali', fontsize=25)
ax.set_ylabel('Trasmittanza Reale - Ideale (%)', fontsize=18)
ax.set_xlabel('Filtri Ruota Scura', fontsize=18)
ax.set_xticks(x + 0.18*2.5)
ax.set_xticklabels(["Lente {0:.04f}".format(1/10.0**i) for i in range(0,5)])
ax.set_yticks(range(0,51,5))
plt.grid()
plt.axis([0,5,0,35])
plt.show()
        

