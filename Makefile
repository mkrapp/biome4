##
## Makefile for BIOME4 series models
## Uses netCDF v3.x I/O
## Jed O. Kaplan, 19 October 1999
##

################################################################
## Edit these three to indicate the path for the netcdf include
## file 'netcdf.h', the name of the netcdf library file, and the
## path to that library file.
################################################################
NETCDF_FFLAGS = $(shell nc-config --fflags)
NETCDF_FLIBS  = $(shell nc-config --flibs)

################################################################
## If you want to use another compiler instead of the
## the GNU g77 fortran compiler, change value for compile in the
## following line. 
################################################################
FC = gfortran

####################
## Can add a -g here
####################
#OTHERFLAGS = -g

################################################################
## You should not have to edit anything below this line        #
################################################################

MODELOBJS = biome4main.o biome4setup.o biome4driver.o biome4.o

FFLAGS = $(OTHERFLAGS) -O3 -Wall $(NETCDF_FFLAGS)

################################################################

all::	model

model:	$(MODELOBJS)
	$(FC) -o biome4 $(MODELOBJS) $(FFLAGS) $(NETCDF_FLIBS)

clean::	
	-rm *.o
