# -*- mode: python -*-

import time
from metadata import ManualParameter
from process.bmain import AWPInlandWater
from process.default.default import VALUE


start_time = time.time()
parameters = ManualParameter()
mode = parameters.default
if mode == 'True':
    aod = parameters.aod * VALUE.default['factor']

    if aod >= VALUE.default['threshold']:
        p_min = VALUE.default['major']['min']
        p_max = VALUE.default['major']['max']

    else:
        p_min = VALUE.default['minor']['min']
        p_max = VALUE.default['minor']['max']

else:
    p_min = parameters.p_min
    p_max = parameters.p_max
    aod = parameters.aod

awp = AWPInlandWater(parameters.path_image, parameters.path_out, parameters.path_metadata, aod, parameters.target_altitude, p_min, p_max)
awp.run()
print('Finished')
print('Time:', time.time() - start_time, 'seconds')