# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 01:45:27 2023

@author: giannisps
"""

import numpy as np
from osgeo import gdal

# Define the path and filename of the multispectral image
multispectral_path = "/path/to/multispectral_image.tif"

# Define the path and filename of the panchromatic image
panchromatic_path = "/path/to/panchromatic_image.tif"

# Open the multispectral image and read the spectral bands as numpy arrays
multispectral_dataset = gdal.Open(multispectral_path, gdal.GA_ReadOnly)
red_band = multispectral_dataset.GetRasterBand(1).ReadAsArray().astype(np.float32)
green_band = multispectral_dataset.GetRasterBand(2).ReadAsArray().astype(np.float32)
blue_band = multispectral_dataset.GetRasterBand(3).ReadAsArray().astype(np.float32)

# Open the panchromatic image and read it as a numpy array
panchromatic_dataset = gdal.Open(panchromatic_path, gdal.GA_ReadOnly)
panchromatic_band = panchromatic_dataset.GetRasterBand(1).ReadAsArray().astype(np.float32)

# Perform pansharpening
pansharpened_red_band = red_band * (panchromatic_band / np.mean(panchromatic_band))
pansharpened_green_band = green_band * (panchromatic_band / np.mean(panchromatic_band))
pansharpened_blue_band = blue_band * (panchromatic_band / np.mean(panchromatic_band))

# Create a new GeoTIFF file to save the pansharpened image
driver = gdal.GetDriverByName("GTiff")
pansharpened_path = "/path/to/pansharpened_image.tif"
pansharpened_dataset = driver.Create(pansharpened_path, multispectral_dataset.RasterXSize, multispectral_dataset.RasterYSize, 3, gdal.GDT_Float32)

# Write the pansharpened bands to the new GeoTIFF file
pansharpened_dataset.GetRasterBand(1).WriteArray(pansharpened_red_band)
pansharpened_dataset.GetRasterBand(2).WriteArray(pansharpened_green_band)
pansharpened_dataset.GetRasterBand(3).WriteArray(pansharpened_blue_band)

# Set the projection and geotransform information of the new GeoTIFF file
pansharpened_dataset.SetProjection(multispectral_dataset.GetProjection())
pansharpened_dataset.SetGeoTransform(multispectral_dataset.GetGeoTransform())

# Close the datasets
multispectral_dataset = None
panchromatic_dataset = None
pansharpened_dataset = None