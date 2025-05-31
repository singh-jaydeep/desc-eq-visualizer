import h5py
import numpy as np



f = h5py.File('test.h5', 'w')
f.create_dataset('dataset1', data=np.arange(0,100,2))
f.create_dataset('dataset2', data=np.zeros(5))
f.close()





g = h5py.File('test.h5', 'r')
print(g['dataset1'][()])
