# -*- mode: python -*-

from osgeo import gdal
gdal.UseExceptions()
import numpy as np

from .f_aux import Auxiliary
import codeinC.adpconv.adpconvolution as conv


class AdjacencyCorr:

    def atmospheric_point_scattering_function(self, atmosphere_parameters):
        """
        Calculates the Fr weight per distance.
        """
        # Output Data:
        output = {}
        # Converts the grid distance to km:
        open_adjrange = gdal.Open(r'aux_/fr_grid20x20m/grid%distance%fr%20x20m.tif').ReadAsArray().astype(float)
        radius_km = open_adjrange / 1000
        # Zenith view angle -> degree:
        view_z = float(atmosphere_parameters['view_z'])
        # Rayleigh UPWARD diffuse transmittance -> T_upward_difRayleigh:
        Rayleigh_OpticalDepth = float(atmosphere_parameters['optical_depth__total_Ray'])
        T_upward_Rayleigh = float(atmosphere_parameters['rayleigh_scatransmi_upward'])
        T_upward_dirRayleigh = np.exp(-Rayleigh_OpticalDepth / np.cos(view_z * (np.pi / 180)))
        T_upward_difRayleigh = T_upward_Rayleigh - T_upward_dirRayleigh
        # Aerosol UPWARD diffuse transmittance -> T_upward_difAerosol:
        Aerosol_OpticalDepth = float(atmosphere_parameters['optical_depth__total_Aero'])
        T_upward_Aerosol = float(atmosphere_parameters['aerosol_scatransmi_upward'])
        T_upward_dirAerosol = np.exp(-Aerosol_OpticalDepth / np.cos(view_z * (np.pi / 180)))
        T_upward_difAerosol = T_upward_Aerosol - T_upward_dirAerosol
        # Calculates the Aerosol's Fr and Rayleigh's Fr functions using the equation described by Vermote et al.(2006):
        FrRayleigh = ((0.930 * np.exp(-0.08 * radius_km)) + (0.070 * np.exp(-1.10 * radius_km)))
        FrAerosol = ((0.448 * np.exp(-0.27 * radius_km)) + (0.552 * np.exp(-2.83 * radius_km)))
        # Calculates the APSF (Fr) -> Atmospheric Point Scattering Function:
        Fr = (T_upward_difRayleigh * FrRayleigh + T_upward_difAerosol * FrAerosol) / (T_upward_difRayleigh + T_upward_difAerosol)
        # Exports the APSF:
        output['apfs'] = Fr
        self.apfs = output

    def conv(self, array_band, array_wsize):
        # Atmospheric Point Scattering Function:
        Weight_general = self.apfs['apfs']
        # Creates the edge in the image. Here, its generates an edge in the array with zero values. The edge size is
        # proportional to the kernel width and length:
        edge_size = 124 # Default. It uses the maximum window size defined in 5000 meters.
        band = Auxiliary().border(array_band, edge_size, 0)
        # Adaptative convolution:
        self.adjvalue = conv.AdaptativeConvolution(array_band, band, array_wsize, Weight_general)


    def AdjacencyEffect_correction(self, atmosphere_parameters, array_band):
        """
        Removes the adjacency effect of the image, using the equation described in the Vermote et al. (1997).
        """
        # Zenith view angle -> degree:
        view_z = float(atmosphere_parameters['view_z'])
        # Atmopheric optical depth (Rayleigh + Aerosol) -> Atmospheric_OpticalDepth:
        Atmospheric_OpticalDepth = float(atmosphere_parameters['optical_depth__total_AeroRay'])
        # Total transmittance UPWARD (Rayleigh + Aerosol) -> T_upward:
        T_upward = float(atmosphere_parameters['total_scattering_transmittance_upward'])
        # Total transmittance UPWARD direct (Rayleigh + Aerosol) -> T_upward_dirAeroRay:
        T_upward_dirAeroRay = np.exp(-Atmospheric_OpticalDepth / np.cos(view_z * (np.pi / 180)))
        # Total transmittance UPWARD diffuse (Rayleigh + Aerosol) -> T_upward_difAeroRay
        T_upward_difAeroRay = T_upward - T_upward_dirAeroRay
        # Surface reflectance without adjacency effect - Vermote et al. (1997):
        self.withoutadj = (array_band * (T_upward / T_upward_dirAeroRay)) - (self.adjvalue * (T_upward_difAeroRay / T_upward_dirAeroRay))

