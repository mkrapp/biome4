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
NETCDF_FFLAGS = -I$(shell nc-config --includedir)
NETCDF_FLIBS  = -L$(shell nc-config --libdir) -lnetcdf -lnetcdff

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
OTHERFLAGS = -fallow-argument-mismatch

################################################################
## You should not have to edit anything below this line        #
################################################################

LPJOBJS = lpj/parametersmod.o lpj/orbitmod.o lpj/radiationmod.o
LPJ_AR = lpj/liblpj.so
MODELOBJS = biome4.o biome4setup.o biome4driver.o biome4main.o

FFLAGS = $(OTHERFLAGS) -O3 -Wall $(NETCDF_FFLAGS)

################################################################

%.o: %.f liblpj
	$(FC) -c -o $@ $< $(FFLAGS) -Ilpj

all::	model

# compile LPJ objects first
lpj/%.o: lpj/%.f90
	$(FC) -c -fPIC -o $@ $< $(FFLAGS)

liblpj: $(LPJOBJS)
	ar rcs $(LPJ_AR) $(LPJOBJS)

model:	$(MODELOBJS)
	$(FC) -o biome4 $(MODELOBJS) $(FFLAGS) $(NETCDF_FLIBS) -Llpj -llpj

clean::	
	-rm *.o lpj/*.o $(LPJ_AR) biome4 *.mod
