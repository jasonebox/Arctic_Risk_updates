#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 06:43:05 2022

@author: jason

http://psc.apl.uw.edu/research/projects/arctic-sea-ice-volume-anomaly/data/


"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import stats
from numpy.polynomial.polynomial import polyfit
from scipy import stats
from scipy.interpolate import interp1d
from matplotlib.ticker import FormatStrFormatter
import matplotlib as mpl

font_size=12
th=1
plt.style.use('default')
# plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams["font.size"] = font_size 
plt.rcParams["mathtext.default"]='regular'
plt.rcParams['axes.grid'] = False
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.linewidth'] = th/2.

if os.getlogin() == 'jason':
    base_path = '/Users/jason/Dropbox/Arctic_Risk_monthly/'

os.chdir(base_path)

# # gather daily data
# os.system('curl http://psc.apl.uw.edu/wordpress/wp-content/uploads/schweiger/ice_volume/PIOMAS.vol.daily.1979.2022.Current.v2.1.dat.gz > ./raw_data/PIOMAS.vol.daily.1979.2022.Current.v2.1.dat.gz')
# os.system('gunzip ./raw_data/PIOMAS.vol.daily.1979.2022.Current.v2.1.dat.gz')
# os.system('mv ./raw_data/PIOMAS.vol.daily.1979.2022.Current.v2.1.dat ./raw_data/PIOMAS.vol.daily.1979.2022.Current.v2.1.csv')

# gather monthly data
gather=0
if gather:os.system('curl http://psc.apl.uw.edu/wordpress/wp-content/uploads/schweiger/ice_volume/PIOMAS.monthly.Current.v2.1.csv > ./raw_data/PIOMAS.monthly.Current.v2.1.csv')


# df = pd.read_csv('./raw_data/PIOMAS.vol.daily.1979.2022.Current.v2.1.csv',header=None,skiprows=1)
df = pd.read_csv('./raw_data/PIOMAS.monthly.Current.v2.1.csv')


fs=10 # land ice

# fig, ax = plt.subplots(figsize=(7.5, 6.5))
fig, ax = plt.subplots()

figsubpath='SIV' ; source='PIOMAS'
region='Arctic'
print(df)

fyear=int(df.year.values[-1])
iyear=1979 ; nyears=fyear-iyear+1

SIV=[]
x=[]

for yy in range(nyears):
    for mm in range (12):
        print(yy,mm,df.iloc[yy,mm+1])
        SIV.append(df.iloc[yy,mm+1])
        x.append(yy+iyear+(mm/12))

x=np.array(x)
y=np.array(SIV)
y[y<0]=np.nan

y*=1000

ylab='Arctic sea ice volume, x 1,000 $km^{3}$'
ylab='cubic kilometers'

v=np.where(np.isfinite(y))
# v=np.where((y>=)&(np.isfinite(y)))1

ax.set_title('Arctic Sea Ice Volume '+str(iyear)+' to '+str(fyear))
ax.plot(x[v[0]], y[v[0]],'-',c=(0.0, 0.2, 0.7),label=lab)

coefs=stats.pearsonr(x[v[0]],y[v[0]])
b, m = polyfit(x[v[0]],y[v[0]], 1)

ax.plot(x[v[0]], b + m * x[v[0]], '--',c=(1., 0., 0.0))
ax.set_ylabel(ylab,fontsize=fs)

confidencex=str("%8.3f"%(1-coefs[1])).lstrip()
if confidencex=='1.000':confidencex='>0.999'
ny=len(v[0])    
mult=0.79
xx0=0.04 ; yy0=0.15
units=' M $km^{2}$'
ny=len(x[v[0]])
# change=m*ny/np.mean(y[v[0]])*100.
xx0=m*x[v[0][0]]+b
xx1=m*x[v[0][-1]]+b
change=(xx1-xx0)/xx0*100.
ax.set_xlim(iyear-1,fyear+1-0.1)

xticksx=np.arange(min(x[v[0]]), max(x[v[0]])+1, 2)-1

ax.set_xticks(xticksx)

yticksx=np.arange(0,33.5,5)*1000
ax.set_ylim(0,33500)

ax.set_yticks(yticksx,
            # rotation=45,
            fontsize=fs,
            rotation_mode="anchor",ha='right')

ax.set_xticklabels(xticksx.astype(int),rotation=45,
            fontsize=fs,
            rotation_mode="anchor",ha='right')

ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

props = dict(boxstyle='round', facecolor='w', alpha=0.5,edgecolor='grey')

mult=0.9
xx0=0.03 ; yy0=0.22

c0=0.4
color=[c0,c0,c0]

ax.text(xx0,yy0, '%.0f'%nyears+' years\n'
        # +'time correlation: %.3f'%coefs[0]+'\n'
        +'loss rate: %.0f'%-m+' $km^{3}$ per year\n'
        # +'confidence: '+confidencex+'\n'
        +'change over period of record: %.1f' % change+'%'
        ,transform=ax.transAxes, fontsize=fs*mult,
        verticalalignment='top', bbox=props,rotation=0,color=color, rotation_mode="anchor")  

mult=1.2
# ax.text(0.78,0.04, '@Climate_Ice', transform=ax.transAxes,
# ax.text(0.77,0.04, '@AMAP_Arctic', transform=ax.transAxes,
ax.text(0.72,0.07, 'arcticrisk.org', transform=ax.transAxes,
        fontsize=font_size*mult,verticalalignment='top',color='maroon', rotation_mode="anchor")

mult=0.85
xx0=0.02
ax.text(xx0,0.05, 'data after Schweiger et al 2011, Zhang et al 2003',transform=ax.transAxes, fontsize=fs*mult,
        verticalalignment='top',rotation=0,color=color, rotation_mode="anchor")  

ly='p'

if ly=='x':plt.show()

figname='sea_ice_volume'

fig_path='./Figs/'

if ly=='p':
    # 1200 pixels wide x 675 is optimal for Twitter 16:9 aspect ratio
    my_dpi=300
    plt.savefig(fig_path+figname+'.png', bbox_inches='tight',figsize=(1200/my_dpi, 675/my_dpi), dpi=my_dpi)
    # os.system('open '+fig_path+figname+'.png')