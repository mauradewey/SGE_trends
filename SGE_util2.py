import xarray as xr
import numpy as np
from datetime import datetime, timedelta
from glob import glob
from os import path

#utils
def grey_atmos(x,a,b):
    #x: surface temperature
    #a: parameter describing the surface temperature dependent contribution of dry atmosphere to the optical depth 
    #b: parameter describing the surface temperature dependent contributino of water vapour to the optical depth
    sigma=5.670374419E-8
    tau_wet=b*(x-220)
    tau=a+tau_wet
    y=sigma*(x**4)*(1-1/((3/4)*tau+(1/2)))
    return y

def SGE_threshold(T,OLR,TPWV):
    #T: surface temperature [K]
    #OLR: outgoing longwave radiation [W/m^2]
    #TPWV: total precitable water [kg/m^2]
    #SGE_occ: grid passes threshold (1=yes, 0=no)
    #SGE_strength: difference between expected and measured OLR [W/m^2]
    sigma=5.670374419E-8
    H2O_threshold=40
    OLR_expected=sigma*(T**4)-grey_atmos(T,0.84454868,0.00804156)
    OLR_best_fit=sigma*(T**4)-grey_atmos(T,0.67507104,0.00866809)
    SGE_occ=xr.where(np.logical_and((OLR-OLR_expected)<0, TPWV>H2O_threshold), np.ones_like(OLR), 0)
    SGE_strength=(OLR_best_fit-OLR)*SGE_occ
    return SGE_occ, SGE_strength


def earth_radius(lat):
    '''
    -----------
    https://towardsdatascience.com/the-correct-way-to-average-the-globe-92ceecd172b7
    WGS84: https://earth-info.nga.mil/GandG/publications/tr8350.2/tr8350.2-a/Chapter%203.pdf
    '''
    from numpy import deg2rad, sin, cos

    # define oblate spheroid from WGS84
    a = 6378137
    b = 6356752.3142
    e2 = 1 - (b**2/a**2)
    
    # convert from geodecic to geocentric
    # see equation 3-110 in WGS84
    lat = deg2rad(lat)
    lat_gc = np.arctan( (1-e2)*np.tan(lat) )

    # radius equation
    # see equation 3-107 in WGS84
    r = (
        (a * (1 - e2)**0.5) 
         / (1 - (e2 * np.cos(lat_gc)**2))**0.5 
        )
    return r

def shift_latlon(df):
    #shift airs data from [-180,180] to [0,360]
    lon_atrib = df.coords['lon'].attrs
    lat_atrib = df.coords['lat'].attrs
    df.coords['lon'] = df.coords['lon'] % 360 + 0.5 #v7.0 AIRS values off by 0.5 degress??
    df.coords['lat'] = df.coords['lat'] + 0.5
    df = df.sortby(df.lon)
    df = df.sortby(df.lat).sel(lat=slice(-34.5,34.5))
    df.coords['lon'].attrs = lon_atrib
    df.coords['lat'].attrs = lat_atrib
    return df

def get_AIRS_files(airs_dp,dateStart,dateEnd):
    #modified from https://stackoverflow.com/questions/31821098/getting-file-from-date-range-of-the-current-directory

    CERES_DATE_FORMAT = '%Y%m%d'
    AIRS_DATE_FORMAT = r'AIRS.%Y.%m.%d'
    AIRS_PATH_FORMAT = airs_dp
    start_date = datetime.strptime(dateStart, CERES_DATE_FORMAT).date()
    end_date = datetime.strptime(dateEnd, CERES_DATE_FORMAT).date()
    delta_one_day = timedelta(days=1)
    AIRS_files = []
    date = start_date
    while date <= end_date:
        data_folder = date.strftime(AIRS_PATH_FORMAT)
        if path.isdir(data_folder):
            for filename in glob(data_folder+'/'+date.strftime(AIRS_DATE_FORMAT)+'*.nc4'):
                AIRS_files.append(filename)
        date += delta_one_day 
    return AIRS_files

# a couple of preprocess setps to speed up open_mfdataset for CERES files
def olrc_preprocess(ds):
    return ds['toa_lw_clr_daily'].sel(lat=slice(-34.5,34.5))

def olra_preprocess(ds):
    return ds['toa_lw_all_daily'].sel(lat=slice(-34.5,34.5))

def time_preprocess(ds):
    return ds['time']

def h2o_preprocess(ds):
    return ds['aux_precipw_daily'].sel(lat=slice(-34.5,34.5))

def sst_preprocess(ds):
    return ds['aux_skint_daily'].sel(lat=slice(-34.5,34.5))