
from entropy_functions_python2 import preprocess_filter_resp, do_statistics
import os
import pickle
import numpy as np
import warnings
import time

# in python itself (this compiles the module inplace)
#os.system("python3 setup_cython.py build_ext --inplace") 

from calc_counting import _do_counting

MAX_DIAGONAL = 180
CIRC_BINS = 48

RANGES = [(0,10),
          (10,20),
          (20,30),
          (30,40),
          (40,50),
          (50,60), 
          (60,70), 
          (70,80),
          (80,90), 
          (90,100),
          (100,110),
          (110,120),
          (120,130),
          (130,140),
          (140,150),
          (150,160),
          (160,170), 
          (170,180)]

PLOT_DIR = "plots"
TEXT_DIR = "text"
EXPORT_DIR = "export"


if not os.path.exists(PLOT_DIR):
    os.makedirs(PLOT_DIR)
if not os.path.exists(TEXT_DIR):
    os.makedirs(TEXT_DIR)
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

TIMESTAMP = time.strftime("%Y.%m.%d-%H%M%S-%a")
log_file = os.path.join(EXPORT_DIR,"export-"+TIMESTAMP+".csv")


result_names = ["%s%d-%d" % (n, r[0], r[1]) for r in RANGES for n in ["avg-shannon-nan"]]



with open(log_file, 'w') as log:
    log.write("image,"+",".join(result_names)+"\n")

### preallocate memory
output = np.zeros(180 * 48 * 256).astype("uint32")

distance_list = np.zeros(126 * 126 * 126 * 126).astype("uint32")
direction_list = np.zeros(126 * 126 * 126 * 126).astype("uint32")
difference_list = np.zeros(126 * 126 * 126 * 126).astype("uint32")

distance = np.zeros(126 * 126).astype("uint32")
direction = np.zeros(252 * 252).astype("uint32")

### precompute distance
for i in range(126):
    for j in range(126):
        distance[j + 126*i] = np.round(np.sqrt( i**2  + j**2  )).astype("uint32")

### precompute direction
for i in range(252):
    for j in range(252):
        temp =   np.round( (np.arctan2(i-126, j-126) / (2.0 * np.pi)) * CIRC_BINS ) #.astype("uint32")
        temp_mod = (temp + 48 ) % 48;
        direction[i + 252*j] = temp_mod.astype("uint32")

### load precomputed filter responses (see original code)

dir_filter_resp = '...'

i = 0
for n in range(96):
    
    if n > 65:
        
        print('###################################################')
        print('n:', n)
        print('  ')
        log_file = os.path.join(EXPORT_DIR,"export-"+TIMESTAMP+ '__filter_noNorm_' + str(n) +".csv")
        
        for subdir, dirs, files in os.walk(dir_filter_resp):
            for file in files:
                res_dict  = pickle.load(  open( os.path.join(subdir, file) , 'rb'  )   )
                
                ### loop over images (filter responses of each image)
                for key in res_dict:
                    print (" (%d/%s)" % (i+1, 4300),)              
                    print(key)

                    image_name = key.split('/')[-1]
                    
                    resp = res_dict[key]
                    
                    ### normalize filters
                    resp_norm = preprocess_filter_resp( resp )
                    #resp_norm = resp
                    
                    start = time.time()
                    
                    #for target in resp_norm:
                    target = resp_norm[n]  
                    
                    output = np.zeros(180 * 48 * 256).astype("uint32")
        
                    filt_c = target.flatten().astype("int32")
        
                    _do_counting(filt_c   ,  distance ,  direction , output)
                    
                    if np.sum(output) != 126*126*126*126:
                        print(np.sum(output))
                        assert(-1)
        
                    out_re = output.reshape([256,48,180])
                    counts = np.swapaxes(out_re,0,2)
                    shannon_nan = do_statistics(counts)
           
                    results = []
                    for r in RANGES:
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore", category=RuntimeWarning)
                            results.append(np.nanmean(np.nanmean(shannon_nan, axis=1)[r[0]:r[1]]))

                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", category=RuntimeWarning)
                        np.savetxt(os.path.join(TEXT_DIR, os.path.basename(image_name)+".shannon-nan.txt"), np.nanmean(shannon_nan, axis=1))
        
                    with open(log_file, 'a') as log:
                        log.write(os.path.basename(image_name)+","+",".join([str(v) for v in results])+"\n")
                      
                            
                    end = time.time()   
                    print('time taken: ' , end - start)
                    i += 1


            
