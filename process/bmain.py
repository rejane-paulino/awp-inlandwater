# -*- mode: python -*-

from .f_aux import Auxiliary
from .atm.sixinput import SixInput
from .atm.sim6s import AtmosfericParameters
from .windowsize import WindowAdaptative
from .adj_toolbox import AdjacencyCorr


class AWPInlandWater:

    def __init__(self, path_image, path_out, path_metadata, aod, target_altitude, p_min, p_max):
        self.path_image = path_image
        self.path_out = path_out
        self.path_metadata = path_metadata
        self.aod = aod
        self.target_altitude = target_altitude
        self.p_min = p_min
        self.p_max = p_max


    def run(self):
        # Loads the main functions:
        auxprocess = Auxiliary()
        sixinput_values = SixInput()
        window = WindowAdaptative()
        adjtool = AdjacencyCorr()
        # It resampling the image pixels to 20-by-20 meters:
        auxprocess.resample(self.path_image)
        # It loads the images:
        auxprocess.loadarray()
        auxprocess.corrsize()
        # It recovers the SixInput values:
        metadata = Auxiliary().open_metadata(self.path_metadata)
        sixinput_values.date_and_time(metadata)
        sixinput_values.geometry(metadata)
        sixinput_values.sixparameters(self.target_altitude)
        # It simulates the atmospheric feature:
        image_day_ = int(sixinput_values.sixparam['image']['date_and_time']['day'])
        image_month_ = int(sixinput_values.sixparam['image']['date_and_time']['month'])
        geometry_solar_z_ = float(sixinput_values.sixparam['geometry_view_and_sun']['sun_zn'])
        geometry_solar_a_ = float(sixinput_values.sixparam['geometry_view_and_sun']['sun_az'])
        geometry_view_z_ = float(sixinput_values.sixparam['geometry_view_and_sun']['view_zn'])
        geometry_view_a_ = float(sixinput_values.sixparam['geometry_view_and_sun']['view_az'])
        target_altitude_ = float(sixinput_values.sixparam['auxiliary_data']['target_altitude_km'])
        atmospheric_parameters = AtmosfericParameters(self.aod, image_day_, image_month_, geometry_solar_z_, geometry_solar_a_, geometry_view_z_, geometry_view_a_, target_altitude_)
        atmospheric_parameters.run()
        # It reduces the adjacency effect:
        window.mndwi_index(auxprocess.array)
        window.sliding_window(self.p_min, self.p_max)
        out_corrected = {}
        for i in range(0, 8):
            adjtool.atmospheric_point_scattering_function(atmospheric_parameters.output[i])
            adjtool.conv(auxprocess.array[i], window.array_wsize)
            adjtool.AdjacencyEffect_correction(atmospheric_parameters.output[i], auxprocess.array[i])
            out_corrected[i] = adjtool.withoutadj
        # Save:
        auxprocess.export_raster(out_corrected, self.path_out)
        # Remove intermediate files:
        auxprocess.removedir(r'intermediaries/resampled_img')
