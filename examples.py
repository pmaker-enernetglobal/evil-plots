#! /usr/bin/env python3
#
# examples.py - just some plot examples as prototypes for a bwginning
#

import docopt
import math
import random
import sys
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# import bokeh
# import seaborn as sns
# sns.set()

#
# test data generation
#

When = np.arange(24 * 365)

    
def plot(name, var, period=24, site='Somewhere'):
    plt.rcParams['figure.figsize'] = [14, 12]
    plt.clf()
    plt.grid()
    plt.title(site + ' ' + name + ' ' + 'for the 15th of each month', fontsize=16)
    plt.xlabel('Time of day in hours')
    plt.xlim(left=0, right=period-1)
    
    l = []
    lv = []
    for h in range(24):
        lv.append(h)
        l.append(str(h) + 'h')
    plt.xticks(lv, l)

    plt.ylabel('System Load kW')
    pmax = 1000
    plt.ylim(bottom=0, top=pmax)
    l = []
    lv = []
    for p in range(0, pmax, 100):
        lv.append(p)
        l.append(str(p))
    if pmax != lv[-1]:
        lv.append(pmax)
        l.append(str(pmax))
    plt.yticks(lv, l)
    return None
    
def ts(var, lb, mk, st, len):
    global When
    x = When[st:st + len] - st
    y = var[st:st + len]
    plt.step(x, y, label=lb, marker=mk, markersize=4, alpha=0.5)

def display():
    if True:
        plt.legend(bbox_to_anchor=(1, 1), loc=2, prop={'size':12})
    else:
        plt.legend()
    plt.show()

def date_to_day(d):
    '''returns the day of year (0..366) from a date such as 2-3-2016

    >>> assert date_to_day('01-01-2016') == 1
    >>> assert date_to_day('05-01-2016') == 5
    '''
    adate = datetime.datetime.strptime(d, "%d-%m-%Y")
    return adate.timetuple().tm_yday

def monthname(m):
    return ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'][m-1]
#

def readjob(job=1557, iter=0, col='Total Load [kW]'):
    fn = '~/Downloads/job-' + str(job) + '-results/results/annual_hourly_ops_iteration_' + str(iter) + '.csv'
    df = pd.read_csv(fn)
    # print(df.info())
    return df[col]

# these are the user level functions

def typical_days(name, var, dl=None):
    '''plot period data sampled every timestamp'''
    if dl == None:
        dl = []
        dn = []
        for m in range(1,13,1):
            dl.append(date_to_day('15-' + str(m) + '-2000'))
            dn.append(monthname(m))
    plot(name, var, 24)
    for d, n in zip(dl, dn):
        ds = str(d) + 'd'
        ts(var, n, '*', d * 24, 24)
    display()
    return None


# weekly consumption: x=power, y=24h, lines=Monday,...Sunday or lines=1 day from each month


if __name__ == '__main__':
    LoadP = readjob(col='Total Load [kW]')
    PvP = readjob(col='Total Solar Core [kW]')
    PvSpillP = readjob(col='Total Solar Slack [kW]')
    GenP = readjob(col='All Generators [kW]')
    typical_days('LoadP')

    

    
    
