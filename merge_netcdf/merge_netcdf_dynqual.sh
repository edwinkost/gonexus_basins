#!/bin/bash

set -x

python merge_netcdf_general_selected_dynqual.py /scratch/depfg/graha010/DYNQUAL_GLOBAL_OUTPUT_ONLINE/ /scratch/depfg/sutan101/dynqual_output_from_duncan/test/ outDailyTotNC 1980-01-01 2019-12-31 discharge NETCDF4 True 8 dynqual_selected all_lats &

python merge_netcdf_general_selected_dynqual.py /scratch/depfg/graha010/DYNQUAL_GLOBAL_OUTPUT_ONLINE/ /scratch/depfg/sutan101/dynqual_output_from_duncan/test/ outDailyTotNC 1980-01-01 2019-12-31 waterTemp NETCDF4 True 8 dynqual_selected all_lats &

wait

set +x



