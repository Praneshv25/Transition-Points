"""
Module contains functions to read and write csv files. It also contains a function to download files
Author: Pranesh Velmurugan praneshsvels@gmail.com
Date: 8/5/24
"""

import csv
import os
import shutil

import Conversions
from Point import Point, TypePoint


def read_csv(filename, points_dict):
    """
    Reads file and fills up points_dict with Point objects
    :param filename: Csv file names
    :param points_dict: dictionary to fill with Point objects
    :return: populated points_dict
    """
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skips headers
        try:
            for row in reader:
                rgt, type_point, latitude, longitude = int(row[0]), int(row[2]), float(row[3]), float(row[4])
                asc_req = int(row[5])

                state = TypePoint.RGT if type_point == 0 else TypePoint.VEGETATION

                point = Point(rgt, state, latitude, longitude, asc_req)
                points_dict[rgt].append(point)
            return points_dict
        except Exception as e:
            print(e)
            print('CSV File format invalid')
            return None


def write_csv(filename, points_dict):
    """
    Writes file with the RGT number, State, latitude, longitude, asc_req
    :param filename: file name to write to
    :param points_dict: dictionary to get information from
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['rgt', 'trans_type', 'lat', 'lon', 'asc_req'])
        for rgt in points_dict:
            for point in points_dict[rgt]:
                gcs_coords = Conversions.cartesian_to_gcs(point.longitude, point.latitude)
                writer.writerow([point.rgt, point.state.value, gcs_coords[1], gcs_coords[0], point.asc_req])


def download_files(files_destination):
    """
    Function download the Transition Points file and the Warnings file to file_destination
    :param files_destination: Directory to download files to
    """
    source_directory = os.path.join(os.getcwd(), "assets")
    files = ['new_points.csv', 'warnings.txt']
    for filename in files:
        source_path = os.path.join(source_directory, filename)
        destination_path = os.path.join(files_destination, filename)
        shutil.copy(source_path, destination_path)
