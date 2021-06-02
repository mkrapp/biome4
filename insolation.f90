program insolation
    use parametersmod, only : dp
    use orbitmod, only : orbitpars, calcorbitpars, toa_insolation

    implicit none

    type(orbitpars) :: orbit
    real            :: delta,a
    real(dp)        :: lat
    integer         :: cal_year,month,day,i
    real            :: daysinmonth(12)
    real            :: qo(365),qo_old(365)
    real            :: ho(365),ho_old(365)
    real            :: pie, dip, u, v
    daysinmonth = (/ 31,28,31,30,31,30,31,31,30,31,30,31 /)

    pie = 4.*atan(1.)
    dip = pie/180.

    write(*,*) "Enter calendar year (relative to 1950)"
    read(*,*) cal_year
    call calcorbitpars(cal_year,orbit)
    write(*,*) "obliquity:", orbit%xob
    open(1, file="insolation_new.dat", form="formatted")
    open(2, file="ho_new.dat", form="formatted")
    open(3, file="insolation_old.dat", form="formatted")
    open(4, file="ho_old.dat", form="formatted")
    do i=1,181
        do day=1,365
            lat = -91.0+i
            call toa_insolation(orbit,day,lat,qo(day),ho(day),delta)
            ! qo is in kJ/day
            qo_old(day) = 1366.5*(1.+2.*0.01675*cos(dip*(360.*real(day))/365.))

            a = -dip*orbit%xob*cos(dip*360.*(real(day)+10.)/365.)
            v = cos(lat*dip)*cos(a)
            u = sin(lat*dip)*sin(a)

            !      Check for polar day and polar night
            if(u.ge.v)then
                !      polar day:
                ho_old(day) = pie
            elseif(u.le.(0.-v))then
                !      polar night:
                ho_old(day) = 0.
            else
                !      normal day and night: (find ho the time of dawn)
                ho_old(day) =  acos(-u/v)
            endif
            qo_old(day) = qo_old(day)*(u*ho_old(day)+v*sin(ho_old(day)))
            ! qo_old is in ???
            ! to hours
            ho_old(day) = 24.*(ho_old(day)/pie)
        end do
        write(1,'(365(F13.2," "))') qo
        write(2,'(365(F13.2," "))') ho
        write(3,'(365(F13.2," "))') qo_old
        write(4,'(365(F13.2," "))') ho_old
    end do
    close(1)
    close(2)
    close(3)
    close(4)
end program
