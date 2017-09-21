#!/usr/bin/env python
"""
==================================================
Texture-Based Transfer Function
==================================================
@author: Radhika Mattoo, http://www.github.com/radhikamattoo
@organization: MediVis, Inc.
@contact: rm3485@nyu.edu

Reference:
Jesus J. Caban et al., "Texture-based Transfer Functions for Direct Volume Rendering",
IEEE Transactions On Visualization and Computer Graphics November/December 2008
"""
print(__doc__)
import time
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy
import dicom

RHO = 2
SIGMA = 4

def collect_data(data_path):
    print "collecting data"
    files = []  # create an empty list
    for dirName, subdirList, fileList in os.walk(data_path):
        for filename in fileList:
            if ".dcm" in filename:
                files.append(os.path.join(dirName,filename))
    # Get reference file
    ref = dicom.read_file(files[0])

    # Load dimensions based on the number of rows, columns, and slices (along the Z axis)
    pixel_dims = (int(ref.Rows), int(ref.Columns), len(files))

    # Load spacing values (in mm)
    pixel_spacings = (float(ref.PixelSpacing[0]), float(ref.PixelSpacing[1]), float(ref.SliceThickness))

    x = np.arange(0.0, (pixel_dims[0]+1)*pixel_spacings[0], pixel_spacings[0])
    y = np.arange(0.0, (pixel_dims[1]+1)*pixel_spacings[1], pixel_spacings[1])
    z = np.arange(0.0, (pixel_dims[2]+1)*pixel_spacings[2], pixel_spacings[2])

    # Row and column directional cosines
    orientation = ref.ImageOrientationPatient

    # This will become the intensity values
    dcm = np.zeros(pixel_dims, dtype=ref.pixel_array.dtype)

    origins = []

    # loop through all the DICOM files
    for filename in files:
        # read the file
        ds = dicom.read_file(filename)
        #get pixel spacing and origin information
        origins.append(ds.ImagePositionPatient) #[0,0,0] coordinates in real 3D space (in mm)

        # store the raw image data
        dcm[:, :, files.index(filename)] = ds.pixel_array
    return dcm, origins, pixel_spacings, orientation
def partition_data(data):
    print "partitioning data"
    # variables for separating data into subvolumes
    voxelSpread = RHO + SIGMA
    subvolumeSize = voxelSpread ** 3
    numSlicesPerVolume = subvolumeSize/voxelSpread

    rows, cols, slices = data.shape
    subvolumes = []
    # FIXME
    it = np.nditer(data, flags=['multi_index'])
    for slice in range(0,slices, numSlicesPerVolume):
        for row in range(0,rows):
            for col in range(0, cols,RHO): #Rho is region size
                # val = data[row,col,slice]
                subvolume_coordinates = find_subvolume_coordinates([row,col,slice], voxelSpread,subvolumeSize,numSlicesPerVolume, data.shape)
                subvolumes.push(subvolume_coordinates)
    return subvolumes

def find_subvolume_coordinates(currentIdx, voxelSpread, subvolumeSize, numSlicesPerVolume, dataShape):
    coordinates = [currendIdx]
    # FIXME
    # rowLength, colLength, sliceLength = dataShape
    # # correct for off-by-one errors
    # rowLength -=1
    # colLength -= 1
    # sliceLength -= 1
    # center_x, center_y, center_z = currentIdx
    #
    # # Left edge
    # if center_y == 0:
    #     if center_x == 0:
    #         print "top left corner"
    #         for slice in range(center_z,(center_z + numSlicesPerVolume)):
    #
    #     else if center_x == rowLength:
    #         print "bottom left corner"
    #     else:
    #         print "generic left side cell"
    #
    # # Right edge
    # # Bottom edge
    # # Top edge
    return []

def first_order_statistics(data):
    print "computing first order statistics"
    maximum = np.max(data)
    pixelCount = np.zeros((maximum+1), dtype=np.int32) #prevent off-by-1

    # iterate through data and count number of unique pixel values
    it = np.nditer(data, flags=['multi_index'])
    while not it.finished:
        x,y,z = it.multi_index
        value = data[x,y,z]
        pixelCount[value] += 1
        it.iternext()
    # compute probability of an intensity being in a subvolume
    subvolumeSize = np.square((RHO+SIGMA))
    histogram = np.empty((maximum+1), dtype=np.float32)

    count = 0
    for pixel in pixelCount:
        probability = pixel/subvolumeSize
        histogram[count] = probability
        count += 1
    print histogram
    return histogram

if __name__ == '__main__':
    path = "data/"
    data, origins, pixel_spacings, orientation = collect_data(path)
    partitions = partition_data(data)
    for subvolume in partition:
        first_order_statistics(subvolume)
