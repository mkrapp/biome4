
OBJ = parametersmod.o orbitmod.o radiationmod.o
#FFLAGS = -Ofast -Wall
#FC = gfortran
FFLAGS = -O3 -xHost -ipo
FC = ifort

all: lib

%.o: %.f90
	$(FC) -c -fPIC -o $@ $< $(FFLAGS)

lib: $(OBJ)
	ar rcs liblpj.so $(OBJ)

clean::	
	-rm *.o *.mod

