#!/glade/u/apps/opt/conda/envs/npl/bin/python
#PBS -N mld_avg
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

var = 'HMXL'

ds_list = []
for file in sorted(glob.glob(os.path.join(hr_path, 'B.E.13.B1850C5.ne120_t12.sehires38.003.sunway_02.pop.h.'+var+'.*'))):
    ds = xr.open_dataset(file)
    dsi = ds[var].where(ds.TLAT <= -30, drop=True)
    ds_list.append(dsi)
    ds.close()

ds_full = xr.concat(ds_list, dim='time')

mld_avg = ds_full.sel(time=slice('0338-02', None)).mean(dim='time')

cr_full.to_netcdf(save_path+'HRCESM-SO-'+var+'-338start-avg.nc')
