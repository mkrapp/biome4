import numpy as np
import netCDF4 as nc4
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
import sys

def main():
    # here goes the main part

    fnm1 = sys.argv[1]
    ds1 = xr.open_dataset(fnm1)
    fnm2 = sys.argv[2]
    ds2 = xr.open_dataset(fnm2)
    proj = ccrs.PlateCarree()
    data_proj = ccrs.PlateCarree()

    fig, ax = plt.subplots(3,2,sharex=True,sharey=True,subplot_kw={"projection": proj},figsize=(8,5))

    cbar_kwargs={"shrink":0.7, "label": None}

    ax[0,0].coastlines(linewidths=0.5)
    ax[0,0].set_title("biomes",loc="left",fontsize=10)
    ds1["biome"].plot(ax=ax[0,0],rasterized=True,cmap="Spectral_r",transform=data_proj,cbar_kwargs=cbar_kwargs)
    ax[1,0].coastlines(linewidths=0.5)
    ax[1,0].set_title("NPP",loc="left",fontsize=10)
    ds1["npp"].plot(ax=ax[1,0],rasterized=True,cmap="Spectral_r",transform=data_proj,cbar_kwargs=cbar_kwargs)
    ax[2,0].coastlines(linewidths=0.5)
    ax[2,0].set_title("annual evapotranspiration",loc="left",fontsize=10)
    ds1["aet"].plot(ax=ax[2,0],rasterized=True,cmap="Spectral_r",transform=data_proj,cbar_kwargs=cbar_kwargs)

    #ax[0,1].coastlines(linewidths=0.5)
    #ds2["biome"].plot(ax=ax[0,1],transform=data_proj,cbar_kwargs={"shrink":0.5})
    #ax[1,1].coastlines(linewidths=0.5)
    #ds2["npp"].plot(ax=ax[1,1],cmap="Spectral_r",transform=data_proj,cbar_kwargs={"shrink":0.5})
    #ax[2,1].coastlines(linewidths=0.5)
    #ds2["aet"].plot(ax=ax[2,1],cmap="Spectral_r",transform=data_proj,cbar_kwargs={"shrink":0.5})

    ax[0,1].coastlines(linewidths=0.5)
    ax[0,1].set_title("new - old",loc="left",fontsize=10)
    (ds1["biome"]-ds2["biome"]).plot(ax=ax[0,1],rasterized=True,transform=data_proj,vmin=-2,vmax=2,cmap="RdBu_r",cbar_kwargs=cbar_kwargs)
    ax[1,1].coastlines(linewidths=0.5)
    ax[1,1].set_title("new - old",loc="left",fontsize=10)
    (ds1["npp"]-ds2["npp"]).plot(ax=ax[1,1],rasterized=True,transform=data_proj,vmin=-300,vmax=300,cmap="RdBu_r",cbar_kwargs=cbar_kwargs)
    ax[2,1].coastlines(linewidths=0.5)
    ax[2,1].set_title("new - old",loc="left",fontsize=10)
    (ds1["aet"]-ds2["aet"]).plot(ax=ax[2,1],rasterized=True,transform=data_proj,vmin=-350,vmax=350,cmap="RdBu_r",cbar_kwargs=cbar_kwargs)

    plt.show()
    fig.tight_layout()
    fig.savefig('biome4_differences.pdf',dpi=300, bbox_inches='tight', pad_inches = 0.01)

if __name__ == "__main__":
    main()

