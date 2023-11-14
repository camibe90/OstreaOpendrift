#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import numpy as np
from opendrift.readers.reader_constant import Reader as ConstantReader
from opendrift.readers.basereader import BaseReader  as BaseReader
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.readers.unstructured import shyfem
from opendrift.readers import reader_shape
from opendrift.models.larvalfishOstrea import LarvalFish 


# In[ ]:


import cartopy.io.shapereader as shpreader
reader_ghss =reader_shape.Reader.from_shpfiles( "") 


# In[ ]:


o = LarvalFish(loglevel=50)

wcurr=reader_netCDF_CF_generic.Reader("")
sal=reader_netCDF_CF_generic.Reader("")
temp=reader_netCDF_CF_generic.Reader("")
mld=reader_netCDF_CF_generic.Reader("")
curr=reader_netCDF_CF_generic.Reader("")
depth=reader_netCDF_CF_generic.Reader("")

o.add_reader([wcurr,wcurr1, reader_ghss, sal,sal1, temp,temp1,mld,mld1, curr, curr1, depth])
o.set_config('general:use_auto_landmask', False)  # (Dis)abling the automatic GSHHG landmask
o.set_config('general:coastline_action', 'stranding') #options to use 'stranding', 'none'
o.set_config('general:seafloor_action','deactivate') 


# In[ ]:



lo = #longitude
la= #latitude
rad=#radius to seed in meters
 
timed=#seeding duration
num= #number of seed 


# In[ ]:


time = datetime(yyyy,m,d,h)
ncfile = '.nc' #file to save output 

start_time = time
time_step = timedelta(hours=xx) #time distance between each seeding 
num_steps = timed
for i in range(num_steps+1):
    o.seed_elements(lo, la, z='',
                    time=start_time + i*time_step,radius=rad, number=num)


import xarray as xr
te = xr.open_dataset("xx.nc")

weekly=te.groupby('time.week').median(skipna=True)
we1=datetime(yyyy,m,1).strftime("%W")
we2=datetime(yyyy,m,15).strftime("%W")
dvlt=weekly.sel(lat=slice(la-0.20, la+0.20), lon=slice(lo-0.50,lo+0.50), week=slice(float(we1),float(we2)), depth=slice()).median().thetao
grwr=np.exp(-8354.9*1/(dvlt +273.15) + 30.737)
dvpt=110/grwr
dvpt #developemnt time of oysters to arrive at attachemnt 


o.set_config('general:use_auto_landmask', False) 
o.set_config('drift:max_age_seconds', dvpt*24*60*60)
o.set_config('vertical_mixing:diffusivitymodel','constant')
o.set_config('drift:current_uncertainty',0.005)
o.set_config('IBM:fraction_of_timestep_swimming',0.5)
o.run(steps=timed*24, time_step=timedelta(hours=24),outfile=ncfile)

