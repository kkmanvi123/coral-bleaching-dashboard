from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Sample data for this example
# Replace this with your actual data
df = pd.read_csv('ghg-emissions-by-sector.csv')

df = df.drop(columns='Code')
total_emissions_df = df.groupby(['Entity', 'Year']).sum().reset_index()
total_emissions_df['Total Carbon Emissions'] = total_emissions_df.iloc[:, 3:].sum(axis=1)

app = Dash(__name__)

app.layout = html.Div([
    html.H4('CO2 Emissions Choropleth Map'),
    html.P("Select a year:"),
    dcc.Slider(
        id='year-slider',
        min=total_emissions_df['Year'].min(),
        max=total_emissions_df['Year'].max(),
        step=1,
        value=total_emissions_df['Year'].min(),
        marks={str(year): str(year) for year in total_emissions_df['Year'].unique()},
    ),
    dcc.Graph(id="choropleth-map"),
    html.Button("Play", id="play-button", n_clicks=0),
    dcc.Interval(id="play-interval", interval=1000, n_intervals=0),
])

@app.callback(
    Output("year-slider", "value"),
    Input("play-button", "n_clicks"),
    Input("play-interval", "n_intervals"),
    prevent_initial_call=True,
)
def update_slider_value(n_clicks, n_intervals):
    max_year = total_emissions_df['Year'].max()
    current_value = total_emissions_df['Year'].min() if n_clicks % 2 == 1 else total_emissions_df['Year'].max()
    next_value = current_value + 1 if n_clicks % 2 == 1 else current_value - 1
    return min(max_year, max(total_emissions_df['Year'].min(), next_value))

@app.callback(
    Output("play-interval", "disabled"),
    Input("play-button", "n_clicks"),
)
def toggle_interval(n_clicks):
    return n_clicks % 2 == 0

@app.callback(
    Output("choropleth-map", "figure"),
    Input("year-slider", "value"),
    Input("play-interval", "n_intervals"),
)
def display_choropleth(selected_year, n_intervals):
    filtered_df = total_emissions_df[total_emissions_df['Year'] == selected_year]
    fig = px.choropleth(
        filtered_df,
        locations="Entity",
        locationmode="country names",
        color="Total Carbon Emissions",
        color_continuous_scale="Reds",
        range_color=[0, 5e9],  # Set the range to 0 to 1 billion
        labels={"Total Carbon Emissions": "Total Emissions"},
        title=f"CO2 Emissions by Country in {selected_year}",
    )
    fig.update_geos(
        projection_type="robinson",
        showcoastlines=True,
    )
    return fig

@app.callback(
    Output("play-button", "n_clicks"),
    Input("play-interval", "n_intervals"),
    prevent_initial_call=True,
)
def update_play_button(n_intervals):
    if n_intervals % total_emissions_df['Year'].nunique() == 0:
        return 1
    return 0

app.run_server(debug=True)
