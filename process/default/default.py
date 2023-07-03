# -*- mode: python -*-

class VALUE:
    # According to Paulino et al. (2022).
    # AOD's proportion between MODIS and reversed AOD (theoretical AOD) (proportion --> 1:2).
    # The theoretical AOD correspond to 2.08 (in average) higher than MODIS' AOD.
    # The proportions (min and max) were mapped considering Paulino et al. (2022).
    default = {'factor': 2.08, 'threshold': 0.3, 'minor': {'min': 20, 'max': 30}, 'major': {'min': 40, 'max': 50}}
