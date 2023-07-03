# -*- mode: python -*-

import numpy as np
import datetime


class SixInput:

    def date_and_time(self, metadata):
        """
        Returns the date and the hour fo the image acquisition:
        :param metadata: metadata in dict;
        :return: date and hour.
        """
        # Output data:
        output = {}
        # Date -> '%Y-%m-%d':
        date_and_time = metadata["n1:Level-1C_Tile_ID"]['n1:General_Info']['SENSING_TIME']['#text']
        date_acquired = date_and_time[0:10]
        date = datetime.datetime.strptime(date_acquired, '%Y-%m-%d').timetuple()
        output['day'] = date.tm_mday
        output['month'] = date.tm_mon
        output['year'] = date.tm_year
        # Time -> 'hours':
        scene_center_time = date_and_time[11:-1].split(':')
        time_hh = int(scene_center_time[0]) + (float(scene_center_time[1]) / 60) + (float(scene_center_time[2]) / 3600)
        output['time_hh'] = time_hh
        self.datetime = output


    def geometry(self, metadata):
        """
        Returns the average geometry of observation and illumination of the image:
        :param metadata: metadata in dict;
        :return: geometries of observation and illumination in degree.
        """
        # Output data:
        output = {}
        # Lists:
        angle_view_az = []
        angle_view_zn = []
        # Sun azimuth [az] and zenith [zn] angle:
        # Sun angle -> AZIMUTH:
        sun_az_angle = float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']['Mean_Sun_Angle']['AZIMUTH_ANGLE']['#text'])
        # Sun angle -> ZENITH:
        sun_zn_angle = float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']['Mean_Sun_Angle']['ZENITH_ANGLE']['#text'])
        # View [SATELLITE] azimuth [az] and zenith [zn] angle band_blue -> id 1:
        angle_view_az.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][1]['AZIMUTH_ANGLE']['#text']))
        angle_view_zn.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][1]['ZENITH_ANGLE']['#text']))
        # View [SATELLITE] azimuth [az] and zenith [zn] angle band_green -> id 2:
        angle_view_az.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][2]['AZIMUTH_ANGLE']['#text']))
        angle_view_zn.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][2]['ZENITH_ANGLE']['#text']))
        # View [SATELLITE] azimuth [az] and zenith [zn] angle band_red -> id 3:
        angle_view_az.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][3]['AZIMUTH_ANGLE']['#text']))
        angle_view_zn.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][3]['ZENITH_ANGLE']['#text']))
        # View [SATELLITE] azimuth [az] and zenith [zn] angle band_rededge1 -> id 4:
        angle_view_az.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][4]['AZIMUTH_ANGLE']['#text']))
        angle_view_zn.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][4]['ZENITH_ANGLE']['#text']))
        # View [SATELLITE] azimuth [az] and zenith [zn] angle band_rededge1 -> id 5:
        angle_view_az.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][5]['AZIMUTH_ANGLE']['#text']))
        angle_view_zn.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][5]['ZENITH_ANGLE']['#text']))
        # View [SATELLITE] azimuth [az] and zenith [zn] angle band_rededge3 -> id 6:
        angle_view_az.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][6]['AZIMUTH_ANGLE']['#text']))
        angle_view_zn.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][6]['ZENITH_ANGLE']['#text']))
        # View [SATELLITE] azimuth [az] and zenith [zn] angle band_nir -> id 7:
        angle_view_az.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][7]['AZIMUTH_ANGLE']['#text']))
        angle_view_zn.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][7]['ZENITH_ANGLE']['#text']))
        # View [SATELLITE] azimuth [az] and zenith [zn] angle band_nir_a -> id 8:
        angle_view_az.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][8]['AZIMUTH_ANGLE']['#text']))
        angle_view_zn.append(float(metadata['n1:Level-1C_Tile_ID']['n1:Geometric_Info']['Tile_Angles']["Mean_Viewing_Incidence_Angle_List"]['Mean_Viewing_Incidence_Angle'][8]['ZENITH_ANGLE']['#text']))
        # Retrieve average geometry:
        output['sun_az'] = sun_az_angle
        output['sun_zn'] = sun_zn_angle
        output['view_az'] = np.array(angle_view_az).mean()
        output['view_zn'] = np.array(angle_view_zn).mean()
        self.geo = output


    def sixparameters(self, target_altitude: float):
        """
        Joins 6S input parameters.
        """
        # Output Data:
        output = {}
        # Levels:
        output['image'] = {}
        output['geometry_view_and_sun'] = {}
        output['auxiliary_data'] = {}
        # Date and Time:
        output['image']['date_and_time'] = self.datetime
        # Observation and illumination geometry:
        output['geometry_view_and_sun'] = self.geo
        # Target altitude:
        output['auxiliary_data']['target_altitude_km'] = target_altitude
        self.sixparam = output


