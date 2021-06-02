import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

#fnm = "test.dat"
#df = pd.read_csv(fnm,delim_whitespace=True,index_col=0,header=None)
#print(df)
#
#fig, ax = plt.subplots(1,1)
##ax2 = ax.twinx()
##df[[1]].plot(ax=ax)
##df[[2]].plot(ax=ax2,c='r')
#ax.plot(df[[1]],df[[2]],ls='',marker='.',mew=0)
##ax2 = ax.twinx()
##df[[1]].plot(ax=ax)
##df[[2]].plot(ax=ax,c='r')

x = np.linspace(-10.,35.,100)
y = np.linspace(0,100,100)

X,Y = np.meshgrid(x,y)

b = 0.2
radup = 107.0
radup = 5.67e-8*(X+273.15)**4
rl = (b + (1-b)*(Y/100.))*(radup - X)
#rl = 207.0 + 2.17*X

#im = plt.pcolormesh(X,Y,rl)
#plt.colorbar(im)
#plt.xlabel("temperature")
#plt.ylabel("sunshine")

lat = np.linspace(-90,90,181)
obl = -23.4
day = np.arange(1,366)
LAT, DAY = np.meshgrid(lat,day)
aa = np.radians(obl)*np.cos(np.pi/180.*360.*(DAY+10.)/365)

u = np.sin(np.radians(LAT))*np.sin(aa)
v = np.cos(np.radians(LAT))*np.cos(aa)

w = np.tan(np.radians(LAT))*np.tan(aa)

ho = np.arccos(-w)
ho = np.where(w>1,np.pi,ho)
ho = np.where(w<-1,0,ho)

#ho = np.zeros(LAT.shape)
#ho = np.where(u>=v,2.*np.pi,ho)
#ho = np.where(np.logical_and(u>-v,u<v),np.arccos(-u/v),ho)
#ho = np.where(u<=-v,0.0,ho)
print(ho.min(),ho.max())

ho *= 12./np.pi
print(ho.min(),ho.max())

qo = 3600.*1360.*(1.+2.*0.01675*np.cos(2*np.pi*DAY/365))/86400.

zz = u*ho + v*(12./np.pi)*np.sin(np.pi/12.*ho)

#im = plt.pcolormesh(DAY,LAT,ho,vmin=0,vmax=2.*np.pi)
#im = plt.pcolormesh(DAY,LAT,2*qo*zz)
#plt.colorbar(im)
#plt.show()
#sys.exit()

fig, ax = plt.subplots(2,3,sharex=True,sharey=True,figsize=(10,4))
ax = ax.flatten()

ins_new = np.loadtxt("insolation_new.dat") # kJ/day
ins_new /= 86.4 # kJ/day -> W/m2

print(x.shape)
lat = np.linspace(-90,90,ins_new.shape[0])
day = np.linspace(1,365,ins_new.shape[1])
DAY, LAT = np.meshgrid(day,lat)

im = ax[0].pcolormesh(DAY,LAT,ins_new,vmin=0,vmax=550,shading="nearest",rasterized=True)
ax[0].contour(DAY,LAT,ins_new,levels=np.arange(0,551,50),colors='k',linewidths=0.5)
plt.colorbar(im,ax=ax[0],label="W/m$^2$")
ax[0].set_title("new")

ins_old = np.loadtxt("insolation_old.dat")
ins_old /= np.pi
im = ax[1].pcolormesh(DAY,LAT,ins_old,vmin=0,vmax=550,shading="nearest",rasterized=True)
ax[1].contour(DAY,LAT,ins_old,levels=np.arange(0,551,50),colors='k',linewidths=0.5)
plt.colorbar(im,ax=ax[1],label="W/m$^2$")
ax[1].set_title("old")

ins_diff = ins_new-ins_old
print(ins_diff.min(),ins_diff.max())
im = ax[2].pcolormesh(DAY,LAT,ins_diff,vmin=-30,vmax=30,shading="nearest",cmap='RdBu_r',rasterized=True)
ax[2].contour(DAY,LAT,ins_diff,levels=np.arange(-30,31,5),colors='k',linewidths=0.5)
plt.colorbar(im,ax=ax[2],label="W/m$^2$")
ax[2].set_title("new - old")

ho_new = np.loadtxt("ho_new.dat")
im = ax[3].pcolormesh(DAY,LAT,ho_new,vmin=0,vmax=24,shading="nearest",rasterized=True)
ax[3].contour(DAY,LAT,ho_new,levels=[15,18,21,24],colors='k',linewidths=0.5)
ax[3].contour(DAY,LAT,ho_new,levels=[0,3,6,9],colors='k',linestyles='--',linewidths=0.5)
plt.colorbar(im,ax=ax[3],label="hours")
ax[3].set_title("new")

ho_old = np.loadtxt("ho_old.dat")
im = ax[4].pcolormesh(DAY,LAT,ho_old,vmin=0,vmax=24,shading="nearest",rasterized=True)
ax[4].contour(DAY,LAT,ho_old,levels=[15,18,21,24],colors='k',linewidths=0.5)
ax[4].contour(DAY,LAT,ho_old,levels=[0,3,6,9],colors='k',linestyles='--',linewidths=0.5)
plt.colorbar(im,ax=ax[4],label="hours")
ax[4].set_title("old")

ho_diff = ho_new-ho_old
print(ho_diff.min(),ho_diff.max())
im = ax[5].pcolormesh(DAY,LAT,ho_diff,vmin=-2,vmax=2,shading="nearest",cmap='RdBu_r',rasterized=True)
ax[5].contour(DAY,LAT,ho_diff,levels=[-2,-1,-0.5,0.5,1,2],colors='k',linewidths=0.5)
plt.colorbar(im,ax=ax[5],label="hours")
ax[5].set_title("new - old")

# axis labels
ax[3].set_xlabel("day")
ax[4].set_xlabel("day")
ax[5].set_xlabel("day")
ax[0].set_ylabel("lat")
ax[3].set_ylabel("lat")

fig.savefig('biome4_insolation.pdf',dpi=300, bbox_inches='tight', pad_inches = 0.01)

plt.show()
