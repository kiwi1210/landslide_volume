# calculate volume without outliers
band_id = 1
def volume_2nd(raster_name):
  raster = rasterio.open(raster_name)
  band_arr = raster.read(band_id)
  total = band_arr.flatten()
  delete = []
  for index in range(len(total)):
    # filter Nodata value -9999
    if total[index] < -1000:
      delete.append(index)
      
  total = np.delete(total, delete)
  Q1 = np.percentile(total , 25)
  Q3 = np.percentile(total , 75)
  
  # Find IQR, upper limit, lower limit
  IQR = Q3 - Q1
  upper = Q3+1.5*IQR
  lower = Q1-1.5*IQR
  
  #calculate volume without outliers
  positive = []
  negative = []
  for i in range(band_arr.shape[0]):
    for j in range(band_arr.shape[1]):
      if band_arr[i ,j] > 0 and band_arr[i ,j] < upper:
        positive.append(band_arr[i ,j])
      elif band_arr[i ,j] < 0 and band_arr[i ,j] > lower:
        negative.append(band_arr[i ,j])
      else:
        continue

  gain = sum(positive)*4
  loss = sum(negative)*4
  result = []
  result.append(gain)
  result.append(loss)
  return result
