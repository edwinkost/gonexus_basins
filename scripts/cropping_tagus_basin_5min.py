#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

import pcraster as pcr

import virtualOS as vos

import edwin_tools as etls

# code/name for the case area
code_name = "tagus"

# original input file provided by our partner
original_input_file = "/scratch/depfg/sutan101/data/gonexus_basins/extracted/Tagus/shp/tagus_3sec.tif"

# output folder (we will use this as our working folder as well)
output_folder = "/scratch/depfg/sutan101/gonexus_basin_case_studies/version_2024-03-28/" + str(code_name) + "/"
# ~ output_folder = "/scratch/depfg/sutan101/gonexus_basin_case_studies/test/" + str(code_name) + "/"

# 'tmp' (temporary) folder within the output_folder
tmp_folder    = output_folder + "/tmp/"

# create output folder (as well as tmp folder )
cleanOutputDir = False
if cleanOutputDir and os.path.exist(output_folder):
    shutil.rmtree(output_folder)
if os.path.exists(output_folder) == False or os.path.exists(tmp_folder) == False: os.makedirs(tmp_folder)

# go to the the output folder
os.chdir(output_folder)

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
basin_5min_pcrglobwb_local_file_name = "basin_5min_pcrglobwb_" + str(code_name) + "_local.map" 
pcr.report(pcr.nominal(basin_5min_pcrglobwb_local), basin_5min_pcrglobwb_local_file_name) 

# get the local ldd
ldd_map_local = pcr.lddrepair(pcr.ldd(vos.readPCRmapClone(v = ldd_map_file, \
                                                          cloneMapFileName = clone_local_map_file, \
                                                          tmpDir = tmp_folder, \
                                                          absolutePath = None, \
                                                          isLddMap = True, \
                                                          cover = None, \
                                                          isNomMap = False)))
ldd_map_local = pcr.lddmask(ldd_map_local, pcr.defined(basin_5min_pcrglobwb_local))
ldd_map_local_file_name = "ldd_5min_pcrglobwb_" + str(code_name) + "_local.map"
pcr.report(ldd_map_local, ldd_map_local_file_name) 


# calculate strahler order (local)
strahler_order_local = pcr.streamorder(ldd_map_local)
strahler_order_local_file_name = "strahler_order_5min_pcrglobwb_" + str(code_name) + "_local.map"
pcr.report(strahler_order_local, strahler_order_local_file_name) 


# get the local cell area (unit: m2) for calculating catchment area in m2 (based on pcrglobwb)
cell_area_m2_local = vos.readPCRmapClone(v = cell_area_file, \
                                         cloneMapFileName = clone_local_map_file, \
                                         tmpDir = tmp_folder, \
                                         absolutePath = None, \
                                         isLddMap = False, \
                                         cover = None, \
                                         isNomMap = False)
cell_area_m2_local_file_name = "cell_area_m2_5min_pcrglobwb_" + str(code_name) + "_local.map"
pcr.report(cell_area_m2_local, cell_area_m2_local_file_name) 


# calculate catchment area in m2 (local)
catchment_area_m2_local = pcr.catchmenttotal(cell_area_m2_local, ldd_map_local)
catchment_area_m2_local_file_name = "catchment_area_m2_5min_pcrglobwb_" + str(code_name) + "_local.map"
pcr.report(catchment_area_m2_local, catchment_area_m2_local_file_name) 


# convert the pcrglobwb-based basin map to a netcdf file
cmd = 'gdal_translate -of NETCDF ' + basin_5min_pcrglobwb_local_file_name + " basin_pgb.nc"
print(cmd); os.system(cmd)
# - do cdo invertlat in order to flip y coordinates so that it will be consitent to our netcdf files
cmd = 'cdo -L -f nc4 -invertlat basin_pgb.nc basin_pgb_invertlat.nc'
print(cmd); os.system(cmd)
mask = "basin_pgb_invertlat.nc"


# pcrglobwb_human_output files
pcrglobwb_human_output_folder = "/depfg/sutan101/pcrglobwb_wri_aqueduct_2021/pcrglobwb_aqueduct_2021_monthly_annual_files/version_2021-09-16_merged/gswp3-w5e5/historical-reference/"
nc_input_files = [
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_precipitation_global_monthly-total_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_temperature_global_monthly-average_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_totalEvaporation_global_monthly-total_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_nonIrrWaterConsumption_global_monthly-total_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_actualET_global_monthly-total_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_evaporation_from_irrigation_global_monthly-total_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_transpiration_from_irrigation_global_monthly-total_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_directRunoff_global_monthly-total_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_interflowTotal_global_monthly-total_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_baseflow_global_monthly-total_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_gwRecharge_global_monthly-total_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_surfaceWaterInf_global_monthly-total_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_totalRunoff_global_monthly-total_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_snowCoverSWE_global_monthly-average_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_snowFreeWater_global_monthly-average_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_interceptStor_global_monthly-average_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_storUppTotal_global_monthly-average_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_storLowTotal_global_monthly-average_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_storGroundwater_global_monthly-average_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_storGroundwaterFossil_global_monthly-average_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_surfaceWaterStorage_global_monthly-average_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_totalWaterStorageThickness_global_monthly-average_1960_2019_basetier1.nc",
"pcrglobwb_cmip6-isimip3-gswp3-w5e5_image-aqueduct_historical-reference_discharge_global_monthly-average_1960_2019_basetier1.nc"
]
for nc_input_file in nc_input_files:
    
    # input file name
    inp_file_name = pcrglobwb_human_output_folder + "/" + nc_input_file
    
    # output file name
    out_file_name = nc_input_file.replace("global", str(code_name))
    out_file_name = out_file_name.replace("gswp3-w5e5", "w5e5")
    out_file_name = out_file_name.replace("1960_2019", "1980_2019")

    # cropping to the model region
    etls.cdo_crop_file_1980_2019(inp_file_name, mask, xmin, xmax, ymin, ymax, out_file_name)


# streamflow naturalized
pcrglobwb_natur_output_folder = "/scratch/depfg/sutan101/pcrglobwb_aqueduct_2021_naturalized/version_2021-09-16_naturalized/gswp3-w5e5/historical-reference/selected_1979-2019/"
inp_file_name = pcrglobwb_natur_output_folder + "/" + "discharge_monthAvg_output_1979-2019_setgrid.nc"
out_file_name = "pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_" + "discharge-naturalized_" + str(code_name) + "_monthly-average_1980_2019_basetier1.nc"
etls.cdo_crop_file_1980_2019(inp_file_name, mask, xmin, xmax, ymin, ymax, out_file_name)


# ~ sutan101@node033.cluster:/scratch/depfg/sutan101/dynqual_output_from_duncan/1980-2019$ ls -lah *.nc
# ~ -r--r--r-- 1 sutan101 depfg 100G Mar 27 14:09 discharge_dailyTot_output_1980-2019.nc
# ~ -r--r--r-- 1 sutan101 depfg  54G Mar 27 12:41 waterTemp_dailyTot_output_1980-2019.nc

# dynqual water temperature - monthly average
dynqual_output_folder = "/scratch/depfg/sutan101/dynqual_output_from_duncan/1980-2019/" 
inp_file_name = dynqual_output_folder + "/" + "waterTemp_dailyTot_output_1980-2019.nc"
out_file_name = "pcrglobwb_dynqual_cmip6-isimip3-w5e5_historical-reference_" + "waterTemp_" + str(code_name) + "_monthly-average_1980_2019_basetier1.nc"
etls.cdo_crop_file_1980_2019(inp_file_name, mask, xmin, xmax, ymin, ymax, out_file_name, monavg = True)

# dynqual discharge - daily
dynqual_output_folder = "/scratch/depfg/sutan101/dynqual_output_from_duncan/1980-2019/" 
inp_file_name = dynqual_output_folder + "/" + "discharge_dailyTot_output_1980-2019.nc"
out_file_name = "pcrglobwb_dynqual_cmip6-isimip3-w5e5_historical-reference_" + "discharge_" + str(code_name) + "_daily_1980_2019_basetier1.nc"
etls.cdo_crop_file_1980_2019(inp_file_name, mask, xmin, xmax, ymin, ymax, out_file_name, monavg = False)


# move all unmasked files to a separate folder
os.system('mkdir unmasked')
os.system('mv *.unmasked unmasked')

# clean up temporary and unnecessary files
os.system('rm *.tif* ; rm *global* ; rm *basin_pgb*')


