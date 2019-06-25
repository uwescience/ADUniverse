import pandas as pd
from pandas import DataFrame as DF
import numpy as np
import re

# Retrieve permits data
permits = pd.read_csv("permits.csv", sep=",",header=0)
permits = permits.drop(['se_anno_cad_data'], axis=1)

# Retrieve parcel data
parcels = pd.read_csv("parcels.csv", sep=",",header=0)
parcels = parcels.drop(['SHAPE_AREA', 'SHAPE_LEN'], axis=1)

def keyword_locate(kw, text = permits.comments):
    '''
    This function iterates over entries in the "text" variable, searching for any matches to the "kw" variable.
    Returns an nx1 numpy array of 1s and 0s, 1s indicating a match was found for "kw" in the associated row
    kw: keyword to search for
    text (optional): Pandas series of entries to iterate over.
    '''
    N = len(text)
    text = text.replace(np.nan, 'None') # Replace NaN values with string 'None'
    arr_match = np.zeros((N,1)) # define a table of 0s
    
    iter = 0
    for iter in range(0,N):
        
        if not text[iter] == 'None':
            
            # if any instances of the keyword are located...
            if len(re.findall(kw,text[iter])) > 0:
                arr_match[iter] = 1 # indicate a match was found
        
    return arr_match
	
# ADUs/DADUs
ADU = permits.type_occ.eq('ADU') | permits.type_occ.eq('DADU')

# ADUs under SF
SF = np.asarray(permits.type_occ == 'SF').reshape(-1,1)
# entries containing "ADU", less those containing "adult"
ADU_kw = keyword_locate('ADU') - keyword_locate('ADULT') 
# entries containing "accessory dwelling unit" in the comments
ADU_text = keyword_locate('accessory dwelling unit')
SF = (SF + ADU_kw + ADU_text) > 1
SF = pd.Series(SF.ravel())

# Specifically noted exceptions
EXCs = permits.objectid.eq(72) | permits.objectid.eq(117) | permits.objectid.eq(595) | permits.objectid.eq(622)
EXCs = EXCs | permits.objectid.eq(726) | permits.objectid.eq(998) | permits.objectid.eq(1064)
EXCs = EXCs | permits.objectid.eq(1249) | permits.objectid.eq(10188) | permits.objectid.eq(16818)

ADU = ADU | SF | EXCs

# Create DataFrame of modified data
cols = list(permits.columns)
cols.append("ADU")
df_ADUS = DF(np.append(np.asarray(permits), np.asarray(ADU).reshape(-1,1)*1, axis=1), columns=cols)

# Export DataFrame to csv file
df_ADUS.to_csv("ADUs.csv")
