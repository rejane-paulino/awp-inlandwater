# -*- mode: python -*-

import pandas as pd


class Metadata():

    def __init__(self, path_image, path_out, path_metadata, aod, target_altitude, p_min, p_max, default):
        self.path_image = path_image
        self.path_out = path_out
        self.path_metadata = path_metadata
        self.aod = aod
        self.target_altitude = target_altitude
        self.p_min = p_min
        self.p_max = p_max
        self.default = default


    def loadMetadata(self):
        dInput = pd.read_csv(r'parameters.txt', sep=';')
        self.path_image = str(dInput.iloc[0][1]).strip()
        self.path_out = str(dInput.iloc[1][1]).strip()
        self.path_metadata = str(dInput.iloc[2][1]).strip()
        self.aod = float(dInput.iloc[3][1])
        self.target_altitude = float(dInput.iloc[4][1])
        self.p_min = int(dInput.iloc[5][1])
        self.p_max = int(dInput.iloc[6][1])
        self.default = str(dInput.iloc[7][1]).strip()


class ManualParameter(Metadata):

    def __init__(self):
        super(ManualParameter, self).loadMetadata()

