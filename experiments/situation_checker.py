

"""from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body, get_moon
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy import units as u
import time

actual_time = time.localtime()
t = Time(f"{actual_time[0]}-{actual_time[1]}-{actual_time[2]} {actual_time[3]}:{actual_time[4]}", scale="utc")
loc = EarthLocation(lat=51.48284274379047*u.deg, lon=-2.529776116804264*u.deg, height=0*u.m)

with solar_system_ephemeris.set('jpl'):
  sun = get_body('sun', t, loc)

altazframe = AltAz(obstime=t, location=loc, pressure=0)
sunaz=sun.transform_to(altazframe)

print(sunaz.alt.degree,sunaz.az.degree)"""
