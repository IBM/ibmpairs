"""
IBM PAIRS IPython Notebook Magic for Pairs Query Language

Copyright 2021 IBM Weather Busines Solutions,
AI Applications Cloud and Cognitive Software
All Rights Reserved.

SPDX-License-Identifier: BSD-3-Clause
Note: Python3 only
"""
__maintainer__  = "Physical Analytics, TJ Watson Research Center"
__copyright__   = "(c) 2021, IBM Corp"
__authors__     = ['David Selby', 'Steffan Taylor',]
__email__       = "pairs@us.ibm.com"
__status__      = "Development"
__date__        = "Aug 2021"

from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic, line_cell_magic)
import re
import requests
import pandas as pd
import os
import math
import zipfile
import tempfile
import numpy as np
import rasterio
import PIL
import xarray as xr
from base64 import b64encode
from io import BytesIO, StringIO
import matplotlib as mpl
from matplotlib import pyplot as plt
from ipyleaflet import Map, ImageOverlay, basemap_to_tiles, basemaps, LayersControl
from copy import deepcopy
from rasterio.io import MemoryFile
from rasterio import Affine as A
from rasterio.warp import reproject, Resampling,calculate_default_transform as cdt
from pyproj import Transformer

@magics_class
class pqlMagic(Magics):

    def __init__(self, shell, debug=False, *args, **kwargs):
        super(pqlMagic, self).__init__(shell, debug=debug)
        self.regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
       r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        self.identifier = re.compile(r":[a-z|A-Z][a-z|A-Z|0-9]*", re.UNICODE)
        self.url = None
        self.headers = {'Content-Type': 'application/json'}
        print("pql loaded and available")

    def extract_zip(self,input_zip):
        input_zip=zipfile.ZipFile(BytesIO(input_zip))
        return {name: input_zip.read(name) for name in input_zip.namelist()}

    def getzoom(self,latMin,lngMin,latMax,lngMax):
        latDiff = latMax - latMin
        lngDiff = lngMax - lngMin

        maxDiff = latDiff
        if lngDiff > latDiff:
            maxDiff = lngDiff
        if (maxDiff < 360 / pow(2, 20)):
              zoomLevel = 18;
        else:
            zoomLevel = int((-1*( (math.log(maxDiff)/math.log(2)) - (math.log(360)/math.log(2)))))
            if zoomLevel < 1:
                 zoomLevel = 1
        return zoomLevel

    @line_cell_magic
    def pql(self, line, cell=None):
        """Magic entry point that works both as %pql and as %%pql"""
        if cell is None:
            if re.match(self.regex,line) is not None:
                self.url = line
                print("Set request url")
            else:
                print("Invalid URL specification")
            return None
        else:
            if self.url is None:
               print('Please specify connection url for PAIRS Service, example: %pql $url or %pql http:// ... ')
            else:
               while True:
                     match = re.search(self.identifier,cell)
                     if match:
                          name = match.group()[1:]
                          if name in self.shell.user_ns:
                               cell = cell[:match.start()] + self.shell.user_ns[name] + cell[match.end():]
                          else:
                               print("Error: " + name + " Not found in python namespace")
                               return  # !! Early bath
                     else:
                        break

               response = requests.post(self.url, headers=self.headers, data=cell, verify=False)

               if response.status_code == 200:
                   map_coords = None
                   print(response.headers['Content-Type'])
                   if response.headers['Content-Type'] == "application/gzip":
                       files = self.extract_zip(response.content)
                   else:
                       f = response.headers['Content-Disposition']
                       f = f[f.find('=')+1:]
                       files = {}
                       files[f] = response.content
                   #no_graphs = sum("statistics.csv" in x for x in files.keys())
                   themap = None
                   for key, value in files.items():
                       if "output.csv" in key:
                           temp = pd.read_csv(StringIO(value.decode()))
                           #temp['datestamp'] = pd.to_datetime(temp['datestamp'],format='%Y-%m-%d %H:%M:%S',yearfirst=True,errors='ignore')
                           vname = key[0:key.find('output.csv')-1]
                           if vname == "output.cs":
                                 vname = "output"
                           self.shell.user_ns.update({vname: temp})
                           print("created " + vname)
                       elif "statistics.csv" in key:
                           num_bins = 100
                           value = value.decode('utf-8')
                           lines = value.splitlines()
                           t = {}
                           y = []
                           x = []
                           i = 0
                           not_hdr = False
                           for line in lines:
                               l = line.split(',')
                               if not_hdr:
                                   if i > 1:
                                      y.append(float(l[2]))
                                      t[l[1].replace('"','')] = float(l[2])
                                      x.append(i-2)
                                   else:
                                      t[l[1].replace('"','')] = l[2].replace('"',"")
                                   i = i + 1
                               else:
                                   not_hdr = True
                           vname = key[0:key.find('.csv')]
                           desc = t["description"]
                           if desc == "null":
                                  desc = key[0:key.find("_")]
                           else:
                                  desc = desc + " (" + key[0:key.find("_")] + ")"
                           units = t["units"]
                           if units != "null":
                                  desc = desc + "[" + units + "] "
                           print( desc + ": min = " + str(y[0]) + ", q2 = " + str(y[24]) + ", median = " + str(y[49]) + ", q3 = " + str(y[74]) + ", max = " + str(y[100]) + ", mean = " + str(t["mean"]) + ", stddev = " + str(t["stddev"]) + ", valued rows = " + str(int(t["count_not_null"])))
                           self.shell.user_ns.update({vname: t})
                           print("created " + vname)
                           plt.style.use('fivethirtyeight')
                           plt.title(desc)
                           plt.xlabel("Percentiles")
                           plt.ylabel("Value")
                           plt.ylim(y[0],y[99])
                           plt.bar(x[0:99],y[0:99],color="blue",linewidth=1)
                           plt.show()
                           plt.close()
                       elif "count.csv" in key:
                           value = value.decode('utf-8')
                           lines = value.splitlines()
                           res = lines[1].split(',')
                           vname = res[0].replace('"','')
                           print( vname + ' has a count of ' + res[2])
                           vname = vname + '_' + res[1].replace('"','')
                           self.shell.user_ns.update({vname: int(res[2])})
                           print("created " + vname)
                       elif ".tif" in key:
                              with MemoryFile(value) as memfile:
                                   with memfile.open() as dataset:
                                        a = dataset.read()
                                        vname = key[0:key.find('.tif')] + "_img"
                                        self.shell.user_ns.update({vname : a})
                                        print("created " + vname)
                                        Input_CRS = { 'init' : 'EPSG:' + str( dataset.crs.to_epsg()) }
                                        # define the output coordinate system
                                        Output_CRS = {'init': "EPSG:3857"}
                                        # set up the transform
                                        transform, Width, Height = cdt(Input_CRS,Output_CRS,dataset.height,dataset.width,*dataset.bounds)
                                        kwargs = dataset.meta.copy()
                                        kwargs.update({
                                                       'crs': Output_CRS,
                                                       'transform': transform,
                                                       'width': Width,
                                                       'height': Height
                                                      })

                                        with MemoryFile() as memfile:
                                             with memfile.open(**kwargs) as destination:
                                                  reproject(
                                                              source=rasterio.band(dataset,1),
                                                              destination=rasterio.band(destination, 1),
                                                              src_transform=dataset.transform,
                                                              src_crs=dataset.crs,
                                                              dst_transform=transform,
                                                              dst_crs=Output_CRS,
                                                              resampling=Resampling.nearest)
                                                  acc_web = destination.read()
                                                  acc_web = acc_web.reshape(acc_web.shape[1:])
                                                  acc_norm = acc_web - np.nanmin(acc_web)
                                                  acc_norm = acc_norm / np.nanmax(acc_norm)
                                                  acc_norm = np.where(np.isfinite(acc_web), acc_norm, 0)
                                                  acc_im = PIL.Image.fromarray(np.uint8(plt.cm.jet(acc_norm)*255))
                                                  acc_mask = np.where(np.isfinite(acc_web), 255, 0)
                                                  mask = PIL.Image.fromarray(np.uint8(acc_mask), mode='L')
                                                  im = PIL.Image.new('RGBA', acc_norm.shape[::-1], color=None)
                                                  im.paste(acc_im, mask=mask)
                                                  f = BytesIO()
                                                  im.save(f, 'png')
                                                  data = b64encode(f.getvalue())
                                                  data = data.decode('ascii')
                                                  imgurl = 'data:image/png;base64,' + data
                                                  b = dataset.bounds
                                                  transformer = Transformer.from_crs(dataset.crs, "EPSG:4326")
                                                  bounds = [transformer.transform(b.left, b.bottom), transformer.transform(b.right, b.top)]
                                                  if themap is None:
                                                      zoom = self.getzoom(bounds[0][0],bounds[0][1],bounds[1][0],bounds[1][1])
                                                      cy = b.bottom + ((b.top-b.bottom)/2)
                                                      cx = b.left + ((b.left-b.right)/2)
                                                      center = transformer.transform(cx, cy)
                                                      themap = Map(center=center, zoom=zoom, interpolation='nearest')
                                                      themap.add_control(LayersControl(position='topright'))
                                                      tile = basemap_to_tiles(basemaps.Esri.WorldStreetMap)
                                                      themap.add_layer(tile)
                                                  imgo = ImageOverlay(name=key[0:key.find('.tif')],url=imgurl, bounds=bounds)
                                                  imgo.interact(opacity=(0.0,1.0,0.01))
                                                  themap.add_layer(imgo)
                       elif "error.msg" == key:
                             print(value.decode())
                       elif ".nc" in key:
                              with MemoryFile(value) as cdffile:
                                   xrda = xr.open_dataset(cdffile)
                                   vname = key[0:key.find('.nc')] + "_netcdf"
                                   self.shell.user_ns.update({vname : xrda})
                                   print("Created " + vname)

                   if themap is not None:
                         display(themap)
               else:
                   print(response.text)

            return
