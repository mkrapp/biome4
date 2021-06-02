program calc_orbit
    use parametersmod, only : dp
    use orbitmod, only : orbitpars, calcorbitpars

    implicit none

    type(orbitpars) :: orbit
    integer         :: y
    real            :: pie
    pie = 4.*atan(1.)

    open(1, file="orbit.dat", form="formatted")
    do y=-1000000,1000000,1000
        call calcorbitpars(y,orbit)
        write(1,'(I8," ",4(F13.7," "))') y, orbit%ecc, orbit%pre, sin(orbit%perh*pie/180.d0), orbit%xob
    end do
end program
