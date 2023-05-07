#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 09:45:38 2023

@author: evanchladny
"""

import xarray as xr
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from cartopy import crs as ccrs
import imageio

#Opens data files

fname='./Data/Wind_Data'
w_ds=xr.open_dataset(fname)

fname = './Data/Pressure_Data'
p_ds=xr.open_dataset(fname)

########## Wind Speed and Pressure ##########

#Creates a new array for future GIF

wind_frames = []

#For loop to run through each timestep and create the plots

for i in range(2,12):
    
    #Creates the map
    
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines(resolution='50m')
    ax.add_feature(cfeature.STATES)
    central_lon, central_lat = 98, 39.5
    extent = [-105, -90, 44.5, 34.5]
    ax.set_extent(extent)
    
    #Generates a timestamp for each plot title
    
    unix_timestamp = w_ds['time'][i].item()/ 1e9
    time = datetime.fromtimestamp(unix_timestamp)
    title_str = time.strftime('%Y-%m-%d %H:%M:%S')
    
    #Adds all the information onto the figure

    plt.title('Wind and Pressure: ' + title_str)

    wind = 2.237*np.sqrt((w_ds['u10'][i,:,:]*w_ds['u10'][i,:,:]) + (w_ds['v10'][i,:,:]*w_ds['v10'][i,:,:]))

    cs = ax.contourf(w_ds['longitude'], 
                      w_ds['latitude'], 
                      wind,
                      transform = ccrs.PlateCarree(),extend='both', cmap = 'inferno_r', levels = [25, 30, 35, 40, 45, 50, 55], alpha = 0.6)

    ax.barbs(w_ds['longitude'][::6], w_ds['latitude'][::6], w_ds['u10'][i, ::6, ::6], w_ds['v10'][i, ::6, ::6], length = 6)

    cbar = plt.colorbar(cs,orientation='horizontal', label = '10-m Wind speed [mph]', shrink = .5, pad = 0.05)
    
    ax.contour(p_ds['longitude'], p_ds['latitude'], p_ds['msl'][i,:,:], 20)
    
    #Saves each figure to the output folder along with adding them to the array
    
    plt.savefig('Output/Images/Winds ' + title_str + '.png', bbox_inches='tight', dpi=400)
    
    image = imageio.v2.imread('Output/Images/Winds ' + title_str + '.png')
    wind_frames.append(image)
    
    plt.show()

#Generates the GIF

imageio.mimsave('./Output/GIFs/Full_Event_Winds.gif',
            wind_frames,
            fps = 1)

########## Wind Gusts and Pressure ##########

#Opens data set for wind gusts

fname = './Data/Wind_Gusts'
g_ds=xr.open_dataset(fname)

#Creates a new array for future GIF

gusts_frames = []

for i in range(2,12):
    
    #Creates the map
    
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines(resolution='50m')
    ax.add_feature(cfeature.STATES)
    central_lon, central_lat = 98, 39.5
    extent = [-105, -90, 44.5, 34.5]
    ax.set_extent(extent)
    
    #Generates a timestamp for each plot
    
    unix_timestamp = w_ds['time'][i].item()/ 1e9
    time = datetime.fromtimestamp(unix_timestamp)
    title_str = time.strftime('%Y-%m-%d %H:%M:%S')
    
    #Adds all the information onto the figure

    plt.title('Wind Gusts and Pressure: ' + title_str)

    wind = 2.237*np.sqrt((g_ds['i10fg'][i,:,:]*g_ds['i10fg'][i,:,:]) + (g_ds['i10fg'][i,:,:]*g_ds['i10fg'][i,:,:]))

    cs = ax.contourf(g_ds['longitude'], 
                      g_ds['latitude'], 
                      wind,
                      transform = ccrs.PlateCarree(),extend='both', cmap = 'inferno_r', levels = [50, 60, 70, 80, 90, 100], alpha = 0.6)
    
    cbar = plt.colorbar(cs,orientation='horizontal', label = '10-m Wind gust speed [mph]', shrink = .5, pad = 0.05)
    
    ax.contour(p_ds['longitude'], p_ds['latitude'], p_ds['msl'][i,:,:], 20)
    
    #Highlights the 100mph+ contour
    
    ax.contour(g_ds['longitude'], 
               g_ds['latitude'], 
               wind, 
               colors = 'red', levels = [100])
    
    #Creates non-magnitude directional arrows
    
    wind_directions = np.arctan2(w_ds['v10'][i, ::6, ::6], w_ds['u10'][i, ::6, ::6])
    
    u = np.cos(wind_directions)
    v = np.sin(wind_directions)

    ax.quiver(w_ds['longitude'][::6], w_ds['latitude'][::6], u, v, scale = 25)
    
    #Saves each figure to the output folder along with adding them to the array
    
    plt.savefig('Output/Images/Gusts ' + title_str + '.png', bbox_inches='tight', dpi=400)
    
    image = imageio.v2.imread('Output/Images/Gusts ' + title_str + '.png')
    gusts_frames.append(image)
    
    plt.show()
    
#Generates the GIF
    
imageio.mimsave('./Output/GIFs/Full_Event_Gusts.gif',
            gusts_frames,
            fps = 1)
