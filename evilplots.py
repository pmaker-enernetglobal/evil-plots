#! /usr/bin/env python3
#
# evilplots.py - a small plotting library for python designed for hybrid power
#   systems
#

# import docopt
import math
import random
import sys
import datetime
import copy

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append('../gridscape-reader')
from gridscapereader import gs_read, gs_names, gs_show, gs

# default plot options
options = {
    'title': 'A title',
    'xlabel': 'Time',
    'ylabel': 'kW',

    'xmin': 0,
    'xmax': 24 * 365,
    'xstep': 24 * 7 * 4,
    'xfmt': lambda t : str(t/24) + 'd',
    
    'ymin': 0,   
    'ymax': 1000,
    'ystep': 100,

    'marker': None,
    
    'figsize': [14, 12],

    'save_plot': False,   # save the plot to  file after each call
    'show_plot': True,    # show the plot after each call
    'show_options': True, # show options for every plot
}

def plot(*args):
    global options
    opts = copy.copy(options)

    for a in args:
        x = np.arange(opts['xmin'], opts['xmax']) 
        if type(a) is str: # just plot it from gridscape
            plt.step(x, gs(a)[opts['xmin']:opts['xmax']],
                     label=a,
                     marker=opts['marker'], markersize=8)
        elif type(a) is dict: # update the options
            opts.update(a)
            print(opts['marker'])
        else: # plot it as a variable
            plt.step(x, a[opts['xmin']:opts['xmax']],
                     label=opts['label'],
                     marker=opts['marker'],
                     markersize=8
            )
    plot_end(opts)

def plot_show():
    plt.show()

def plot_begin():
    global options
    plt.rcParams['figure.figsize'] = options['figsize']
    plt.clf()

def plot_end(opts):
    plt.grid()
    plt.title(opts['title'])
    plt.xlabel(opts['xlabel'])
    xt = range(opts['xmin'], opts['xmax'], opts['xstep'])
    xl = map(opts['xfmt'], xt) 
    plt.xticks(xt, xl)
    plt.ylabel(opts['ylabel'])
    plt.yticks(range(opts['ymin'], opts['ymax'], opts['ystep']))
    # plt.xlim((0, 10))
    # plt.ylim((-5, 5))
    plt.legend(bbox_to_anchor=(1, 1), loc=2, prop={'size':7})

def scatter(x, y):
    plt.grid()
    plt.scatter(gs(x), gs(y), facecolors='none', edgecolors='r')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.xlim(xmin=0)

def scatter_pv():
    plt.scatter(gs('LoadP'), gs('PvSpillP'),
                facecolors='none', edgecolors='r', marker='o',
                label='PvSpillP')
    plt.scatter(gs('LoadP'), gs('PvP'),
                facecolors='none', edgecolors='g', marker='.',
                label='PvP')
    plt.xlabel('LoadP')
    plt.ylabel('PvSpillP, PvP kW')
    plt.title('PV Spill and Output versus Load')
    plt.legend()
    
def date_to_hour(d):
    '''returns the hour for a date'''
    adate = datetime.datetime.strptime(d, "%d-%m-%Y")
    return 24 * adate.timetuple().tm_yday
 
def monthname(m):
    return ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'][m-1]


# user commands for special plots

def plot_typical_day_per_month(v):
    period = 24
    markers =  [None,
                '1', '2', '3', '4',
                '+', 'x', '|', '_',
                '*', 's', 'P', 'x'
                ]
    for m in range(1, 13):
        ts = date_to_hour('15-' + str(m) + '-2000')
        te = ts + period
        plot({'xmax': period,
              'xstep': 1,
              'xfmt': lambda t : str(t) + 'h',
              'label': monthname(m),
              'marker': markers[m],
              'title': 'Typical Days for each month',
        }, gs(v)[ts:te])
    plot_show()

def iteration_scatter(xn, yn, sn=None, title=''):
    xs = []
    ys = []
    ss = []
    sa = []
    if sn == None:
        for size, v, s in zip(gs_names(xn), gs_names(yn)):
            xs.append(gs(size))
            ys.append(gs(v))
            ss.append(6)
            sa.append('')
    else:
        for size, v, s in zip(gs_names(xn), gs_names(yn), gs_names(sn)):
            xs.append(gs(size))
            ys.append(gs(v))
            ss.append(gs(s))
            sa.append(str(int(gs(s))))
        ss = list(map(lambda x : int(20 + 100 * x/max(ss)), ss))
        fig, ax = plt.subplots()
        for i, txt in enumerate(sa):
            ax.annotate(txt, (xs[i], ys[i]), fontsize=7, alpha=0.3)
    plt.scatter(xs, ys, s=ss, facecolor='none', edgecolor='black', alpha=0.5)
    plt.title(title)
    plt.xlabel(xn)
    plt.ylabel(yn)
    plt.legend()
    plot_show()


if __name__ == '__main__':
    gs_read(1467, 4)
    plot_begin()
    print(gs('LoadP'))
    if False:
        plot_typical_day_per_month('LoadP')
    
        plot({'xmin': 0,
              'xmax': 7 * 24,
              'xstep': 24,
              'xfmt': lambda x : str(x/24) + 'd'},
             'PvP', 'PvAvailP')
        scatter('LoadP', 'PvSpillP')
        scatter_pv()
    gs_show()
    iteration_scatter('Gs*PvMaxPPa', 'Gs*SysPpaDpere', 'Gs*EssMaxPPa',
                      title='PV size vs $/kWh')

    # gs_show()
    # print(gs_names('*PvAvailP_mean'))

