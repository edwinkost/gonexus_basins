#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

import pcraster as pcr

# output folder (we will use this as our working folder as well)
output_folder = "/scratch/depfg/sutan101/gonexus_basin_case_studies/como/"

# create output folder
cleanOutputDir = False
if cleanOutputDir and os.path.exist(output_folder):
    shutil.rmtree(output_folder)
if os.path.exists(output_folder) == False: os.makedirs(output_folder)

# go to the the output folder
os.chdir(output_folder)

# original input file provided by our partner
original_input_file = "/scratch/depfg/sutan101/data/gonexus_basins/extracted/como_and_zambezi/Como_model_mask.tif"

# ldd and cell area maps
ldd_map_file   = "/scratch/depfg/sutan101/data/pcrglobwb_input_aqueduct/version_2021-09-16/general/lddsound_05min_version_20210330.map"
cell_area_file = "/scratch/depfg/sutan101/data/pcrglobwb_input_aqueduct/version_2021-09-16/general/cdo_gridarea_clone_global_05min_correct_lats.nc.map"

# - set clone at the global extent
clone_map = ldd_map_file
pcr.setclone(clone_map)

# read ldd and calculate catchment area (m2)
ldd_map           = pcr.lddrepair(pcr.ldd(pcr.readmap(ldd_map_file)))
cell_area_m2      = pcr.readmap(cell_area_file)
catchment_area_m2 = pcr.catchmenttotal(cell_area_m2, ldd_map)


# convert the original basin input file to 5 arcmin resolution at the global extent, and read it
cmd = 'gdalwarp -t_srs "+proj=longlat +ellps=WGS84" -tr 0.08333333333333333333333333333333333333333333333333333 0.08333333333333333333333333333333333333333333333333333 -te -180 -90 180 90 ' + original_input_file + " " + os.path.basename(original_input_file) + ".tif"
print(cmd); os.system(cmd)
# - convert to map
cmd = 'gdal_translate -of PCRaster ' + os.path.basename(original_input_file) + ".tif " + os.path.basename(original_input_file) + ".tif.map"
print(cmd); os.system(cmd)
# - make sure that its mapattr consistent with clone_map
cmd = 'mapattr -c ' + clone_map + " " + os.path.basename(original_input_file) + ".tif.map"
print(cmd); os.system(cmd)
# - read the map
basin_5min_original = pcr.boolean(pcr.readmap(os.path.basename(original_input_file) + ".tif.map"))
basin_5min_original = pcr.ifthen(basin_5min_original, basin_5min_original)
pcr.aguila(basin_5min_original) 


# define the basin according to pcrglobwb ldd
basin_5min_original_catchment_area_m2 = pcr.ifthen(basin_5min_original, catchment_area_m2)
basin_5min_pcrglobwb = pcr.ifthen(basin_5min_original_catchment_area_m2 == pcr.mapmaximum(basin_5min_original_catchment_area_m2), pcr.boolean(1.0))
basin_5min_pcrglobwb = pcr.catchment(ldd_map, basin_5min_pcrglobwb)
pcr.aguila(basin_5min_pcrglobwb)
# ~ # - extend five cells downstream
# ~ basin_5min_pcrglobwb_scalar  = pcr.scalar(basin_5min_pcrglobwb)
# ~ basin_5min_pcrglobwb_scalar += pcr.upstream(ldd_map, basin_5min_pcrglobwb_scalar)
# ~ basin_5min_pcrglobwb_scalar += pcr.upstream(ldd_map, basin_5min_pcrglobwb_scalar)
# ~ basin_5min_pcrglobwb_scalar += pcr.upstream(ldd_map, basin_5min_pcrglobwb_scalar)
# ~ basin_5min_pcrglobwb_scalar += pcr.upstream(ldd_map, basin_5min_pcrglobwb_scalar)
# ~ basin_5min_pcrglobwb_scalar += pcr.upstream(ldd_map, basin_5min_pcrglobwb_scalar)
# ~ pcr.aguila(basin_5min_pcrglobwb_scalar)
