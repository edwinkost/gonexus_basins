#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

import pcraster as pcr


# code/name for the case area
code_name = "como"

# output folder (we will use this as our working folder as well)
output_folder = "/scratch/depfg/sutan101/gonexus_basin_case_studies/" + str(code_name) + "/"

# 'tmp' (temporary) folder within the output_folder
tmp_folder    = output_folder + "/tmp/"

# create output folder (as well as tmp folder )
cleanOutputDir = False
if cleanOutputDir and os.path.exist(output_folder):
    shutil.rmtree(output_folder)
if os.path.exists(output_folder) == False: os.makedirs(tmp_folder)
    

# go to the the output folder
os.chdir(output_folder)

# original input file provided by our partner
original_input_file = "/scratch/depfg/sutan101/data/gonexus_basins/extracted/como_and_zambezi/Como_model_mask.tif"

# output cell size at arcdeg resolution (as string)
cell_size_in_string = "0.08333333333333333333333333333333333333333333333333333"

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
cmd = 'gdalwarp -t_srs "+proj=longlat +ellps=WGS84" -tr ' + str(cell_size_in_string) + ' ' + str(cell_size_in_string) + ' -te -180 -90 180 90 ' + original_input_file + " " + os.path.basename(original_input_file) + ".tif"
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
# ~ pcr.aguila(basin_5min_original)
# - save the file as a nominal map
basin_5min_original_global_file_name = "basin_5min_original_" + str(code_name) + "_global.map" 
pcr.report(pcr.nominal(basin_5min_original), basin_5min_original_global_file_name) 


# define the basin according to pcrglobwb ldd
basin_5min_original_catchment_area_m2 = pcr.ifthen(basin_5min_original, catchment_area_m2)
basin_5min_pcrglobwb = pcr.ifthen(basin_5min_original_catchment_area_m2 == pcr.mapmaximum(basin_5min_original_catchment_area_m2), pcr.boolean(1.0))
basin_5min_pcrglobwb = pcr.catchment(ldd_map, basin_5min_pcrglobwb)
# ~ pcr.aguila(basin_5min_pcrglobwb)
# - extend five cells downstream
basin_5min_pcrglobwb_scalar  = pcr.scalar(basin_5min_pcrglobwb)
basin_5min_pcrglobwb_scalar += pcr.upstream(ldd_map, basin_5min_pcrglobwb_scalar)
basin_5min_pcrglobwb_scalar += pcr.upstream(ldd_map, basin_5min_pcrglobwb_scalar)
basin_5min_pcrglobwb_scalar += pcr.upstream(ldd_map, basin_5min_pcrglobwb_scalar)
basin_5min_pcrglobwb_scalar += pcr.upstream(ldd_map, basin_5min_pcrglobwb_scalar)
basin_5min_pcrglobwb_scalar += pcr.upstream(ldd_map, basin_5min_pcrglobwb_scalar)
basin_5min_pcrglobwb = pcr.ifthen(basin_5min_pcrglobwb_scalar > 0.0, pcr.boolean(1.0))
basin_5min_pcrglobwb = pcr.catchment(ldd_map, basin_5min_pcrglobwb)
basin_5min_pcrglobwb = pcr.ifthen(basin_5min_pcrglobwb, basin_5min_pcrglobwb)
# ~ pcr.aguila(basin_5min_pcrglobwb)
# - save the file as a nominal map
basin_5min_pcrglobwb_global_file_name = "basin_5min_pcrglobwb_" + str(code_name) + "_global.map" 
pcr.report(pcr.nominal(basin_5min_pcrglobwb), basin_5min_pcrglobwb_global_file_name) 


# get the bounding box coordinates
xmin, ymin, xmax, ymax = vos.boundingBox(basin_5min_pcrglobwb)
num_rows = int(round(ymax - ymin) / float(cell_size_in_string))
num_cols = int(round(xmax - xmin) / float(cell_size_in_string))

# create a local clone map and set the clone to it
clone_local_map_file = "clone_5min_" + str(code_name)  + ".map"
cmd = "mapattr -s -R %s -C %s -B -P yb2t -x %s -y %s -l %s %s" %(str(num_rows), str(num_cols), str(xmin), str(ymax), str(cell_size_in_string), clone_local_map_file)
print(cmd); os.system(cmd)
# - set the clone to this local map
pcr.setclone(clone_local_map_file)


# crop the original basin map
basin_5min_original_local  = vos.readPCRmapClone(v = basin_5min_original_global_file_name, \
                                                 cloneMapFileName = clone_local_map_file, \
                                                 tmpDir = tmp_folder, \
                                                 absolutePath = None, \
                                                 isLddMap = False, \
                                                 cover = None, \
                                                 isNomMap = True)
# save the original basin map
basin_5min_original_local_file_name = "basin_5min_original_" + str(code_name) + "_local.map" 
pcr.report(pcr.nominal(basin_5min_original_local), basin_5min_original_local_file_name) 

# crop the basin map based on pcrglobwb ldd
basin_5min_pcrglobwb_local = vos.readPCRmapClone(v = basin_5min_pcrglobwb_global_file_name, \
                                                 cloneMapFileName = clone_local_map_file, \
                                                 tmpDir = tmp_folder, \
                                                 absolutePath = None, \
                                                 isLddMap = False, \
                                                 cover = None, \
                                                 isNomMap = True)

# get the local ldd
ldd_map_local = pcr.lddrepair(pcr.ldd(vos.readPCRmapClone(v = ldd_map_file, \
                                                          cloneMapFileName = clone_local_map_file, \
                                                          tmpDir = tmp_folder, \
                                                          absolutePath = None, \
                                                          isLddMap = True, \
                                                          cover = None, \
                                                          isNomMap = False))
ldd_map_local = pcr.lddmask(ldd_map_local, basin_5min_pcrglobwb_local)
pcr.aguila(ldd_map_local)

                                                 
