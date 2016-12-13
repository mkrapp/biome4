
OBJ = parametersmod.o orbitmod.o radiationmod.o
FFLAGS = -O3 -Wall
FC = gfortran

all: lib

%.o: %.f90
	$(FC) -c -fPIC -o $@ $< $(FFLAGS)

lib: $(OBJ)
	ar rcs liblpj.so $(OBJ)

clean::	
	-rm *.o *.mod

