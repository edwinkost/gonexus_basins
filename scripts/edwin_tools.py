#!/usr/bin/env python
# -*- coding: utf-8 -*-


def cdo_crop_file_1980_2019(inp_file_name, mask, xmin, xmax, ymin, ymax, out_file_name):

    # perform the following cdo operations for the variables that you want
    # -f nc4 -z zip 
    # -selyear 1980/2019
    # -sellonlatbox,-180,180,-90,90
    cmd  = "cdo -L -f nc4 "
    cmd += "-selyear,1981/2019 "
    cmd += "-sellonlatbox," + str(xmin) + "," + str(xmax) + "," + str(ymin) + "," + str(ymax) + " "
    cmd += input_file_name + " "
    cmd += os.path.basename(input_file_name) + ".tmp"
    print(cmd); os.system(cmd)
    
    # use area in 
    cmd = "cdo -L -f nc4 -div " + os.path.basename(input_file_name) + ".tmp " + output_file_name
    print(cmd); os.system(cmd)
    
    # rm tmp file
    cmd = 'rm ' + os.path.basename(input_file_name) + ".tmp"
    print(cmd); os.system(cmd)
    
    


     
