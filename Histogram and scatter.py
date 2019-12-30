# Written by Berker Bahceci, October 2019
# Sanofi CI2C Turkey
# CRIF score visualization
# Non-interactive

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.text
import numpy as np
from scipy.interpolate import interp1d

# Data
scores = pd.read_excel('crif_scores.xlsx')
scores.dropna(inplace = True)
mean = scores.iloc[:,1].mean()
std = scores.iloc[:,1].std()
data = scores.iloc[:,1]

# Main
fig, (ax2, ax1) = plt.subplots(2, figsize=(12,10), sharex=True)
counts, bins, patches = ax1.hist(data, facecolor='royalblue', edgecolor='black')

# Labels
ax1.set_xlabel('CRIF scores')
ax1.set_ylabel('Number of customers in the range')
ax1.set_title("Distribution of customer's CRIF scores")
ax1.set_xticks(bins)
ax1.xaxis.grid(True, linestyle = '--')


# Bins
bin_x_centers = 0.5 * np.diff(bins) + bins[:-1]
bin_y_centers = ax1.get_yticks()[1] * 0.25
for i in range(len(bins)-1):
    bin_label = "%d customers" %counts[i]
    plt.text(bin_x_centers[i], bin_y_centers, bin_label, rotation=90, rotation_mode='anchor')

# Color code
perc_25_colour = 'crimson'
perc_50_colour = 'royalblue'
perc_75_colour = 'goldenrod'
perc_95_colour = 'peachpuff'

for patch, leftside, rightside in zip(patches, bins[:-1], bins[1:]):
    if rightside < mean-std:
        patch.set_facecolor(perc_25_colour)
    elif leftside > mean+2*std:
        patch.set_facecolor(perc_95_colour)
    elif leftside > mean+std:
        patch.set_facecolor(perc_75_colour)

# Legend
handles = [Rectangle((0,0),1,1,color=c,ec="k") for c in [perc_25_colour, perc_50_colour, perc_75_colour, perc_95_colour]]
labels= ["< \u03BC - \u03C3","Within \u03BC +/- \u03C3", "> \u03BC + \u03C3", "> \u03BC + 2*\u03C3"]
plt.legend(handles, labels, bbox_to_anchor=(0.5, 0., 0.70, 0.98))

# Annotate mean and standard deviation
ax1.annotate('Mean is \u03BC = %.1f \nStandard deviation is \u03C3 = %.1f' %(mean, std),
            xy=(.91,.20), xycoords='figure fraction',
            horizontalalignment='left', verticalalignment='center',
            fontsize=10, bbox=dict(boxstyle="round", fc="white"),
            rotation=90)


##############################################################################
# Scatter

scores['Bins'] = np.digitize(data, bins)
risk = scores.copy().reset_index()
risk.drop(['index', 'Company Name', '2018 finar score'], axis = 1, inplace=True)
for i in range(len(risk)):
    if risk.loc[i, 'Bins'] == 11:
        risk.loc[i, 'Bins'] = 10

risk2 = risk.groupby('Bins').sum() #This should sum the risks for each bin.

ax2.set_title('Risk distribution with respect to CRIF scores')
ax2.set_xlabel('CRIF scores')
ax2.set_ylabel('Total risk (in TRY)', color='black')  # we already handled the x-label with ax1
ax2.scatter(bin_x_centers, risk2, c='black', marker="X", s=100, alpha=0.5)
ax2.tick_params(axis='y', labelcolor='black')
ax2.ticklabel_format(style='plain')
ax2.grid(True, linestyle = '--')

x_new = np.linspace(bin_x_centers.min(), bin_x_centers.max(), 500)
risk2_arr = risk2.iloc[:,0].values
degree = len(bins)-1
f = interp1d(bin_x_centers, risk2_arr)
smooth = f(x_new)

ax2.plot(x_new, smooth)

fig.tight_layout()
plt.show()

"""




##############################################################################
plt.show()
fig.savefig('CRIF histogram.jpg', bbox_inches = "tight")

###############################################################################
# Summing the risks
scores['Bins'] = np.digitize(data, bins)
grouped_scores = scores.groupby(['Bins'])
