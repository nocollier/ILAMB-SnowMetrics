from ILAMB.Confrontation import Confrontation

class ConfSnowWaterEquivalent(Confrontation):
            
    def stageData(self,m):

        # clip off anything above 250 [mm]
        obs,mod = super(ConfSnowWaterEquivalent,self).stageData(m)
        obs.convert("mm")
        mod.convert("mm")
        obs.data = obs.data.clip(0,250)
        mod.data = mod.data.clip(0,250)
        return obs,mod
