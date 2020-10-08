from ILAMB.Confrontation import Confrontation
from ILAMB.Regions import Regions
from ILAMB.Variable import Variable
import ILAMB.ilamblib as il
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import os
import ILAMB.Post as post

class ConfSnowExtent(Confrontation):

    def __init__(self,**keywords):
        
        super(ConfSnowExtent,self).__init__(**keywords)
        
        # Ensure we have the region we need
        r = Regions() 
        r.addRegionNetCDF4(os.path.join(os.environ["ILAMB_ROOT"],"DATA/regions/nh_no_gl.nc"))
        
    def stageData(self,m):

        # Get the observational data
        obs = Variable(filename       = self.source,
                       variable_name  = "sce",
                       alternate_vars = self.alternate_vars,
                       t0 = None if len(self.study_limits) != 2 else self.study_limits[0],
                       tf = None if len(self.study_limits) != 2 else self.study_limits[1])
        obs.data = np.ma.masked_invalid(obs.data)
        
        # Try to extract a commensurate quantity from the model
        mod = m.extractTimeSeries(self.variable,
                                  alt_vars     = self.alternate_vars,
                                  expression   = self.derived,
                                  initial_time = obs.time_bnds[ 0,0],
                                  final_time   = obs.time_bnds[-1,1])
        
        # But here we take the spatial integral over the northern hemisphere but not Greenland
        mod = mod.integrateInSpace(region="nh_no_gl")

        # This makes sure the time series overlap and are in the same units
        obs,mod = il.MakeComparable(obs,mod,
                                    mask_ref  = True,
                                    clip_ref  = True,
                                    extents   = self.extents,
                                    logstring = "[%s][%s]" % (self.longname,m.name))

        # Renaming these will make plots automatic
        obs.name = "spaceint_of_snc_over_global"
        mod.name = "spaceint_of_snc_over_global"        
        return obs,mod
            
    def confront(self,m):
        
        obs,mod = self.stageData(m)
        obs_mean = obs.integrateInTime(mean=True)
        mod_mean = mod.integrateInTime(mean=True)
        bias = Variable(name = "Bias global",
                        unit = obs_mean.unit,
                        data = obs_mean.data - mod_mean.data)
        var  = obs.variability().data
        bias_score = Variable(name = "Bias Score global",
                              unit = "1",
                              data = np.exp(-np.abs(bias.data)/var))
        obs_mean.name = "Period Mean global"
        mod_mean.name = "Period Mean global"
        
        with Dataset(os.path.join(self.output_path,"%s_%s.nc" % (self.name,m.name)),mode="w") as dset:
            dset.setncatts({"name":m.name,"color":m.color,"complete":0})
            mod       .toNetCDF4(dset,group="MeanState")
            mod_mean  .toNetCDF4(dset,group="MeanState")
            bias      .toNetCDF4(dset,group="MeanState")
            bias_score.toNetCDF4(dset,group="MeanState")
            dset.setncattr("complete",1)

        if not self.master: return
        with Dataset(os.path.join(self.output_path,"%s_Benchmark.nc" % (self.name)),mode="w") as dset:
            dset.setncatts({"name":"Benchmark","color":(0.5,0.5,0.5),"complete":0})
            obs     .toNetCDF4(dset,group="MeanState")
            obs_mean.toNetCDF4(dset,group="MeanState")
            dset.setncattr("complete",1)
            
    def modelPlots(self,m):
        
        bname = os.path.join(self.output_path,"%s_Benchmark.nc" % (self.name       ))
        fname = os.path.join(self.output_path,"%s_%s.nc"        % (self.name,m.name))
        if not os.path.isfile(bname): return
        if not os.path.isfile(fname): return
        page = [page for page in self.layout.pages if "MeanState" in page.name][0]
        with Dataset(fname) as dset: clr = dset.color

        # plot spaceint
        pname = "spaceint"
        region = "global"
        page.addFigure("Spatially integrated regional mean","spaceint","MNAME_RNAME_spaceint.png","REGIONAL MEAN",False)
        obs = Variable(filename=bname,variable_name="spaceint_of_snc_over_global",groupname="MeanState")
        mod = Variable(filename=fname,variable_name="spaceint_of_snc_over_global",groupname="MeanState")
        fig,ax = plt.subplots(figsize=(15,3),tight_layout=True,dpi=100)
        obs.plot(ax,lw=2,color='k',alpha=0.5)
        mod.plot(ax,lw=2,color=clr,label=m.name)
        dy = 0.05*(self.limits[pname][region]["max"]-self.limits[pname][region]["min"])
        ax.set_ylim(self.limits[pname][region]["min"]-dy,
                    self.limits[pname][region]["max"]+dy)
        ax.set_ylabel(post.UnitStringToMatplotlib(obs.unit))
        fig.savefig(os.path.join(self.output_path,"%s_%s_%s.png" % (m.name,"global",pname)))
        plt.close()
