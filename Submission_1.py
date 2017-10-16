import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gc

train = pd.read_csv('data/train_2.csv')
train.fillna(0, inplace=True)

# define the Windows according to Ehsan's kernel
r = 1.61803398875  
Windows = np.round(r**np.arange(0,9) * 7).astype(int)

test = pd.read_csv('data/key_2.csv')
test['Date'] = test.Page.apply(lambda x: x[-10:])
test['Page'] = test.Page.apply(lambda x: x[:-11])
test['Date'] = test['Date'].astype('datetime64[ns]')
test['wk']= test.Date.dt.dayofweek >=5

for i in Windows:
    print(i,end= ' ')
    val='MW'+str(i)
    tmp = pd.melt(train[list(train.columns[-i:])+['Page']], 
                  id_vars='Page', var_name='D', value_name=val)
    tmp['D'] = tmp['D'].astype('datetime64[ns]')
    tmp['wk']= tmp.D.dt.dayofweek  >=5           
    tmp1 = tmp.groupby(['Page','wk']).median().reset_index()
    test = test.merge(tmp1, how='left')
    
test['Visits']=test.iloc[:,4:].median(axis=1).round().astype(int)
test[['Id','Visits']].to_csv('submissions/Submission_1.csv', index=False)
gc.collect()