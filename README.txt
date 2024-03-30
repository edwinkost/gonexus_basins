
The folder contains two types of files, netcdf files and pcraster maps. All files are in the latitude and logitude grids. For questions, please contact E.H.Sutanudjaja@uu.nl (Edwin Sutanudjaja).


pcraster maps (.map files)
==========================

The pcraster maps are basically for describing the river basin attributes. See below for their brief description. 

- "basin_5min_original_<river_basin_name>_local.map": This map is a 5 arcmin raster basin map, based on the local model, more specifically based on the GIS file provided by the local modeler. Hence, this river basin map is condidered as the "original" one from the local model.

- "basin_5min_pcrglobwb_<river_basin_name>_local.map": This 5 arcmin raster basin map is identified based on the PCR-GLOBWB river/drainage network. To consdider uncertainty, this basin map includes five cell downstreams from the furthest downstream pixel within the "basin_5min_original_<river_basin_name>local.map" along with their corresponding catchments. Furthermore, it includes all (inland) sinks within the "basin_5min_original_<river_basin_name>_local.map" and their associated catchments.   

- "catchment_area_m2_5min_pcrglobwb_<river_basin_name>_local.map": The map of catchment area for every pixel in the "basin_5min_pcrglobwb_<river_basin_name>_local.map". The unit is m2 and the map is calculated based on the PCR-GLOBWB river/drainage network (i.e. "ldd_5min_pcrglobwb_<river_basin_name>_local.map") and PCR-GLOBWB cell areas ("cell_area_m2_5min_pcrglobwb_<river_basin_name>_local.map"). 

- "cell_area_m2_5min_pcrglobwb_<river_basin_name>_local.map": Individual cell area value for each pixel within the "basin_5min_pcrglobwb_<river_basin_name>_local.map. The unit is m2.

- "strahler_order_5min_pcrglobwb_<river_basin_name>_local.map": The strahler stream order for each pixel within the "basin_5min_pcrglobwb_<river_basin_name>_local.map.

- clone_5min_<river_basin_name>.map: The clone map, indicating the map extent and cell size (in arc-degree).

- ldd_5min_pcrglobwb_<river_basin_name>_local.map: The river/drainage network based on the PCR-GLOBWB model. 


netcdf files (.nc files)
========================

The following netcdf files are provided. Brief information for each file is given as follows. In each file, you can also check its netcdf attribute/metadata information that includes its unit. Note that basically the values in netcdf files provided are limited to the the mask in the file "basin_5min_pcrglobwb_<river_basin_name>_local.map". Yet, if required, the unmasked version files are also provided under the sub-folder "unmasked".

Evaporation:

- total evaporation from land and surface water bodies, but excluding evaporated water from non irrigation water consumption: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_totalEvaporation_<river_basin_name>_monthly-total_1980_2019_basetier1.nc

- evaporated water from non irrigation water consumption: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_nonIrrWaterConsumption_<river_basin_name>_monthly-total_1980_2019_basetier1.nc

- land surface evaporation (excluding surface water body evaporation and evaporated water from non irrigation water consumption): pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_actualET_<river_basin_name>_monthly-total_1980_2019_basetier1.nc

- evaporation from irrigated land: prglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_evaporation_from_irrigation_<river_basin_name>_monthly-total_1980_2019_basetier1.nc
pc

- transporation from irrigated land: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_transpiration_from_irrigation_<river_basin_name>_monthly-total_1980_2019_basetier1.nc


Precipitation and runoff:

- precipitation:  pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_precipitation_<river_basin_name>_monthly-total_1980_2019_basetier1.nc

- direct runoff (overland flow): pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_directRunoff_<river_basin_name>_monthly-total_1980_2019_basetier1.nc

- interflow (sub-surface stormflow): pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_interflowTotal_<river_basin_name>_monthly-total_1980_2019_basetier1.nc

- groundwater discharge (baseflow): pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_baseflow_<river_basin_name>_monthly-total_1980_2019_basetier1.nc

- total runoff (including local changes in surface water bodies): pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_totalRunoff_<river_basin_name>_monthly-total_1980_2019_basetier1.nc

- groundwater recharge pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_gwRecharge_<river_basin_name>_monthly-total_1980_2019_basetier1.nc

- surface water infiltration induced by groundwater pumping: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_surfaceWaterInf_<river_basin_name>_monthly-total_1980_2019_basetier1.nc

- river discharge based on pcrglobwb: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_discharge_<river_basin_name>_monthly-average_1980_2019_basetier1.nc

- river discharge based on the naturalized version of pcrglobwb: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_discharge-naturalized_<river_basin_name>_monthly-average_1980_2019_basetier1.nc

- river discharge based on DynQual (daily resolution): pcrglobwb_dynqual_cmip6-isimip3-w5e5_historical-reference_discharge_como_daily_1980_2019_basetier1.nc


Storage:

- interception storage: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_interceptStor_<river_basin_name>_monthly-average_1980_2019_basetier1.nc

- snow cover: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_snowCoverSWE_<river_basin_name>_monthly-average_1980_2019_basetier1.nc

- liquid water stored above snow: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_snowFreeWater_<river_basin_name>_monthly-average_1980_2019_basetier1.nc

- renewable part of groundwater storage: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_storGroundwater_<river_basin_name>_monthly-average_1980_2019_basetier1.nc

- non-renewable part (fossil) of groundwater storage: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_storGroundwaterFossil_<river_basin_name>_monthly-average_1980_2019_basetier1.nc

- upper soil moisture: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_storUppTotal_<river_basin_name>_monthly-average_1980_2019_basetier1.nc

- lower soil moisture: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_storLowTotal_<river_basin_name>_monthly-average_1980_2019_basetier1.nc

- surface water storage: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_surfaceWaterStorage_<river_basin_name>_monthly-average_1980_2019_basetier1.nc

- total water storage thickness: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_totalWaterStorageThickness_<river_basin_name>_monthly-average_1980_2019_basetier1.nc


Surface water temperature: pcrglobwb_dynqual_cmip6-isimip3-w5e5_historical-reference_waterTemp_como_daily_1980_2019_basetier1.nc

Air temperature: pcrglobwb_cmip6-isimip3-w5e5_image-aqueduct_historical-reference_temperature_<river_basin_name>_monthly-average_1980_2019_basetier1.nc


 
