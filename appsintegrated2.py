import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State

df = pd.read_csv('https://raw.githubusercontent.com/mainelli/globe_and_flatmap/master/Origins_and_Destinations_sample.csv')  # Data comes in csv file format, with airport Origin Name, Latitude, and Longitude, and corresponding airport Destination Name, Latitude, and Longitude.

app = dash.Dash(__name__)

app.layout = html.Div([  # HTML Div gives every individual viz a spot on the page. In this case, the globe is one div, the map another, and the inputfield a third.
    html.Div([
        dcc.Graph(
            id='globe',
            clear_on_unhover=True,
            figure=dict(
                data=[go.Scattergeo(
                    lat=df['OrigLat'],
                    lon=df['OrigLon'],
                    hoverinfo='text',  # Hides the latitude and longitude values from being displayed on hoverover
                    hovertext=df['OrigName'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        symbol='circle',
                        color='#fc197f',
                        opacity=0.6,  # Giving dots some transparency helps preserve dot density perception
                        line=dict(
                            width=0.7,
                            color='#fce702'
                        )
                    )
                )],
                layout=go.Layout(
                    title='Click a spot on the globe to see reachable destinations',
                    hovermode='closest',
                    width=580,
                    height=580,
                    margin=go.layout.Margin(
                        l=10,
                        r=10,
                        b=10,
                        t=40
                    ),
                    font=dict(
                        family='Garamond EB',
                        size=18,
                        color='#535a82'
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    geo=go.layout.Geo(
                        showland=True,
                        showcountries=True,
                        showocean=True,
                        showlakes=True,
                        countrywidth=0.8,
                        landcolor='#f7ede8',
                        countrycolor='#b1ceba',
                        oceancolor='#c7e8e8',
                        lakecolor='#d1f2fc',
                        projection=go.layout.geo.Projection(
                            type='orthographic',
                            rotation=go.layout.geo.projection.Rotation(
                                lon=10,
                                lat=30,
                                roll=0
                            )
                        )
                    )
                )
            )
        )
    ],
        id='divglobe',
        style={
            'float': 'left',
            'display': 'inline-block',
            'width': '40%',
            'margin-top': '20px',
            'padding': '5px',
        }
    ),

    html.Div([
        dcc.Graph(
            id='map',
            clear_on_unhover=True,
        )
    ],
        id='divmap',
        style={
            'float': 'right',
            'display': 'inline-block',
            'margin-top': '30px',
            'padding': '5px'
        }
    ),

    html.Div([
        dcc.Input(
            id='inputField',
            placeholder='Click a spot on the Globe',
            type='text',
            value='',
        )
    ],
        id='divinputfield',
        style={
            'width': '10%',
            'display': 'block',
            'margin-top': '100px',
            'margin-left': '215px',
            'padding': '5px',
        }
    )
]
)


@app.callback(  # updates the input field whenever a hover occurs
    Output('inputField', 'value'),
    [Input('globe', 'hoverData')])
def update_input_field(input_value):  # input_value is given whatever 'hoverData' is
    if input_value != None:  # Prevents an error at the start when there has not yet been an input
        cityname = input_value['points'][0]['hovertext']
        return cityname


@app.callback(  # updates the map whenever a click occurs
    Output('map', 'figure'),
    [Input('globe', 'clickData')],
    state=[State('map', 'figure')])
def update_map(clickData, _):
    dff = pd.DataFrame(columns=['DestLat', 'DestLon', 'DestName'])
    origin_name = ''
    if clickData and len(clickData['points']) > 0:
        origin_name = clickData['points'][0]['hovertext']
        print("origin_name is " + origin_name)
        dff = df[df['OrigName'] == origin_name]
    return dict(
        data=[dict(
            type='scattergeo',
            lat=dff['DestLat'],
            lon=dff['DestLon'],
            hoverinfo='text',  # Hides the latitude and longitude values from being displayed on hoverover
            hovertext=dff['DestName'],
            mode='markers',
            marker=dict(
                size=10,
                symbol='circle',
                color='#fc197f',
                opacity=0.6,  # Giving dots some transparency helps preserve dot density perception – click on origin London to see this in action in North America
                line=dict(
                    width=0.7,
                    color='#fce702',
                )
            ),
        )],
        layout=go.Layout(
            title=dict(
                text='Destinations you can reach from <b>{}</b>'.format(origin_name)
            ),
            width=800,
            height=550,
            hovermode='closest',
            margin=go.layout.Margin(
                l=40,
                r=40,
                b=10,
                t=40
            ),
            font=dict(
                family='Garamond EB',
                size=18,
                color='#535a82'
            ),
            geo=go.layout.Geo(
                showland=True,
                showcountries=True,
                showocean=True,
                showlakes=True,
                countrywidth=0.8,
                landcolor='#f7ede8',
                countrycolor='#b1ceba',
                oceancolor='#c7e8e8',
                lakecolor='#d1f2fc',
                projection=go.layout.geo.Projection(
                    type='miller'
                )
            )
        )
    )


if __name__ == '__main__':
    app.run_server(debug=True)
