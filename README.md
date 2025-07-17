# Visualization dashboard for DESC

An interactive application for visualizing three dimensional, toroidal magnetic fields. The dashboard is built in [Dash](https://dash.plotly.com/), and is compatible with outputs of the [DESC](https://github.com/PlasmaControl/DESC) code. 

Key features:
- Accepts 'X.h5' files storing Equilibrium or EquilibriumFamily objects from DESC
- Uses DESC's API to compute and store quantities of interest:
    - scalar figures of merit ($\beta$, MHD force error, ...)
    - functions of the flux surface label (pressure, rotational transform, ...)
    - 2D flux surfaces on fixed toroidal slices
    - 2D heatmaps of functions on fixed flux surface, and fixed toroidal slice (current and magnetic field densities, ... )
    - 3D flux surfaces, and magnetic axis
    - 3D heatmaps of functions on fixed flux surface(current and magnetic field densities, ... )
- At runtime, loads computed quantities into a browser Dash app. User can select different quantities to plot, and cycle through equilibria
      








