# -*- mode: python -*-

import numpy as np
import warnings

from .f_aux import Auxiliary
import codeinC.adpwindow.slidingwindow as wsize


class WindowAdaptative:

    def mndwi_index(self, dic: dict):
        """
        It calculates the MNDWI spectral index.
        It's used to determine the fraction of water and non-water along the array:
        :param dic: array with spectral values;
        :return: dictionary with mdwi index value.
        """
        warnings.filterwarnings("ignore")
        # It calculates the MNDWI index:
        mndwi = (dic[1] - dic[8]) / (dic[1] + dic[8])
        # It creates a binary water mask [0 or 1]:
        self.wmask = np.where(mndwi <= 0.20, 0, 1)


    def sliding_window(self, p_min_, p_max_):
        # It generates a border around the array wmask:
        wmask_b = Auxiliary().border(self.wmask, 500, -9999)
        # Array-sizes:
        (imgH, imgW) = self.wmask.shape[:2]
        (edgeH, edgeW) = wmask_b.shape[:2]
        edge_size = 500  # Default value
        # Adaptative Window - Size:
        self.array_wsize = wsize.sliding_window(int(imgH), int(imgW), int(edgeH), int(edgeW), int(edge_size), wmask_b.astype('float'), int(p_min_), int(p_max_))

