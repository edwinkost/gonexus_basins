#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess

import pcraster as pcr

# output folder (we will use this as our working folder as well)
output_folder = "/scratch/depfg/sutan101/gonexus_basin_case_studies/como/"

# create output folder
cleanOutputDir = False
if cleanOutputDir and os.path.exist(output_folder):
    shutil.rmtree(output_folder)
if os.path.exist(output_folder) == False: os.makedirs(output_folder)

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

# convert the original input file to 5 arcmin resolution at the global extent, and read it
cmd = 'gdalwarp -t_srs "+proj=longlat +ellps=WGS84" -tr 0.08333333333333333333333333333333333333333333333333333 0.08333333333333333333333333333333333333333333333333333 -te -180 -90 180 90 ' + os.path.basename(original_input_file) + " " + os.path.basename(original_input_file) + ".tif"
print(cmd); subprocess.run(cmd.split(), check = True)


# - convert to map
cmd = 'gdal_translate -of PCRaster ' + os.path.basename(original_input_file) + ".tif " + os.path.basename(original_input_file) + ".tif.map"
print(cmd); subprocess.run(cmd.split(), check = True)
# - make sure that its mapattr consistent with clone_map
cmd = 'mapattr -c ' + clone_map + " " + os.path.basename(original_input_file) + ".tif.map"
print(cmd); subprocess.run(cmd.split(), check = True)
# - read the map
basin_5min_original = pcr.readmap(os.path.basename(original_input_file) + ".tif.map")
pcr.aguila(basin_5min_original) 


