# -*- mode: python -*-

import Py6S as py6s


class AtmosfericParameters:

    def __init__(self, aod, image_day, image_month, geometry_solar_z, geometry_solar_a, geometry_view_z, geometry_view_a, target_altitude):
        self.aod = aod
        self.image_day = image_day
        self.image_month = image_month
        self.geometry_solar_z = geometry_solar_z
        self.geometry_solar_a = geometry_solar_a
        self.geometry_view_z = geometry_view_z
        self.geometry_view_a = geometry_view_a
        self.target_altitude = target_altitude
        self.output = []


    def run(self):
        # Instantiate the 6S model-------------------------------------------------------------------------------------:
        s = py6s.SixS()  # Main class. It has attributes that allow you to set parameters, run 6S and access the outputs.
        # {Attributes - Input}:
        # Atmospheric Profiles-----------------------------------------------------------------------------------------:
        s.atmos_profile = py6s.AtmosProfile.PredefinedType(py6s.AtmosProfile.Tropical)
        # Defines AOD (Aerosol Optical Depth)--------------------------------------------------------------------------:
        s.aot550 = self.aod
        # Aerosol Profiles---------------------------------------------------------------------------------------------:
        s.aero_profile = py6s.AeroProfile.PredefinedType(py6s.AeroProfile.Continental)
        # Geometries of view and illumination--------------------------------------------------------------------------:
        s.geometry = py6s.Geometry.User()
        s.geometry.day = self.image_day
        s.geometry.month = self.image_month
        s.geometry.solar_z = self.geometry_solar_z
        s.geometry.solar_a = self.geometry_solar_a
        s.geometry.view_z = self.geometry_view_z
        s.geometry.view_a = self.geometry_view_a
        # Altitudes---------------------------------------------------------------------------------------------------:
        s.altitudes = py6s.Altitudes()
        s.altitudes.set_sensor_satellite_level()  # Set the sensor altitude to be satellite level.
        s.altitudes.set_target_custom_altitude(self.target_altitude)  # The altitude of the target (in km).
        # Dictionary Output-------------------------------------------------------------------------------------------:
        output = {}
        # Simulation:
        # Spectral Response Function from Sentinel-2, using the S2A as reference:
        SENTINEL_2 = [py6s.PredefinedWavelengths.S2A_MSI_02, py6s.PredefinedWavelengths.S2A_MSI_03, py6s.PredefinedWavelengths.S2A_MSI_04,
                      py6s.PredefinedWavelengths.S2A_MSI_05, py6s.PredefinedWavelengths.S2A_MSI_06, py6s.PredefinedWavelengths.S2A_MSI_07,
                      py6s.PredefinedWavelengths.S2A_MSI_08, py6s.PredefinedWavelengths.S2A_MSI_8A]
        for num, i in enumerate(SENTINEL_2):
            s.wavelength = py6s.Wavelength(i)
            s.run()
            output[num] = {'view_z': s.outputs.view_z, 'optical_depth__total_Ray': s.outputs.optical_depth_total.rayleigh, 'rayleigh_scatransmi_upward': s.outputs.transmittance_rayleigh_scattering.upward,
                           'optical_depth__total_Aero': s.outputs.optical_depth_total.aerosol, 'aerosol_scatransmi_upward': s.outputs.transmittance_aerosol_scattering.upward,
                           'optical_depth__total_AeroRay': float(s.outputs.optical_depth_total.aerosol + s.outputs.optical_depth_total.rayleigh),
                           'total_scattering_transmittance_upward': s.outputs.total_scattering_transmittance_upward}
        self.output = output
