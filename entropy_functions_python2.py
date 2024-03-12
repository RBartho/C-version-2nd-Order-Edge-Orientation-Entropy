import numpy as np
import pickle
import time

#### define values

MAX_DIAGONAL = 180
CIRC_BINS = 48
GABOR_BINS = 256

BINS_VEC = np.linspace(0, 2*np.pi, GABOR_BINS+1)[:-1]



############### helper functions

def _inf(data, data_name= None , print_data=False):
    if data_name != None:
        print('Data_name:' , data_name)
    print('Data_type: ' , type(data))
    print('Values_type: ' ,  data.dtype)
    print('Data_shape: ', data.shape)
    print('Data_min:', np.min(data), 'Data_max:' , np.max(data), 'Data_std:' , np.std(data))
    if print_data:
        print(data)
    print(' ')
    
    
############## preprocess filter responses

def preprocess_filter_resp( resp ):
    
    filter_max_th = pickle.load( open( './filter_max_th.pkl'  ,'rb')   )

    ### normalize filters with theoretical maximum filter response value to same 'Wertebereich'
    resp_norm = np.zeros_like(resp)
    
    for i , filter_resp in enumerate(resp):
        temp =  filter_resp / filter_max_th[i]
        resp_norm[i] = np.round( temp * (GABOR_BINS - 1 )  )        
    return resp_norm

             
def entropy(a):
    if np.sum(a)!=1.0 and np.sum(a)>0:
        a = a / np.sum(a)
    v = a>0.0
    return -np.sum(a[v] * np.log2(a[v]))

  
def do_statistics(counts):
    """normalize counts, do statistics"""

    # normalize by sum
    counts_sum = np.sum(counts, axis=2) + 0.00001
    normalized_counts = counts / (counts_sum[:,:,np.newaxis])

    d,a,_ = normalized_counts.shape
    shannon_nan = np.zeros((d,a))
    for di in range(d):
      for ai in range(a):
        if counts_sum[di,ai]>1:  ## ignore bins without pixels
            shannon_nan[di,ai] = entropy(normalized_counts[di,ai,:])
        else:
            shannon_nan[di,ai] = np.nan
        
    return shannon_nan
   


        
        
