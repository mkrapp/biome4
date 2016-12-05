       module biome4
       type out_data
         real dpet(365),ddayl(365),dpet_direct(365)
         real drl(365),drs_t(365),drs_s(365)
         real sun(12),dayl(12)
         real rad0
       end type out_data
       contains
!******************************************************************************
!      Calculates insolation and PET for each month
 
       subroutine  ppeett(lat,clou,temp,swrad,lwrad,res)

       implicit none
       real, intent(in) :: lat
       real, intent(in) :: temp(12),clou(12)
       real, intent(in) :: swrad(12),lwrad(12)
       type(out_data), intent(out) :: res
       real :: dpet(365),ddayl(365),dpet_direct(365)
       real :: sun(12),dayl(12),rad0
       real :: dtemp(365),dclou(365)
       real :: dswrad(365), dlwrad(365)
       integer :: month,day,dayofm,midday(12),daysinmonth(12)
       real :: dip,pie,a,sat,cla,sla,ho,rl,fd,qo,rs
       real :: psi,l,b,radup,qoo,c,d,albedo,hos,u,v,us,vs
       real :: radanom(12)

       parameter(b=0.2,radup=107.,qoo=1360.,d=0.5,c=0.25)
       parameter(albedo=0.17)

       ! not used
       radanom = 1.0

       call daily(temp,dtemp)
       call daily(clou,dclou)   
       call daily(swrad,dswrad)
       call daily(lwrad,dlwrad)

       midday =  (/ 16,44,75,105,136,166,197,228,258,289,319,350 /)
       daysinmonth =  (/ 31,28,31,30,31,30,31,31,30,31,30,31 /)

       pie = 4.*atan(1.)
       dip = pie/180.
    
!      Daily loop
       day=0
       rad0=0.
       do month  = 1,12
         do dayofm = 1,daysinmonth(month)
           day=day+1

!          Find psi and l for this temperature from lookup table
!          psychrometer constant (pa/oc), latent heat lamba (mj/kg) 
           call table(dtemp(day),psi,l)
    
!          Calculation of longwave radiation       
           rl = (b + (1-b)*(dclou(day)/100.))*(radup- dtemp(day))

!          Since changes in radiation (short or long) will mainly be due
!          to changes in cloudiness, apply the (short wave) anomaly here too.
!          Per B. Smith 1998
           
           rl=rl*radanom(month)

!          c=0.29*cos(lat) to emphasize the effect of clouds at high latitude
!          c=0.29*cos(lat*dip)

!          Calculation of short wave radiation
           qo  =  qoo*(1.+2.*0.01675*cos(dip*(360.*real(day))/365.))
           rs  =  qo*(c+d*(dclou(day)/100.))*(1.-albedo)

           rs=rs*radanom(month)

           a   = -dip*23.4*cos(dip*360.*(real(day)+10.)/365.)
           cla =  cos(lat*dip)*cos(a)
           sla =  sin(lat*dip)*sin(a)
           u = rs*sla - rl
           v = rs*cla      

!          Check for polar day and polar night
           if(u.ge.v)then
!            polar day:
             ho = pie
           elseif(u.le.(0.-v))then
!            polar night:
             ho = 0.
           else
!            normal day and night: (find ho the time of dawn)
             ho =  acos(-u/v)
           endif
     
!          Equations for demand function
           sat=(2.5*10**6.*exp((17.27*dtemp(day))/(237.3+dtemp(day)))) &
                   /((237.3+dtemp(day))**2.)
!          Multiply l by e6 to convert from mj/kg to j/kg 
           fd = (3600./(l*1e6))*(sat/(sat+psi))

!          Store total daily equilibrium transpiration rate as dpet
           dpet(day)=fd*2.*((rs*sla-rl)*ho+rs*cla*sin(ho))/(pie/12.)
           ! use SW_net and LW_net as direct input (multiplied by hours of day
           dpet_direct(day)=fd*2.*(dswrad(day)-dlwrad(day))*ho/(pie/12.)
           ! TOA SW
           res%drs_t(day) = (qoo*sla*ho+qoo*cla*sin(ho))/pie
           ! SRF SW
           res%drs_s(day) = (rs*sla*ho+rs*cla*sin(ho))/pie
           ! SRF LW
           res%drl(day) = rl

!          Calculate daylength in hours
           if (ho.eq.0.0) then
             ddayl(day)=0.0
           else
             ddayl(day) = 24.*(ho/pie)
           end if

!          If at a mid-month day then record mid-month daily sun and dayl
           if(day.eq.midday(month))then

!            First record the day length 
             dayl(month)=ddayl(day)

!            Now calculate daily total irradiance (j/m2) & record in sun
             us = rs*sla
             vs = rs*cla
!            check for polar day and polar night
             if(us.ge.vs)then
!              polar day:
               hos = pie
             elseif(us.le.(0.-vs))then
!              polar night (also h1=0. for polar night)
               hos = 0.
             else
!              normal day and night, find hos the time of dawn
               hos =  acos(-us/vs)
             endif

!            Find total insolation for this day, units are j/m2
             sun(month)= 2.*(rs*sla*hos+rs*cla*sin(hos))*(3600.*12./pie)
!            Do not allow negative values for insolation 
             if(sun(month).le.0.) sun(month)=0.

!            Sum total annual radiation for months with t>0oC (GJs PAR year-1)
!            (assuming 50% of short wave radiation is PAR)
             if(temp(month).gt.0.)then
               rad0=rad0+real(daysinmonth(month))*sun(month)*1e-9*0.5
             endif

           endif

         end do
       end do

       res%dpet  = dpet
       res%dpet_direct  = dpet_direct
       res%ddayl = ddayl
       res%sun   = sun
       res%dayl  = dayl
       res%rad0  = rad0

       end subroutine
!**************************************************************************
!      subroutine table from bucket subroutine

      subroutine table(tc,gamma,lambda)

! looks up gamma and lambda from table (essential part of EVAPO.F)

! Author: Wolfgang Cramer, Dept. of Geography, Trondheim University-AVH,
! N-7055 Dragvoll, Norway.

! latest revisions 14/2-1991

! enable this when you run on a compiler allowing for it:
      implicit none

! on UNIX, please compile with "f77 -u"

      integer ir,il
      real gbase(2,11),lbase(2,11)
      real, intent(out) :: gamma,lambda
      real, intent(in) :: tc

      gbase = reshape( &
              (/-5.,64.6, 0.,64.9,5.,65.2,10.,65.6,15.,65.9,20.,66.1,&
                25.,66.5,30.,66.8,35.,67.2,40.,67.5,45.,67.8/),&
              shape(gbase))
      lbase = reshape( &
              (/-5.,2.513,0.,2.501,5.,2.489,10.,2.477,15.,2.465,20.,2.454,&
                25.,2.442,30.,2.430,35.,2.418,40.,2.406,45.,2.394/),&
              shape(lbase))

! temperature above highest value - set highest gamma and lambda and return

      if(tc.gt.gbase(1,11)) then
         gamma=gbase(2,11)
         lambda=lbase(2,11)
         return
      endif

! temperature at or below value - set gamma and lambda

      do il=1,11
         if(tc.le.gbase(1,il)) then
            gamma=gbase(2,il)
            lambda=lbase(2,il)
            return
         endif
      end do

      end subroutine
!**************************************************************************
      subroutine daily(mly,dly)
      implicit none
      real, intent(in) :: mly(12)
      real, intent(out) :: dly(365)
      real vinc
      integer im,id
      real midday(12)

      midday = (/16.,44.,75.,105.,136.,166.,197.,228.,258.,289.,319.,350./)

      vinc=(mly(1)-mly(12))/31.0
      dly(350)=mly(12)
      do id=351,365
         dly(id)=dly(id-1)+vinc
      end do
      dly(1)=dly(365)+vinc
      do id=2,15
         dly(id)=dly(id-1)+vinc
      end do
      do im=1,11
         vinc=(mly(im+1)-mly(im))/(midday(im+1)-midday(im))
         dly(int(midday(im)))=mly(im)
         do id=int(midday(im))+1,int(midday(im+1))-1
            dly(id)=dly(id-1)+vinc
         end do
      end do
      return
      end subroutine
      end module
