#################################################
# Tab 1 generates a data table
#################################################

import pandas as pd
import h5py
from dash import dash_table
import dash_bootstrap_components as dbc

from . import layout_utils as lu


def comp_tab():
    div = dbc.Container([
            dbc.Row([
                dbc.Col([
                    dash_table.DataTable(data=None,
                                         columns=[
                                            {"name": "Parameter", "id": "Parameter"},
                                            {"name": "Value", "id": "Value"}
                                        ],
                                        tooltip_data = None,
                                        tooltip_duration = None,
                                        style_table={
                                            'overflowX': 'auto',
                                            'backgroundColor': '#343a40'  
                                        },
                                        style_cell={
                                            'backgroundColor': '#343a40',
                                            'color': 'white',
                                            'border': '1px solid #495057'
                                        },
                                        style_header={
                                            'backgroundColor': '#495057',
                                            'color': 'white',
                                            'fontWeight': 'bold',
                                            'border': '1px solid #6c757d'
                                        },
                                        style_data_conditional=[
                                            {
                                                'if': {'row_index': 'odd'},
                                                'backgroundColor': '#3e444a',
                                            },
                                            {
                                                'if': {'state': 'active'},  
                                                'backgroundColor': '#495057',
                                                'border': '1px solid #adb5bd'
                                            },
                                            {
                                                'if': {'state': 'selected'},  
                                                'backgroundColor': '#198754',  
                                                'color': 'white'
                                            }
                                        ],
                                        id='summary-table')
                ], width=6)
            ])
    ], className='mt-5')
    return div


## Tab 1 update, triggered by callback 
def update_table_stats(eq_index,params):
    with h5py.File(params.pp_desc_path+'/pp_'+params.eq_names_list[eq_index],'r') as f:
        data_scalars = f['/scalars'] ## This is a group, with attributes corresponding to the values
        
        df_list=[]
        hover_list=[]

        ## Separately add NFP, the number of field periods 
        eq = params.eq_loaded[eq_index]
        df_list += [{'Parameter': 'NFP', 'Value': f'{eq.NFP}'}]
        hover_list += [{'Parameter': {'value': 'Number of field periods', 'type': 'markdown'}, 'Value': None}]

        ## Add the remaining quantities in params.attrs_scalars
        for q in params.attrs_scalars:
            val = data_scalars.attrs[q+'_scalar_'+'_value_']
            val_str = lu.display_number(val)
            quantity = data_scalars.attrs[q+'_scalar_'+'_description_']
            units = data_scalars.attrs[q+'_scalar_'+'_units_']
            text = f'Quantity: {quantity} \n Units: {units}'
            df_list += [{'Parameter': q, 'Value': f'{val_str}'}]
            hover_list += [{'Parameter': {'value': text, 'type': 'markdown'}, 'Value': None}]
        
        

    df = pd.DataFrame(df_list)
    return df.to_dict('records'), hover_list



