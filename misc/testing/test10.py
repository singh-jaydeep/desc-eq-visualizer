import desc
from desc.equilibrium import Equilibrium, EquilibriaFamily
from desc.grid import LinearGrid
import numpy as np
from desc.plotting import plot_2d, plot_section, plot_3d
import plotly.graph_objects as go
import plotly
import pandas as pd

import matplotlib.pyplot as plt


eq_family = desc.io.load('equilibria/base_desc_outputs/W7-X_output.h5')

if isinstance(eq_family, EquilibriaFamily):
    eq_family = eq_family[-1]


print(type(eq_family))