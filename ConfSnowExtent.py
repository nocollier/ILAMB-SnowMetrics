from ILAMB.Confrontation import Confrontation
from ILAMB.Regions import Regions

class ConfSnowExtent(Confrontation):

    def stageData(self,m):

        # Ensure that the Northern Hemisphere is a region
        r = Regions() 
        r.addRegionLatLonBounds("nh","Northern Hemisphere",[0,90],[-180,+180])

        # Get the observational data
        obs = Variable(filename       = self.source,
                       variable_name  = self.variable,
                       alternate_vars = self.alternate_vars,
                       t0 = None if len(self.study_limits) != 2 else self.study_limits[0],
                       tf = None if len(self.study_limits) != 2 else self.study_limits[1])

        # Try to extract a commensurate quantity from the model
        mod = m.extractTimeSeries(self.variable,
                                  alt_vars     = self.alternate_vars,
                                  expression   = self.derived,
                                  initial_time = obs.time_bnds[ 0,0],
                                  final_time   = obs.time_bnds[-1,1])
        
        # But here we take the spatial average over just the northern hemisphere
        mod = mod.integrateInSpace(region="nh",mean=True)

        # This makes sure the time series overlap and are in the same units
        obs,mod = il.MakeComparable(obs,mod,
                                    mask_ref  = True,
                                    clip_ref  = True,
                                    extents   = self.extents,
                                    logstring = "[%s][%s]" % (self.longname,m.name))
