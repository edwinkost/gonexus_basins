#!/bin/bash
#SBATCH -N 1
#SBATCH -n 96

#~ #SBATCH -t 240:00:00

#~ #SBATCH -p defq

#SBATCH -J dynqual_merging

#SBATCH --exclusive

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com


set -x

# load software
. /eejit/home/sutan101/load_default.sh


# - loop through all years
for i in {1980..2019}

do

YEAR=${i}

python merge_netcdf_general_selected_dynqual.py /scratch/depfg/graha010/DYNQUAL_GLOBAL_OUTPUT_ONLINE/ /scratch/depfg/sutan101/dynqual_output_from_duncan/1980-2019/${YEAR}/ outDailyTotNC ${YEAR}-01-01 ${YEAR}-12-31 discharge NETCDF4 True 8 dynqual_selected all_lats &

done

wait

set +x



