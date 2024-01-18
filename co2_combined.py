from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the greenhouse gas emissions dataset
df = pd.read_csv('ghg-emissions-by-sector.csv')

# Extract emission factors
factors = list(df.columns[3:])

# Step 1: Define the Dash app object
app = Dash(__name__)

# Step 2: Define the layout
app.layout = html.Div([
    html.H4('GLOBAL CO2 CONTRIBUTIONS', style={'font-family': 'Lato', 'text-align': 'left', 'font-weight': 'bold'}),
    html.P("This is an interactive visualization to explore CO2 contributions across the world. You can explore various"
           " countries' contributions and filter through emission types and years.", style={'font-family': 'Lato'}),
    html.P("Select Country:", style={'font-family': 'Lato'}),
    dcc.Dropdown(
        id='dropdown',
        options=list(df.Entity.unique()),
        value='United States',
        clearable=False
    ),
    html.Div([  # Create container for the checkboxes and graph
        html.Div([  # Create container for the checkboxes
            html.P("Select Emission Types:", style={'font-family': 'Lato'}),
            dcc.Checklist(
                id='emission_types',
                options=[
                    {'label': 'Agriculture', 'value': 'Agriculture'},
                    {'label': 'Land-use change and forestry', 'value': 'Land-use change and forestry'},
                    {'label': 'Waste', 'value': 'Waste'},
                    {'label': 'Industry', 'value': 'Industry'},
                    {'label': 'Manufacturing and construction', 'value': 'Manufacturing and construction'},
                    {'label': 'Transport', 'value': 'Transport'},
                    {'label': 'Electricity and heat', 'value': 'Electricity and heat'},
                    {'label': 'Buildings', 'value': 'Buildings'},
                    {'label': 'Fugitive emissions', 'value': 'Fugitive emissions'},
                    {'label': 'Other fuel combustion', 'value': 'Other fuel combustion'},
                    {'label': 'Aviation and shipping', 'value': 'Aviation and shipping'}
                ],
                value=factors,
                labelStyle={'display': 'block'},
                style={'width': '250px'},
            )
        ], style={'width': '30%'}),  # Set width of the checkboxes container
        dcc.Graph(id='graph', style={'width': '90%', 'height': '400px'})  # Set width and height of the graph
    ], style={'display': 'flex'}),  # Set display style to flex for the horizontal layout
    html.P('Select Year Range:', style={'font-family': 'Lato'}),
    dcc.RangeSlider(
        id='year_slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        step=1,
        marks={1990: '1990', 1991: '1991', 1992: '1992', 1993: '1993', 1994: '1994', 1995: '1995',
               1996: '1996', 1997: '1997', 1998: '1998', 1999: '1999', 2000: '2000', 2001: '2001',
               2002: '2002', 2003: '2003', 2004: '2004', 2005: '2005', 2006: '2006', 2007: '2007',
               2008: '2008', 2009: '2009', 2010: '2010', 2011: '2011', 2012: '2012', 2013: '2013',
               2014: '2014', 2015: '2015', 2016: '2016', 2017: '2017', 2018: '2018', 2019: '2019'},
        value=[df['Year'].min(), df['Year'].max()],
    ),
    html.P([
        "For more information regarding greenhouse gas emissions and their impact, please visit the ",
        dcc.Link("EPA's GHG Emissions website", href="https://www.epa.gov/ghgemissions", target="_blank"),
        "."
    ], style={'font-family': 'Lato'})
])


# Step 3: Define the callback for updating the graph
@app.callback(
    Output('graph', 'figure'),
    Input('dropdown', 'value'),
    Input('year_slider', 'value'),
    Input('emission_types', 'value')
)
def display_country_data(country, years, selected_emissions):
    # Filter the data for the selected country and years
    min_year = years[0]
    max_year = years[1]
    df_selected = df[(df['Entity'] == country) &
                     (df['Year'] >= min_year) & (df['Year'] <= max_year)]

    # Create a bar chart for the selected data
    fig = px.bar(data_frame=df_selected, x=df_selected.Year, y=selected_emissions)
    fig.update_layout(title_text=f'{country} CO2 Emissions From {min_year} to {max_year}', title_x=0.5)
    fig.update_yaxes(title_text="Amount of Carbon Emission")
    fig.update_layout(legend_title_text='Emission Types')

    return fig


# Step 4: Run the server
app.run_server(debug=True)
