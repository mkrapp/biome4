import netCDF4 as nc4
from Biome4 import biome4
import numpy as np
import matplotlib.pyplot as plt
import sys

fnm = sys.argv[1]
fnm_lsm = sys.argv[2]

# read netcdf
nc = nc4.Dataset(fnm,'r')
df = {}
var_names = ['lon', 'lat', 'solar_mm_s3_srf', 'totCloud_mm_ua', 'downSol_mm_TOA', 'longwave_mm_s3_srf', 'temp_mm_srf']
for v in var_names:
    df[v] = np.array(nc.variables[v][:]).squeeze()
nc.close()

print df['lat'].shape
print df['solar_mm_s3_srf'].shape

# Read land sea mask
nc = nc4.Dataset(fnm_lsm,'r')
lsm = np.array(nc.variables['lsm'][:]).squeeze()
nc.close()


#temp = df['temp_mm_srf'][::12,0,20]-273.15
#plt.plot(temp,'kx-')
#plt.grid()

is_land = False
while not is_land:
    i = np.random.randint(0,95)
    j = np.random.randint(0,72)
    if lsm[j,i] == 1.0:
        is_land = True

t = np.random.randint(0,61)
t = 61
cc = df['totCloud_mm_ua'][t*12:t*12+12,j,i]*100.
print cc
temp = df['temp_mm_srf'][t*12:t*12+12,j,i]-273.15
lws = df['longwave_mm_s3_srf'][t*12:t*12+12,j,i]
sws = df['solar_mm_s3_srf'][t*12:t*12+12,j,i]
swt = df['downSol_mm_TOA'][t*12:t*12+12,j,i]
lat = df['lat'][j]

print biome4.ppeett.__doc__

res = biome4.ppeett(lat,100.-cc,temp,sws,lws)
print 'rad0', res.rad0

f = plt.figure(figsize=(8,8))

time = np.arange(365)/(365./12.)
time2 = np.arange(0.5,12.5)
ax = plt.subplot(211)
ax.plot(time,res.dpet,'k-',label='PET (standard)')
ax.plot(time,res.dpet_direct,'k--',label='PET (direct SW/LW)')
ax.set_ylabel('potential evapotranspiration (in mm/day)')
plt.legend(loc=2,framealpha=0.5,fontsize=12)
ax2 = ax.twinx()
ax2.plot(time,res.drl,'g-',label='LW (net SRF)')
ax2.plot(time2,-lws,'gx-')
ax2.plot(time2,swt,ls='-',marker='x',c='purple')
ax2.plot(time,res.drs_t,ls='-',c='purple',label='SW (in TOA)')
ax2.plot(time,res.drs_s,'r-',label='SW (net SRF)')
ax2.plot(time2,sws,'rx-')
ax2.plot(time,res.drs_s-res.drl,'b-',label='SW+LW (net SRF)')
ax2.plot(time2,sws+lws,'bx-')
ax2.set_ylabel('heat flux (in W/m2)')
#ax.set_xlim(0,365)
plt.legend(loc=1,framealpha=0.5,fontsize=12)
ax.set_title('i= %d, j=%d, t=%d' % (i,j,t))

ax3 = plt.subplot(212)
ax3.scatter(res.dpet,res.dpet_direct,c=np.arange(365),s=50,cmap='Reds')
xmin = np.array([res.dpet_direct,res.dpet]).flatten().min()
xmax = np.array([res.dpet_direct,res.dpet]).flatten().max()
x  = np.linspace(xmin,xmax,100)
ax3.plot(x,x,'k-',lw=2)
ax3.set_xlim(xmin,xmax)
ax3.set_ylim(xmin,xmax)
ax3.set_ylabel('PET w/ direct SW/LW flux')
ax3.set_xlabel('PET w/ prescribed LW/SW flux (as in BIOME4)')
plt.grid()

plt.show()


# for var in solar_mm_s3_srf downSol_Seaice_mm_s3_srf ilr_mm_s3_srf totCloud_mm_ua downSol_mm_TOA longwave_mm_s3_srf temp_mm_srf temp_mm_1_5m; do echo $var > $var; for m in jan feb mar apr may jun jul aug sep oct nov dec; do cdo -s output -selindexbox,1,1,17,17 -selname,$var data/interim/hadcm3_${m}_data.nc >> $var; done; done
# paste solar_mm_s3_srf downSol_Seaice_mm_s3_srf ilr_mm_s3_srf totCloud_mm_ua downSol_mm_TOA longwave_mm_s3_srf temp_mm_srf temp_mm_1_5m | column -t > /tmp/hadcm3_i1_j17.txt
