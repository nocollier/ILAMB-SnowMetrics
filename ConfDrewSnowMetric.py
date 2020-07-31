from ILAMB.ModelResult import ModelResult
import pylab as plt
import numpy as np
from scipy.optimize import minimize

def _computeAnnualAmplitude(data):
    # year is October through March
    shp  = data.shape
    shp  = (-1,12,) + shp[-2:]
    dat  = (data[9:-3,...].reshape(shp))[:,:6,...]-273.15
    amp  = dat.max(axis=1)-dat.min(axis=1)
    return dat.mean(axis=1),amp

def _computeSeasonalMean(data):
    # year is October through March
    shp  = data.shape
    shp  = (-1,12,) + shp[-2:]
    dat  = (data[9:-3,...].reshape(shp))[:,:6,...]
    return dat.mean(axis=1)
    
t0   = (1980-1850)*365.
tf   = (2000-1850)*365.
m    = ModelResult("/home/nate/data/ILAMB/MODELS/TestModels/LandTest")
tas  = m.extractTimeSeries("tas",
                           initial_time = t0,
                           final_time   = tf).trim(t   = [t0,tf],
                                                   lat = [20,90])
tsl  = m.extractTimeSeries("tsl",
                           initial_time = t0,
                           final_time   = tf).trim(t   = [t0,tf],
                                                   lat = [20,90],
                                                   d   = [0.195,0.205]).integrateInDepth(mean=True)
snw = m.extractTimeSeries("snw",
                           initial_time = t0,
                           final_time   = tf).trim(t   = [t0,tf],
                                                   lat = [20,90]).convert("m")

Tair ,Aair  = _computeAnnualAmplitude(tas.data)
Tsoil,Asoil = _computeAnnualAmplitude(tsl.data)
Seff        = _computeSeasonalMean(snw.data)
Anorm       = (Aair-Asoil)/(Aair)

mask  = Tair.mask + Aair.mask + Tsoil.mask + Asoil.mask + Seff.mask + Anorm.mask
keep  = (Tair  < -1.0)
keep *= (Tsoil <  2.5)
keep *= (Aair  > 10.0)
keep *= (Seff  > 0.01)
keep *= (Seff  < 1.50)
keep *= (Anorm >= 0.)
keep *= (Anorm <= 1.)
mask += (keep.data==False)
Anorm = np.ma.masked_array(Anorm.data,mask=mask)
Seff  = np.ma.masked_array(Seff .data,mask=mask)


anorm = Anorm[mask==False].flatten().data
seff  = Seff [mask==False].flatten().data

def _residual(x):
    P = x[0]; Q = x[1]; R = x[2]
    return np.linalg.norm(anorm-(P+Q*(1.-np.exp(-seff/R))))

x0  = np.array([0.,1.,0.1])
res = minimize(_residual, x0,
               options = {'disp': True})
print(res.x)


plt.plot(seff,anorm,'.')

s = np.linspace(0,1.5,1000)
a = res.x[0] + res.x[1]*(1.-np.exp(-s/res.x[2]))
plt.plot(s,a,'-r')
plt.xlim(0,0.5)
plt.ylim(0,1)
plt.show()
