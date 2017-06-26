# RPi Meteor Station
# Copyright (C) 2017  Denis Vida
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Generates a plot with all intensities from fieldsum files. """


import os
import sys

import numpy as np

import matplotlib.pyplot as plt

import RMS.ConfigReader as cr
from RMS.Formats.FieldIntensities import readFieldIntensitiesBin
from RMS.Formats.FFbin import filenameToDatetime


def plotFieldsums(dir_path, config):
    """ Plots a graph of all intensity sums from FS*.bin files in the given directory. 
    
    Arguments:
        dir_path: [str] Path to the directory which containes the FS*.bin files.
        config: [Config structure] Configuration.

    Return:
        None
    """

    time_data = []
    intensity_data_peak = []
    intensity_data_avg = []

    # Get all fieldsum files in the directory
    for file_name in sorted(os.listdir(dir_path)):

        # Check if it is the fieldsum file
        if ('FS' in file_name) and ('_fieldsum.bin' in file_name):

            # Read the field sums
            half_frames, intensity_array = readFieldIntensitiesBin(dir_path, file_name)

            # Extract the date and time from the FF file
            dt = filenameToDatetime(file_name)

            # Take the peak intensity value
            intensity_data_peak.append(np.max(intensity_array))

            # Take the average intensity value
            intensity_data_avg.append(np.mean(intensity_array))


            time_data.append(dt)




    ### Plot the raw intensity over time ###
    ##########################################################################################################
    
    # Plot peak intensitites
    plt.plot(time_data, intensity_data_peak, color='r', linewidth=0.5, zorder=3, label='Peak')

    # Plot average intensitites
    plt.plot(time_data, intensity_data_avg, color='k', linewidth=0.5, zorder=3, label='Average')

    plt.gca().set_yscale('log')

    plt.xlim(np.min(time_data), np.max(time_data))
    plt.ylim(np.min(intensity_data_avg), np.max(intensity_data_peak))

    plt.xlabel('Time')
    plt.ylabel('ADU')

    plt.grid(color='0.9', which='both')

    plt.title('Peak field sums for ' + os.path.basename(dir_path))

    plt.tight_layout()

    plt.legend()


    plt.savefig(os.path.join(dir_path, os.path.basename(dir_path) + '_fieldsums.png'), dpi=300)

    plt.clf()
    plt.close()

    ##########################################################################################################


    ### Plot intensities without the average value
    ##########################################################################################################

    intensity_data_peak = np.array(intensity_data_peak)
    intensity_data_avg = np.array(intensity_data_avg)

    # Calculate the difference between the peak values and the average values per every FF file
    intensity_data_noavg = intensity_data_peak - intensity_data_avg


    plt.plot(time_data, intensity_data_noavg, color='k', linewidth=0.5, zorder=3)

    plt.gca().set_yscale('log')

    plt.xlim(np.min(time_data), np.max(time_data))

    plt.xlabel('Time')
    plt.ylabel('Peak ADU - average')

    plt.grid(color='0.9', which='both')

    plt.title('Deaveraged field sums for ' + os.path.basename(dir_path))

    plt.tight_layout()


    plt.savefig(os.path.join(dir_path, os.path.basename(dir_path) + '_fieldsums_noavg.png'), dpi=300)

    plt.clf()
    plt.close()


    ##########################################################################################################






if __name__ == "__main__":


    # Load config file
    config = cr.parse(".config")


    if len(sys.argv) < 2:
        print('Usage: python -m Utils.PlotFieldsums /dir/with/FS/files')

        sys.exit()


    # Read the argument as a path to the night directory
    dir_path = " ".join(sys.argv[1:])

    plotFieldsums(dir_path, config)

