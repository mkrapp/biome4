import numpy as np
import netCDF4 as nc4
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import sys
import random

random.seed(18)

biomes = [
        "Tropical evergreen forest",
        "Tropical semi-deciduous forest",
        "Tropical deciduous forest/woodland",
        "Temperate deciduous forest",
        "Temperate conifer forest",
        "Warm mixed forest",
        "Cool mixed forest",
        "Cool conifer forest",
        "Cold mixed forest",
        "Evergreen taiga/montane forest",
        "Deciduous taiga/montane forest",
        "Tropical savanna",
        "Tropical xerophytic shrubland",
        "Temperate xerophytic shrubland",
        "Temperate sclerophyll woodland",
        "Temperate broadleaved savanna",
        "Open conifer woodland",
        "Boreal parkland",
        "Tropical grassland",
        "Temperate grassland",
        "Desert",
        "Steppe tundra",
        "Shrub tundra",
        "Dwarf shrub tundra",
        "Prostrate shrub tundra",
        "Cushion forb lichen moss tundra",
        "Barren",
        "Land ice"
        ]

def main():
    # here goes the main part
    fnm = sys.argv[1]
    nc = nc4.Dataset(fnm,'r')
    biome = nc.variables["biome"][:].squeeze().astype(int)
#    optpft = nc.variables["optpft"][:].squeeze().astype(int)
#    woodpft = nc.variables["woodpft"][:].squeeze().astype(int)
    lon = nc.variables["lon"][:].squeeze()
    lat = nc.variables["lat"][:].squeeze()
    co2 = int(nc.pCO2)
    print(type(co2))
    nc.close()

    data_crs = ccrs.PlateCarree()
    proj = ccrs.PlateCarree()
    fig, ax = plt.subplots(1,1,figsize=(12,6),subplot_kw={'projection':proj})
    ax.coastlines(lw=0.5)
#    fig, ax = plt.subplots(2,1,figsize=(10,8),subplot_kw={'projection':proj})
#    ax[0].coastlines(lw=0.5)
#    ax[1].coastlines(lw=0.5)

#    optpft = np.where(optpft==14,1,0)
#    woodpft = np.where(np.logical_or(woodpft==6,woodpft==7),2,0)
#    #woodpft = np.where(woodpft==4,2,0)
#    combined = woodpft+optpft
#    combined = np.where(combined>0,combined,np.nan)
#    cmap = colors.ListedColormap(['forestgreen', 'sandybrown', 'purple'])
#    im = ax[0].pcolormesh(lon,lat,combined,cmap=cmap,vmin=0.5,vmax=3.5,rasterized=True,transform=data_crs)
#    ax[0].set_title(r"CO$_2$=%dppm"%co2,loc="right")
#    cbar = plt.colorbar(im,ax=ax[0],shrink=0.9)
#    cbar.set_ticks([])
#    labels = ["Opt PFT", "Wood PFT", "Boreal Parkland"]
#    for j, lab in enumerate(labels):
#        cbar.ax.annotate('{0}' ''.format(lab, j+1), (2, (2. * j + 1) / (2.*len(labels))),xycoords="axes fraction", ha='left', va='center', fontsize=10)

    cmap = plt.cm.Paired  # define the colormap
    # extract all colors from  color map
    l = list(range(cmap.N))
    l = random.sample(l,len(l))
    cmaplist = [cmap(i) for i in l]
    # create the new map
    cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', cmaplist, len(biomes))
#    im = ax[1].pcolormesh(lon,lat,biome,vmin=1,vmax=28,cmap=cmap,rasterized=True,transform=data_crs)
#    cbar = plt.colorbar(im,ax=ax[1],shrink=0.9)
    im = ax.pcolormesh(lon,lat,biome,vmin=1,vmax=28,cmap=cmap,rasterized=True,transform=data_crs)
    cbar = plt.colorbar(im,ax=ax,shrink=0.7)
    cbar.set_ticks([])
    for j, lab in enumerate(biomes):
        cbar.ax.annotate('{0}' ''.format(lab, j+1), (2, (2. * j + 1) / (2.*len(biomes))),xycoords="axes fraction", ha='left', va='center', fontsize=6)
    plt.show()
    fnm_out = sys.argv[2]
    fig
    fig.savefig(fnm_out, dpi=300, bbox_inches='tight', pad_inches = 0.01)


if __name__ == "__main__":
    main()

