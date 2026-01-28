#!/glade/u/apps/opt/conda/envs/npl/bin/python
#PBS -N cr_s_ts
#PBS -A UALB0048
#PBS -j oe
#PBS -k eod
#PBS -q main@desched1
#PBS -l walltime=12:00:00
#PBS -l select=1:ncpus=1:mpiprocs=128

import glob, os
import numpy as np
import xarray as xr

save_path = '/glade/derecho/scratch/rford2/ihesp-gn/'
hr_path = '/glade/campaign/collections/rda/data/d651029/B.E.13.B1850C5.ne120_t12.sehires38.003.sunway_02/ocn/proc/tseries/month_1/'

var = 'SALT'

def conv_box(da):
    da_region = da.where((da.TLAT >= -69) & (da.TLAT <= -64) & ((da.TLONG >= 354) | (da.TLONG <= 19)), drop=True)
    return da_region.load()

tarea_ds = xr.open_dataset(save_path+'HRCESM-POP-TAREA-HRM.nc')
tarea = conv_box(tarea_ds.TAREA)

crmask_ds = xr.open_dataset('/glade/u/home/rford2/ihesp/data/HRCESM-CRMASK2.nc')
crmask = crmask_ds.conv_region

cr_list = []
for file in sorted(glob.glob(os.path.join(hr_path, 'B.E.13.B1850C5.ne120_t12.sehires38.003.sunway_02.pop.h.'+var+'.*'))):
    ds = xr.open_dataset(file)
    cr = conv_box(ds[var].isel(z_t=slice(0, 5))).where(crmask).weighted(tarea).mean(dim=['nlat', 'nlon', 'z_t'])
    cr_list.append(cr)
    cr.close()

cr_full = xr.concat(cr_list, dim='time')
cr_full.to_netcdf(save_path+'HRCESM-CR-'+var+'-50m-ts.nc')
