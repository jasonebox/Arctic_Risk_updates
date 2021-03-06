#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 06:43:05 2022

@author: jason


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
    base_path = '/Users/jason/Dropbox/Arctic Risk/Arctic_Risk_updates/'

os.chdir(base_path)

# df = pd.read_csv('./raw_data/PIOMAS.vol.daily.1979.2022.Current.v2.1.csv',header=None,skiprows=1)
df = pd.read_csv('./raw_data/GOA_1971-2021.csv')
print(df)

def trendline(cc,x,y,color,lab,units,do_trendline):
    v=np.where(np.isfinite(y))
    ax.plot(x[v[0]], y[v[0]],'-o',c=color,linewidth=2,label=lab)
    coefs=stats.pearsonr(x[v[0]],y[v[0]])
    # b, m = polyfit(x[v[0]],y[v[0]], 1)
    if do_trendline:
        v=np.where((x>=2003)&(np.isfinite(y)))
        # ax.plot(x[v[0]], b + m * x[v[0]], '--',c=color)
    #     v=np.where(x>i_year_graphic)
        b, m = polyfit(x[v[0]],y[v[0]], 1)
        ny=x[v[0][-1]]-x[v[0][0]]
        change=m
        increase_or='increase'
        if m<0:increase_or='decrease'
        units='Gigatons per year'
        ax.plot(x[v[0]], b + m * x[v[0]], '--',c='r',label=increase_or+': '+"%.0f" %change+' '+units+'\nsince 2003')

# fig, ax = plt.subplots(figsize=(7.5, 6.5))
fig, ax = plt.subplots()


fyear=int(df.year.values[-1])
iyear=1971 ; nyears=fyear-iyear+1

df['Total']= df.iloc[:, 2:].sum(axis=1)
print(df.columns)

dM=df['Total'][df.year==2021].values-df['Total'][df.year==2003].values
dM=-dM[0]/362

print('sea level contribution since 2003: '+"%.0f" %dM+' mm eustatic, i.e. without thermal expansion')
print('or '+"%.0f" %(dM*1.4)+' mm with +40% thermal expansion')

cc=0

x = df.year
y=df['Total']
ax.set_title('Arctic Glaciers '+str(iyear)+' to '+str(fyear))
ax.axhline(y=0,linestyle='--',linewidth=th*1.5, color='grey')
trendline(cc,x,df['Arctic-Canada'],'k','Arctic-Canada','',do_trendline=0)
trendline(cc,x,df['Alaska'],'cadetblue','Alaska','',do_trendline=0)
trendline(cc,x,df['Greenland'],'g','Greenland','',do_trendline=0)
trendline(cc,x,y,'b','all Arctic land ice','',do_trendline=1)

fg='k'
ax.set_ylabel("cubic kilometers", color=fg)
# ax.set_ylim(np.nanmin(y)*0.99,np.nanmax(y)*1.01)     
# ax.set_ylim(0,np.nanmax(y)*1.01)     
ax.get_xaxis().set_visible(True)
mult=0.8
ax.legend(loc='center left',prop={"size": font_size * mult})
ax.set_xlim(1970,2022)

ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

ax2 = ax.twinx()
# ax2.plot(df.year,df['Total']/-362,'-o',c='b',label='mm sea level rise')
ax2.set_ylabel("mm sea level\nequivalent", color=fg)
ax2.set_ylim(31*1.4,0)
ax2.spines['right'].set_color('k')
ax2.yaxis.label.set_color('k')
ax2.tick_params(axis='y', colors='k')
ax2.grid(False)


print((df['Total'][50]-df['Total'][49])*1e9/(365*86400))


for i in range(cc):
    ax[i].spines['left'].set_color(fg)
    ax[i].spines['right'].set_color(fg)
    ax[i].tick_params(color=fg, labelcolor=fg)

mult=1.2
ax.text(0.66,0.07, 'arcticrisk.org', transform=ax.transAxes,
        fontsize=font_size*mult,verticalalignment='top',color='maroon', rotation_mode="anchor")

mult=0.85
xx0=0.02
# world glacier monitoring service
ax.text(xx0,0.2, 'Greenland data: Mankoff et al 2021\nother Arctic glacier data: Box et al 2018 and WGMS.ch',transform=ax.transAxes, fontsize=font_size*mult,
        verticalalignment='top',rotation=0,color=color, rotation_mode="anchor")  

ly='p'

if ly=='x':plt.show()

figname='glaciers'

fig_path='./Figs/'

if ly=='p':
    # 1200 pixels wide x 675 is optimal for Twitter 16:9 aspect ratio
    my_dpi=300
    plt.savefig(fig_path+figname+'_'+str(my_dpi)+'dpi.png', bbox_inches='tight',figsize=(1200/my_dpi, 675/my_dpi), dpi=my_dpi)
    my_dpi=144
    plt.savefig(fig_path+figname+'_'+str(my_dpi)+'dpi.png', bbox_inches='tight',figsize=(1200/my_dpi, 675/my_dpi), dpi=my_dpi)
    plt.savefig(fig_path+figname+'.eps', bbox_inches='tight')
    # os.system('open '+fig_path+figname+'.png')