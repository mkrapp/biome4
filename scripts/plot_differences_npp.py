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
    fnm3 = sys.argv[3]
    ds3 = xr.open_dataset(fnm3)
    proj = ccrs.PlateCarree()
    data_proj = ccrs.PlateCarree()

    fig, ax = plt.subplots(2,2,sharex=True,sharey=True,subplot_kw={"projection": proj},figsize=(8,4))

    cbar_kwargs={"shrink":0.7, "label": None}
    vmin = -700
    vmax = 700

    ax[0,0].coastlines(linewidths=0.5)
    ax[0,0].set_title("BIOME4",loc="left",fontsize=10)
    ds1["npp"].plot(ax=ax[0,0],rasterized=True,cmap="Spectral_r",transform=data_proj,cbar_kwargs=cbar_kwargs)
    ax[1,0].coastlines(linewidths=0.5)
    ax[1,0].set_title("BIOME4 - SEDAC",loc="left",fontsize=10)
    (ds1["npp"]-ds2["Band1"]).plot(ax=ax[1,0],rasterized=True,cmap="RdBu_r",vmin=vmin,vmax=vmax,transform=data_proj,cbar_kwargs=cbar_kwargs)
    ax[0,1].coastlines(linewidths=0.5)
    ax[0,1].set_title("BIOME4 - MODIS",loc="left",fontsize=10)
    (ds1["npp"]-ds3["Band1"]).plot(ax=ax[0,1],rasterized=True,cmap="RdBu_r",vmin=vmin,vmax=vmax,transform=data_proj,cbar_kwargs=cbar_kwargs)
    ax[1,1].coastlines(linewidths=0.5)
    ax[1,1].set_title("SEDAC - MODIS",loc="left",fontsize=10)
    (ds2["Band1"]-ds3["Band1"]).plot(ax=ax[1,1],rasterized=True,cmap="RdBu_r",vmin=vmin,vmax=vmax,transform=data_proj,cbar_kwargs=cbar_kwargs)


    plt.show()
    fig.tight_layout()
    fig.savefig('biome4_differences_npp.pdf',dpi=300, bbox_inches='tight', pad_inches = 0.01)

if __name__ == "__main__":
    main()

