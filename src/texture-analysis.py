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

if __name__ == '__main__':
    path = "data/"
    data = collect_data(path)
