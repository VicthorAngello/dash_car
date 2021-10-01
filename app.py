
import dash
from dash import dash_table
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Card import Card
from dash_bootstrap_components._components.Row import Row
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

##### DATAFRAME #####

df = pd.read_excel(r'C:\Users\cs101125\Desktop\Dash\df_full.xlsx', sheet_name=0)
df['Total Vencido'] = df['1 - 10'] + df['11 - 30'] + df['31 - 60'] + df['61 - 85'] + df['PCLD']
df['1 - 10'] = pd.Series([round(val/1000, 3) for val in df['1 - 10']], index = df.index)
df['11 - 30'] = pd.Series([round(val/1000, 3) for val in df['11 - 30']], index = df.index)
df['31 - 60'] = pd.Series([round(val/1000, 3) for val in df['31 - 60']], index = df.index)
df['61 - 85'] = pd.Series([round(val/1000, 3) for val in df['61 - 85']], index = df.index)
df['PCLD'] = pd.Series([round(val/1000, 3) for val in df['PCLD']], index = df.index)
df['A Vencer'] = pd.Series([round(val/1000, 3) for val in df['A Vencer']], index = df.index)
df['Total Vencido'] = pd.Series([round(val/1000, 3) for val in df['Total Vencido']], index = df.index)
df['Diretoria_Segmento'] = df['Diretoria'].str.cat(df['Segmento'],sep=" / ")
df_dropdown = sorted(df['Diretoria_Segmento'].unique())

##### APP DASH #####

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], title='Contas a Receber', update_title='Carregando...')

app.layout = html.Div(dbc.Container([    
    
    dbc.Card([dbc.CardImg(src = 'assets\Imagem2.png', style = {"width":'100%', 'height':'80%', 'background':'none'})], style={'border':'0px', 'background':'none'},outline=True),

    dcc.Dropdown(
    id='select-dropdown',
    options=[{'label':i,'value':i} for i in df_dropdown],
    style = {'margin-top': '10px', 
            'margin-bottom': '10px',
            'background-color': 'rgba(255, 255, 255, 0.35)', 
            'font-size': '100%',
            'color': 'rgb(2, 56, 89)',
            'fontWeight': 'bold',
            'textAlign':"center",
    },
    placeholder='Selecionar Operação', 
    #value=sorted(df['Diretoria_Segmento'].unique())[0],
    ),

    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='datatable-interactivity',
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
                ],
                    data=df.to_dict('records'),
                    editable=False,
                    page_size= 15,
                    style_as_list_view=True,
                    style_table={
                        'borderRadius': '5px',
                        'border':'1px solid white',
                        'overflow': 'hidden'
                    },
                    style_cell={'textAlign': 'center'},
                    style_header={
                        'backgroundColor': 'rgba(2, 56, 89, 0.55)',
                        'fontWeight': 'bold',
                        'color': 'rgb(255, 255, 255)'
                    },
                    style_data = {
                        'backgroundColor': 'rgba(2, 56, 89, 0.45)',
                        'fontWeight': 'bold',
                        'color': 'rgb(255, 255, 255)'
                    },                                               
                    style_data_conditional=[{'if': {'column_id': ['Diretoria','Segmento', 'Diretoria_Segmento'],},
                        'display': 'None',},],
                    style_header_conditional=[{'if': {'column_id': ['Diretoria','Segmento', 'Diretoria_Segmento'],},
                        'display': 'None',},],
            ),
            html.Div(id='datatable-interactivity-container')
        ]),
        dbc.Col([
                dcc.Graph(
                    id='cliente-result'
                )
            ]),    
    ]),

    html.Div([
        dcc.Graph(
            id='periordo-result'
        )
    ]),
], 
fluid=True, style={'width': '90%', 'padding':'0.5%'}
), 
style={'background-image':'url("/assets/fundo_paisagem.png")', 'background-repeat': 'no-repeat', 'background-size': 'cover'}, 
)


##### CALLBACKS #####

@app.callback(
    Output(component_id='datatable-interactivity', component_property='data'),
    [Input(component_id='select-dropdown', component_property='value')])

def update_df_div(value):
    if value is None:
        filtered_df = df
        data = filtered_df.to_dict('records')
    else:
        filtered_df =  df[df['Diretoria_Segmento'] == value]
        data = filtered_df.to_dict('records')
    return data


@app.callback(
   Output(component_id='cliente-result',component_property='figure'),
   [Input(component_id='select-dropdown',component_property='value')])

def update_output(value):

    if value is None:
        df_filtered = df.groupby("Cliente").sum().reset_index()    
    else:
        df_filtered = df[df['Diretoria_Segmento'] == value].groupby("Cliente").sum().reset_index()

    fig = px.bar(df_filtered,x='Cliente',y='A Vencer', title="A Vencer por Cliente")
    fig.update_layout({
        'plot_bgcolor': 'rgba(2, 56, 89, 0.45)',
        'paper_bgcolor': 'rgba(255, 255, 255, 0.45)'
    })

    return fig

@app.callback(
   Output(component_id='periordo-result',component_property='figure'),
   [Input(component_id='select-dropdown',component_property='value')])

def update_output(value):
    if value is None:
        df_filtered = df.groupby("Cliente").sum().reset_index()
    else:
        df_filtered = df[df['Diretoria_Segmento'] == value].groupby("Cliente").sum().reset_index()

    fig = px.bar(df_filtered,x='Cliente',y=['1 - 10', '11 - 30', '31 - 60', '61 - 85', 'PCLD'], title="Vencidos por Categoria x Cliente")
    fig.update_layout({
        'plot_bgcolor': 'rgba(2, 56, 89, 0.45)',
        'paper_bgcolor': 'rgba(255, 255, 255, 0.45)',
        'legend_title':'Vencido à:',
        'legend_title_font_color':'rgb(2, 56, 89)',
        'font_color':'rgb(2, 56, 89)'
        })
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)