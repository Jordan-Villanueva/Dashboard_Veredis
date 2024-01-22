#!/usr/bin/env python
# coding: utf-8

# In[12]:


# Load your data
# link of data: http://datosabiertos.stps.gob.mx/Datos/DIL/clave/Tasa_de_Desocupacion.csv
# url = "http://datosabiertos.stps.gob.mx/Datos/DIL/clave/Tasa_de_Desocupacion.csv"
#!pip install voila
#!pip install dash pandas plotly
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

# Cargar datos
url = 'https://raw.githubusercontent.com/Jordan-Villanueva/Dashboard_Veredis/main/Tasa_de_Desocupacion.csv'
data = pd.read_csv(url, encoding='latin-1')
data = data[(data['Entidad_Federativa'] != 'Nacional')].reset_index(drop=True)
data = data.drop(columns=['Unnamed: 7', 'Unnamed: 8'])

# Filtrar años y trimestres únicos
unique_years = data['Periodo'].unique()

# Crear la aplicación Dash
app = dash.Dash("PEA Mexico")

# Definir el diseño
app.layout = html.Div([
    html.H1("Población Económicamente Activa en México"),

    dcc.Dropdown(
        id='year-dropdown',
        options=[
            {'label': str(year), 'value': year} for year in unique_years
        ],
        value=unique_years.max(),
        multi=False,
        style={'width': '50%'}
    ),

    dcc.Dropdown(
        id='trimester-dropdown',
        multi=False,
        style={'width': '50%'}
    ),

    html.Div(
        id='message',
        children='',
        className='centered-message'
    ),

    dcc.Graph(id='bar-chart'),
])

# Definir la devolución de llamada para actualizar las opciones del menú desplegable de trimestres
@app.callback(
    Output('trimester-dropdown', 'options'),
    [Input('year-dropdown', 'value')]
)
def update_trimester_options(selected_year):
    if selected_year == 2023:
        # Si el año es 2023, mostrar solo los trimestres 1 y 2
        trimester_options = [{'label': '1', 'value': 1}, {'label': '2', 'value': 2}]
    else:
        # Para otros años, mostrar todos los trimestres disponibles
        trimester_options = [{'label': str(trimestre), 'value': trimestre} for trimestre in data['Trimestre'].unique()]

    return trimester_options

# Definir callback para actualizar el gráfico de barras
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('trimester-dropdown', 'value')],
    prevent_initial_call=True
)
def update_chart(selected_year, selected_trimester):
    filtered_data = data[(data['Periodo'] == selected_year) & (data['Trimestre'] == selected_trimester)]
    fig = px.bar(
        filtered_data,
        x='Entidad_Federativa',
        y='Poblacion_Economicamente_Activa',
        color='Sexo',
        barmode='group',
        labels={'Poblacion_Economicamente_Activa': 'Población (millones de habitantes)'},
        color_discrete_sequence=['steelblue', 'magenta'],
        title=f'Población Económicamente Activa en {selected_year} - Trimestre {selected_trimester}')
    fig.update_xaxes(tickangle=-60)
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)


# In[13]:


# La version anterior del codigo:
'''
import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Cargar datos
url='https://raw.githubusercontent.com/Jordan-Villanueva/Dashboard_Veredis/main/Tasa_de_Desocupacion.csv'
data = pd.read_csv(url, encoding='latin-1')
data = data[(data['Entidad_Federativa'] != 'Nacional')].reset_index(drop=True)
data = data.drop(columns=['Unnamed: 7', 'Unnamed: 8'])

# Filtrar años y trimestres únicos
unique_years = data['Periodo'].unique()

# Crear la aplicación Dash
app = dash.Dash("PEA Mexico")

# Definir el diseño
app.layout = html.Div([
    html.H1("Población Económicamente Activa en México"),

    dcc.Dropdown(
        id='year-dropdown',
        options=[
            {'label': str(year), 'value': year} for year in unique_years
        ],
        value=unique_years.max(),
        multi=False,
        style={'width': '50%'}
    ),

    dcc.Dropdown(
        id='trimester-dropdown',
        value=data['Trimestre'].max(),
        multi=False,
        style={'width': '50%'}
    ),

    html.Div(
        id='message',
        children='',
        className='centered-message'
    ),

    dcc.Graph(id='bar-chart'),
])

# Definir la devolución de llamada para actualizar las opciones del menú desplegable de trimestres
@app.callback(
    Output('trimester-dropdown', 'options'),
    [Input('year-dropdown', 'value')]
)

def update_trimester_options(selected_year):
    if selected_year == 2023:
        # Si el año es 2023, mostrar solo los trimestres 1 y 2 y seleccionar el primer trimestre
        trimester_options = [{'label': '1', 'value': 1}, {'label': '2', 'value': 2}]
        selected_trimester = 1
    else:
        # Para otros años, mostrar todos los trimestres disponibles y seleccionar el último trimestre
        trimester_options = [{'label': str(trimestre), 'value': trimestre} for trimestre in data['Trimestre'].unique()]
        selected_trimester = data['Trimestre'].max()

    return trimester_options, selected_trimester

def update_chart(selected_year, selected_trimester):
    filtered_data = data[(data['Periodo'] == selected_year) & (data['Trimestre'] == selected_trimester)]
    fig = px.bar(
    filtered_data,
    x='Entidad_Federativa',
    y='Poblacion_Economicamente_Activa',
    color='Sexo',
    barmode='group',
    labels={'Poblacion_Economicamente_Activa': 'Población (millones de habitantes)'},
    color_discrete_sequence = ['steelblue','magenta'],
    title=f'Población Económicamente Activa en {selected_year} - Trimestre {selected_trimester}')
    fig.update_xaxes(tickangle=-60)
    return fig

# ... (código restante)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
'''


# In[ ]:




