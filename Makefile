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
NETCDF_INCLUDEDIR = /usr/local/Cellar/netcdf-fortran/4.6.1/include
NETCDF_LIBDIR = /usr/local/Cellar/netcdf-fortran/4.6.1/lib
NETCDF_FFLAGS = -I$(NETCDF_INCLUDEDIR)
NETCDF_FLIBS  = -L$(NETCDF_LIBDIR) -lnetcdff

################################################################
## If you want to use another compiler instead of the
## the GNU g77 fortran compiler, change value for compile in the
## following line. 
################################################################
FC = gfortran
#FC = ifort

####################
## Can add a -g here
####################
#OTHERFLAGS = -g
# for gfortran
OTHERFLAGS = -fallow-argument-mismatch -cpp
# for ifort
#OTHERFLAGS = -O3 -xHost -ipo -fpp -D IFORT

################################################################
## You should not have to edit anything below this line        #
################################################################

LPJOBJS = lpj/parametersmod.o lpj/orbitmod.o lpj/radiationmod.o
LPJ_AR = lpj/liblpj.so
MODELOBJS = biome4.o biome4setup.o biome4driver.o biome4main.o

#FFLAGS = $(OTHERFLAGS) -Ofast -Wall $(NETCDF_FFLAGS)
FFLAGS = $(OTHERFLAGS) $(OTHERFLAGS) $(NETCDF_FFLAGS)

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

orbit:	orbit.f90
	$(FC) -o orbit.x orbit.f90 $(FFLAGS) -Llpj -llpj

insolation:	insolation.f90
	$(FC) -o insolation.x insolation.f90 $(FFLAGS) -Llpj -llpj

clean::	
	-rm *.o lpj/*.o $(LPJ_AR) biome4 *.mod
