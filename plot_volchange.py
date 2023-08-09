import rasterio
import pandas as pd

band_id = 1
def target(raster_name):
  raster = rasterio.open(raster_name)
  band_arr = raster.read(band_id)
  target_elevation = []
  for i in range(band_arr.shape[0]):
    for j in range(band_arr.shape[1]):
      # filter Nodata value -9999
      if band_arr[i ,j] < -0.1 and band_arr[i ,j] > -1000:
        target_elevation.append(band_arr[i ,j])
      else:
        continue
  return target_elevation

t1 = target('period1.tif')
t2 = target('peroid2.tif')
t3 = target('peroid3.tif')

t1_yr = []
t2_yr = []
t3_yr = []
t1_v = []
t2_v = []
t3_v = []
for i in t1:
  t1_yr.append("2010~2022/10/21")
  t1_v.append(-8.15)
for i in t2:
  t2_yr.append("2022/10/21~2023/03/17")
  t2_v.append(-2.348)
for i in t3:
  t3_yr.append("2023/03/17~2023/07/13")
  t3_v.append(-1.094)

pd.options.display.float_format = '{:.3f}'.format
df_plot = pd.DataFrame(t1, columns=["elevation_diff"])

df_plot.insert(1,"date", t1_yr)
df_plot.insert(2,"volume", t1_v)
df_plot2 = pd.DataFrame(t2, columns=["elevation_diff"])
df_plot2.insert(1,"date", t2_yr)
df_plot2.insert(2,"volume", t2_v)
df_plot3 = pd.DataFrame(t3, columns=["elevation_diff"])
df_plot3.insert(1,"date", t3_yr)
df_plot3.insert(2,"volume", t3_v)
df_plot = df_plot.append(df_plot2, ignore_index=True)
df_plot = df_plot.append(df_plot3, ignore_index=True)
df_plot

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

plt.figure(dpi=150)
sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(10, 4))
sns.boxplot(x="date", y="elevation_diff", data=df_plot, ax=ax, color="navajowhite", fliersize=0)
sns.pointplot(data=df_plot, x='date', y='volume', color="coral", ax=ax, ci=None, dodge=.5 - .5/4, scale=0.65)
plt.legend(loc='lower right', labels=["Elevation Difference","Mean"])
plt.ylabel("Elevation Difference",fontsize=10)
plt.xlabel("Date",fontsize=10)

y_major_locator=MultipleLocator(2)
ax=plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
plt.ylim(-22, 0)
plt.show()   #To see the output plot plz find "plot_volchange.png"