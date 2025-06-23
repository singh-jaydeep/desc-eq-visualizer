import desc
from desc.equilibrium import Equilibrium
from desc.grid import LinearGrid
import numpy as np
from desc.plotting import plot_2d, plot_section
import plotly.graph_objects as go
import plotly


eq = desc.io.load('equilibria/base_desc_outputs/eq_tok_eps_0.4.h5')
fig,_,data = plot_section(eq, 'J^rho', phi = 8, return_data=True)
xdata = data['R'][:,:,0]
ydata = data['Z'][:,:,0]
zdata = data['J^rho'][:,:,0]

fig = go.Figure(data=[
                    go.Surface(
                        x=xdata,
                        y=ydata,
                        z=np.zeros_like(zdata),  
                        surfacecolor=zdata,      
                        colorscale='Viridis',
                        #cmin=np.min(zdata),
                        #cmax=np.max(zdata),
                        showscale=True
                    )
        ])
fig.update_layout(
        scene_camera=dict(eye=dict(x=0., y=0., z=2.)),
        scene_dragmode=False,  
        scene=dict(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            zaxis=dict(visible=False)
        )   
)
fig.show()


'''
eq = desc.io.load('equilibria/base_desc_outputs/eq_tok_eps_0.4.h5')
fx_num_rho = 8
fx_num_theta = 8
fx_num_phi = 12


fig,_,data=plot_section(eq,'J^rho', phi = fx_num_phi, return_data=True)
print(np.shape(data['R']))
print(data['R'][50,:,0])
print(data['R'][:,20,0])
'''



'''
grid_args = {
        "NFP": eq.NFP,
        "sym": False,
        "axis": False,
        "endpoint": True,
        "M": 2, 
        "N": 3,
        "rho": np.array([1.0])
    }
fig0,_,data0 = plot_2d(eq, 'J^rho', grid=LinearGrid(**grid_args), return_data=True)
print(data0.keys())
print(np.shape(data0['zeta']))
print(data0['zeta'])
print(data0['theta'])
print(data0['J^rho'])
fig = go.Figure()
numtheta = 2*2+1
numzeta = 2*3+1
thetadata = np.linspace(0,2*3.14159, numtheta)
zetadata = np.linspace(0, 2*3.14159, numzeta)
fig.add_heatmap(autocolorscale=True, x=thetadata, y=zetadata, z=data0['J^rho'])
fig.show()
'''

'''
grid_args = {
       # "NFP": eq_tok.NFP,
        "sym": False,
        "axis": False,
        "endpoint": True,
        "M": 33, 
        "N": 33,
        #"rho": np.array([1.0])
    }

grid_args['NFP']=eq.NFP
grid_args['rho']=np.array([0.1])
grid = LinearGrid(**grid_args)
attrs_2d = ['B^rho', 'J^rho']
#for q in attrs_2d:
#fig,ax,data = plot_2d(eq, 'B^rho',return_data=True)
#fig,ax,data = plot_2d(eq, 'J^rho', grid = grid, return_data=True)

try:
    fig,ax,data = plot_2d(eq, 'J^rho',return_data=True)
except:
    print('error')

fig = go.Figure()
    ############
    # FIX #
numtheta = 20
numphi = 20
thetadata = np.linspace(0,2*3.14159, numtheta)
phidata = np.linspace(0, 2*3.14159, numphi)
    ############
fig.add_heatmap(autocolorscale=True, x=thetadata, y=phidata, z=None)
fig.show()

'''