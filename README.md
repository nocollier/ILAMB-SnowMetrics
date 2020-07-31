# ILAMB Snow Metrics

This is a space we can use to work on the snow metrics that you all
have been working on. I have included a few things that were/are in
ILAMB but we would like to revisit. Assuming that you have ILAMB
installed (see [docs](https://www.ilamb.org/doc/)) and have cloned
this repository, you can get the relevant observational data and run
the study with the following:

```
cd ILAMB-SnowMetrics
export ILAMB_ROOT=$PWD
export PYTHONPATH=$PWD
ilamb-fetch --no-check-certificate --remote_root https://www.ilamb.org/Snow-Data
ilamb-run --config snow.cfg --model_root PATH/TO/YOUR/MODEL/RESULTS
```

I can add your observational sets to the `ilamb-fetch` command. Some
comparisons may require no extra code. For those that do, we can
develop here and then move things into ILAMB when appropriate.

## Contents

* `ConfSnowExtent.py` is a first attempt to code the spatially
  integrated version (without having seen the observational curve
  Lawrence mentioned).
* `ConfSnowWaterEquivalent.py` is copied from the ILAMB repository and
  only subtracts off the minimum from the observations (CanSISE) and
  the model output. It is a good starting point to do better.
* `ConfDrewSnowMetric.py` is not yet setup in the ILAMB confrontation
  style and only plots the data and best fit exponential curve as Drew
  had them. Need to clean this up with his paper and need
  observational data. Alternatively we could use Eleanor's metric/data.
* `ConfPermafrostExtent.py` is copied from the ILAMB repository and compares
  permafrost extent with respect to the NSIDC permafrost map. If you
  look at the extent
  [maps](https://www.ilamb.org/CMIP5v6/historical/HydrologyCycle/Permafrost/NSIDC/NSIDC.html#AllModels)
  you will see that some models are returning soil temperature over
  Greenland and some just on the coastal regions leading to a
  difficulty in interpretation. We could also revisit methodology,
  this extent is based on a climatological soil temperature threshold.
