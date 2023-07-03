# -*- mode: python -*-

import cv2
import os
from osgeo import gdal
gdal.UseExceptions()
import pathlib
import shutil
import glob
import numpy as np
import json
import xmltodict


class Auxiliary:

    def resample(self, path_image: str):
        """
        It resamples the pixel size from 10 m to 20 m:
        :param path_image: path with images .tif;
        :return: directory 'resampled_img' with resampled-20m images.
        """
        for i in os.listdir(path_image):
            if 'B02' in i or \
                    'B03' in i or \
                    'B04' in i or \
                    'B08' in i:
                # Create directory:
                # It salves the bands resampled within intermediate directory -> default:
                self.dir(r'intermediaries', 'resampled_img')
                # Resample pixel -> 10 to 20 m:
                filename = path_image + '/' + i
                ds_ = gdal.Warp(self.newdir + '/' + i,
                                filename,
                                xRes=20,
                                yRes=20,
                                resampleAlg='near')
            if 'B05' in i or \
                    'B06' in i or \
                    'B07' in i or \
                    'B8A' in i or \
                    'B12' in i:
                # It copies the imagery to another directory:
                shutil.copy2(os.path.join(path_image, i), self.newdir)


    def loadarray(self):
        """
        Loads the image and reads as array:
        :param path_image: path with resampling images (.tif);
        :return: dictionary with array.
        """
        # Output
        output = {}
        path_image = r'intermediaries/resampled_img'
        paths = [band for band in glob.glob(os.path.join(path_image, '*.tif'))
                 if 'B02' in band or 'B03' in band or 'B04' in band or 'B05' in band or 'B06' in band or 'B07' in band or 'B08' in band or 'B8A' in band or 'B12' in band]
        paths.insert(8, paths.pop(7))
        count = 0
        for filename in paths:
            dataset = gdal.Open(filename)
            array = dataset.ReadAsArray().astype(float)
            # Save in the dictionary structure:
            output[count] = array
            count = count + 1
        self.loads = output


    def corrsize(self):
        """
        Verifies and adjusts the array size after the resamplings:
        :param dic: dictionary with array;
        :return: dictionary with adjusted array.
        """
        # Verifies the array size:
        rx, ry = self.loads[7].shape
        output = {}
        for i in range(0, 9):
            array_ = self.loads[i]
            x, y = array_.shape
            sub_x = x - rx
            sub_y = y - ry
            # If rx or ry > x or y (to add rows or columns).
            # If rx or ry < x or y (to reduce rows or columns).
            # Conditions - in ROW:
            if sub_x > 0:
                n = abs(sub_x)
                array_X = np.hstack((array_.transpose(), np.tile(array_.transpose()[:, [0]], n)))
                array_X = array_X.transpose()
            elif sub_x < 0:
                n = abs(sub_x)
                array_X = array_[:-n]
            else:
                array_X = array_
            # Conditions - in COLUMNS:
            if sub_y > 0:
                n = abs(sub_y)
                array_Y = np.hstack((array_X, np.tile(array_X[:, [0]], n)))
                output[i] = array_Y
            elif sub_y < 0:
                n = abs(sub_y)
                array_Y = array_X.transpose()[:-n]
                output[i] = array_Y.transpose()
            else:
                output[i] = array_X
        self.array = output


    def dir(self, path: str, name_directory: str):
        """
        Creates a new directory:
        :param path: path where it will be created;
        :param name_directory: directory's name;
        :return: path of the new directory.
        """
        saved_path = path + '/' + name_directory
        pathlib.Path(saved_path).mkdir(parents=True, exist_ok=True)
        self.newdir = str(saved_path)


    def border(self, array, edge_size, value):
        """
        It creates a boundary around the array considering the "edge_size" attribute:
        :param array: array with syrface reflectance;
        :param edge_size: edge size (int);
        :param value: NaN value;
        :return: array with edge.
        """
        output = cv2.copyMakeBorder(src=array,
                                  top=edge_size,
                                  bottom=edge_size,
                                  left=edge_size,
                                  right=edge_size,
                                  borderType=cv2.BORDER_CONSTANT,
                                  value=value)
        return (output)


    def export_raster(self, dic: dict, path_out: str):
        """
        Saves the corrected images:
        :param dic: dictionary with corrected bands;
        :param path_out: path where the images will be saved
        :return: corrected images in .TIF.
        """
        paths = [band for band in glob.glob(os.path.join(r'intermediaries/resampled_img', '*.tif'))
                 if 'B02' in band or 'B03' in band or 'B04' in band or 'B05' in band or 'B06' in band or 'B07' in band or 'B08' in band or 'B8A' in band]
        for band, tag in zip(dic, paths):
            filename_reference = tag
            filename_out_factor = path_out + '/' + tag[-30:] + '.tif'
            dataset_reference = gdal.Open(filename_reference)

            line = dataset_reference.RasterYSize
            column = dataset_reference.RasterXSize
            bands = 1

            # defining drive
            driver = gdal.GetDriverByName('GTiff')
            # copying the bands data type pre-existing
            data_type = gdal.GetDataTypeByName('Float32')
            # create new dataset
            dataset_output = driver.Create(filename_out_factor, column, line, bands, data_type)
            # copying the spatial information pre-existing
            dataset_output.SetGeoTransform(dataset_reference.GetGeoTransform())
            # copying the projection information pre-existing
            dataset_output.SetProjection(dataset_reference.GetProjectionRef())
            # writing array data in band
            dataset_output.GetRasterBand(1).WriteArray(dic[band])
            # solve values
            test = dataset_output.FlushCache()
            # close dataset
            dataset_output = None


    def open_metadata(self, path_metadata: str):
        """
        Reads the metadata as [.json]:
        :param path_metadata: path of metadata in .xml;
        :return: file as dict;
        """
        with open(path_metadata) as xml_file:
            # Converts the .xml to dict(obj):
            file_dictionary = xmltodict.parse(xml_file.read())
            xml_file.close()
            # Converts the dict to .json:
            return (json.loads(json.dumps(file_dictionary)))


    def removedir (self, path_dir):
        shutil.rmtree(path_dir)
