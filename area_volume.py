##calculate landslide area
import rasterio
import pandas as pd
import numpy as np
import statistics

band_id = 1
#select pixels' value smaller then -0.1 (i.e. erosion)
def area_01(raster_name):
  raster = rasterio.open(raster_name)
  band_arr = raster.read(band_id)
  target = []
  for i in range(band_arr.shape[0]):
    for j in range(band_arr.shape[1]):
      # filter Nodata value -9999
      if band_arr[i ,j] < -0.1  and band_arr[i ,j] > -1000:
        target.append(band_arr[i ,j])
      else:
        continue
  area = len(target)*4
  area_mean = sum(target)/len(target)
  area_median = statistics.median(target)
  return area, area_mean, area_median

#select pixels' value smaller then -10 (i.e. deep erosion)
def area_010(raster_name):
  raster = rasterio.open(raster_name)
  band_arr = raster.read(band_id)
  target = []
  for i in range(band_arr.shape[0]):
    for j in range(band_arr.shape[1]):
      # filter Nodata value -9999
      if band_arr[i ,j] < -10 and band_arr[i ,j] > -1000:
        target.append(band_arr[i ,j])
      else:
        continue
  area = len(target)*4
  area_mean = sum(target)/len(target)
  area_median = statistics.median(target)
  return area, area_mean, area_median

## calculate landslide volume
def volume(raster_name):
  raster = rasterio.open(raster_name)
  band_arr = raster.read(band_id)
  positive = []
  negative = []
  for i in range(band_arr.shape[0]):
    for j in range(band_arr.shape[1]):
      if band_arr[i ,j] > 0:
        positive.append(band_arr[i ,j])
      elif band_arr[i ,j] < -0.1 and band_arr[i ,j] > -1000:
        negative.append(band_arr[i ,j])
      else:
        continue
  gain = sum(positive)*4
  loss = sum(negative)*4
  result = []
  result.append(gain)
  result.append(loss)
  return result

area1 = area_01('filename.tif')
area2 = area_01('filename.tif')
area3 = area_01('filename.tif')

area10 = area_010('filename.tif')
area20 = area_010('filename.tif')
area30 = area_010('filename.tif')

#put result into a data frame, and only show 3 decimal places
pd.options.display.float_format = '{:.3f}'.format
result_df = pd.DataFrame(np.array([area1, area10, area2, area20, area3, area30]),
                   columns=['area','mean','median'])
                   

vol1 = volume('filename.tif')
vol2 = volume('filename.tif')
vol3 = volume('filename.tif')
pd.options.display.float_format = '{:.5f}'.format
result_df = pd.DataFrame(np.array([vol1, vol2, vol3]), columns=['gain', 'loss'])
