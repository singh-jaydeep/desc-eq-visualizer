import desc
from desc.equilibrium import Equilibrium
from desc.grid import LinearGrid
import numpy as np
from desc.plotting import plot_2d, plot_section, plot_3d
import plotly.graph_objects as go
import plotly

import matplotlib.pyplot as plt

eq = desc.io.load('equilibria/base_desc_outputs/eq_tok_eps_0.4.h5')
coord_r = eq.compute('R')['R']
coord_z = eq.compute('Z')['Z']
upper_xyrange = 1.2*np.max(coord_r)
upper_zrange = 1.2*np.max(coord_z)

maj_r = eq.compute('R0')['R0']
min_r = eq.compute('a')['a']
ar=float(eq.compute('R0/a')['R0/a'])
inv_ar = 1/ar
xyrange = maj_r + 20*min_r
zrange = 10*min_r

fig0 = plot_3d(eq, '1')
fig0.update_layout(autosize=False, width=1000,height=750)
fig0.update_traces(opacity=.4, showscale=False)
fig0.update_layout(scene = dict(aspectmode='manual', aspectratio = {'x': 1, 'y':1, 'z': inv_ar},
                                xaxis = dict(range=[-upper_xyrange,upper_xyrange], autorange=False),
                                yaxis = dict(range=[-upper_xyrange,upper_xyrange], autorange=False),
                                zaxis = dict(range=[-upper_zrange,upper_zrange], autorange=False)))
fig0.show()


'''
fig0X, data0X = plot_3d(eq, 'X', return_data=True)
fig0Y, data0Y = plot_3d(eq, 'Y', return_data=True)
fig0Z, data0Z = plot_3d(eq, 'Z', return_data=True)

ranX=np.max(data0X['X'])-np.min(data0X['X'])
ranY=np.max(data0X['Y'])-np.min(data0X['Y'])
ranZ=np.max(data0X['Z'])-np.min(data0X['Z'])
ranMax = max(ranX, ranY, ranZ)

print(ranX/ranMax, ranY/ranMax, ranZ/ranMax)
'''

'''
ar=float(eq.compute('R0/a')['R0/a'])
inv_ar = 1/ar
maj_r = float(eq.compute('R0')['R0'])
min_r = float(eq.compute('a')['a'])

xyrange = maj_r + 20*min_r
zrange = 10*min_r


fig0 = plot_3d(eq, '1')
fig0.update_layout(autosize=False, width=1000,height=750)
fig0.update_traces(opacity=.4, showscale=False)
fig0.update_layout(scene = dict(aspectmode='manual', aspectratio = {'x': 1, 'y':1, 'z': inv_ar},
                                xaxis = dict(range=[-xyrange,xyrange], autorange=False),
                                yaxis = dict(range=[-xyrange,xyrange], autorange=False),
                                zaxis = dict(range=[-zrange,zrange], autorange=False)))
fig0.show()
'''



#fig0.update_layout(width=)

#fig0 = plot_3d(eq, 'J^rho')



#print(len(fig0.data))
#print(type(fig0.data[0]))
'''
mesh0 = fig0.data[0]


gridA_args = {
        "N": 50,
        "M": 50, 
        "NFP": 1, 
        "endpoint": True,
        'rho': np.array([.2])
    }
gridA = LinearGrid(**gridA_args)

gridB_args = {
        "N": 50,
        "M": 50, 
        "NFP": 1, 
        "endpoint": True,
        'rho': np.array([.6])
    }
gridB = LinearGrid(**gridB_args)

meshA = plot_3d(eq, 'J^rho', grid=gridA)
meshB = plot_3d(eq, 'J^rho', grid=gridB)

fig0.add_trace(meshA.data[0])
fig0.add_trace(meshB.data[0])
fig0.show()
'''



'''
print(data.keys())
print(np.shape(data['X']))
print(np.shape(data['Y']))
fig.show()
'''
