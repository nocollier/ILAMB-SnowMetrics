from shapely.geometry import Point, Polygon
import ILAMB.ilamblib as il
import numpy as np
from netCDF4 import Dataset

poly = Polygon([[-43.68,55.13],
                [-35.40,63.65],
                [-13.48,71.69],
                [- 7.15,86.55],
                [-59.03,86.55],
                [-76.08,76.81],
                [-61.22,72.18],
                [-53.43,58.30]])

junk,junk,lat,lon = il.GlobalLatLonGrid(0.5)

miss = -1
ids  = np.ones((lat.size,lon.size),dtype=int)*miss
for i in range(lat.size):
    for j in range(lon.size):
        if lat[i] < 0: continue
        p = Point(lon[j],lat[i])
        if not p.within(poly): ids[i,j] = 0

lbl = np.asarray(["nh_no_gl"])

with Dataset("nh_no_gl.nc",mode="w") as dset:
    dset.createDimension("lat",size=lat.size)
    dset.createDimension("lon",size=lon.size)
    dset.createDimension("nb" ,size=2       )
    dset.createDimension("n"  ,size=lbl.size)
    X = dset.createVariable("lat"   ,lat.dtype,("lat"      ))
    Y = dset.createVariable("lon"   ,lon.dtype,("lon"      ))
    I = dset.createVariable("ids"   ,ids.dtype,("lat","lon"),fill_value=miss)
    L = dset.createVariable("labels",lbl.dtype,("n"        ))
    X [...] = lat
    X.units = "degrees_north"
    Y [...] = lon
    Y.units = "degrees_east"
    I[...]  = ids
    I.labels= "labels"
    L[...]  = lbl


