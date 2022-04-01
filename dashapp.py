import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State
from utils import generate_plot, generate_pdf

#from dash_extensions.enrich import DashProxy, TriggerTransform, MultiplexerTransform, ServersideOutputTransform, NoOutputTransform

# app = DashProxy(transforms=[

#     MultiplexerTransform(),  # makes it possible to target an output multiple times in callbacks

# ],external_stylesheets=[dbc.themes.BOOTSTRAP],)
app = dash.Dash(__name__)
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
app.config.suppress_callback_exceptions = True


distributions = [
    ['normal', 'Normal'],
    ['binomial','Binomial'],
    ['negbinomial', 'Binomial Negativa'],
    ['exponential', 'Exponencial'],
    ['poisson', 'Poisson']
]

app.layout = html.Div([

    html.Div(

        dbc.Container(
            [
                html.H3("Random Distributed Number Generator", className="display-6"),

            ],
            fluid=True,
            className="py-3 center",
        ),
        className="p-3 bg-dark rounded-3",
        style={'color':'#fff'}
    ),
    html.Br(),

    html.Div([

        html.Div([
            html.Label('Select Distribution'),
            dcc.Dropdown(
                id='distribution-select',
                options=[{'label': d[1], 'value': d[0]} for d in distributions],
                value=''
            ),
        ], className='col-6'),
    ]),

    html.Br(),

    dbc.Label('Parameters:'),

    dbc.Card(id='parameters-container',
             children=[
                 html.Div(
                     id='normal-parameters',
                     children=[
                         dbc.Input(id='n-mean', type='number', placeholder='Mean', step=0.1),
                         html.Br(),
                         dbc.Input(id='n-std', type='number', placeholder='Standard Deviation', step=0.001),
                         html.Br()], style={'display': 'none'}),
                 html.Div(
                     id='binomial-parameters',
                     children=[
                         dbc.Input(id='b-r', type='number', placeholder='R', step=0.1),
                         html.Br(),
                         dbc.Input(id='b-p', type='number', placeholder='P', min=0, max=1, step=0.001),
                         html.Br()], style={'display': 'none'}),
                 html.Div(
                     id='negbinomial-parameters',
                     children=[
                         dbc.Input(id='nb-r', type='number', placeholder='R', step=0.1),
                         html.Br(),
                         dbc.Input(id='nb-p', type='number', placeholder='P', min=0, max=1, step=0.001),
                         html.Br()], style={'display': 'none'}),
                 html.Div(
                     id='exponential-parameters',
                     children=[
                         dbc.Input(id='e-a', type='number', placeholder='Alpha', step=0.001),
                         html.Br(),
                         html.Br()], style={'display': 'none'}),

                 html.Div(
                     id='poisson-parameters',
                     children=[
                         dbc.Input(id='p-l', type='number', placeholder='lambda'),
                         html.Br()], style={'display': 'none'})

             ], className='col-6', style={'padding':'30px'}),

    html.Br(),
    dbc.Label('Sample Size:'),
    dbc.Input(id='sample-size', type='number', placeholder='Sample size', step=1, style={'width': '50%'}),
    html.Br(),
    dbc.Button("Get Sample", id='btn-submit', color="primary", style={'width': '100%'}),
    html.Br(),

    html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        children=[
                            dbc.Label('Generated Sample Graph:'),
                            dcc.Graph(id='indicator-graphic'),
                        ],
                    )

                ),
                dbc.Col(
                    html.Div(
                        children=[
                            dbc.Label('Probability Density Function Graph:'),
                            dcc.Graph(id='pdf-graphic'),
                        ]
                    )
                ),
            ]
        ),
],className='container')

@app.callback(
    Output('normal-parameters', 'style'),
    Output('binomial-parameters', 'style'),
    Output('negbinomial-parameters', 'style'),
    Output('exponential-parameters', 'style'),
    Output('poisson-parameters', 'style'),
    Input(component_id='distribution-select', component_property='value')
)
def show_hide_element(distribution):
    if(distribution == 'normal'):
        return [{"display": 'block'}, {"display": 'none'},
                {"display": 'none'}, {"display": 'none'},
                {"display": 'none'}]
    elif (distribution == 'binomial'):
        return [{"display": 'none'}, {"display": 'block'},
                {"display": 'none'}, {"display": 'none'},
                {"display": 'none'}]
    elif (distribution == 'negbinomial'):
        return [{"display": 'none'}, {"display": 'none'},
                {"display": 'block'}, {"display": 'none'},
                {"display": 'none'}]
    elif (distribution == 'exponential'):
        return [{"display": 'none'}, {"display": 'none'},
                {"display": 'none'}, {"display": 'block'},
                {"display": 'none'}]
    elif(distribution == 'poisson'):
        return [{"display": 'none'}, {"display": 'none'},
                {"display": 'none'}, {"display": 'none'},
                {"display": 'block'}]

    return [{"display": 'none'}, {"display": 'none'},
            {"display": 'none'}, {"display": 'none'},
            {"display": 'none'}]


###########################################################
# NORMAL DISTRIBUTION
###########################################################
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('btn-submit', 'n_clicks'),
    State('distribution-select', 'value'),
    State('n-mean', 'value'),
    State('n-std', 'value'),
    State('b-r', 'value'),
    State('b-p', 'value'),
    State('nb-r', 'value'),
    State('nb-p', 'value'),
    State('e-a', 'value'),
    State('p-l', 'value'),
    State('sample-size', 'value'),
    prevent_initial_call=True
)
def show_sample_graph(n_clics, distribution, n_mean, n_std,
                   b_r, b_p, nb_r, nb_p, e_a, p_l, sample_size):
    if(distribution == 'normal'):
        fig = generate_plot(distribution, sample_size, {'mean': float(n_mean), 'std': int(n_std)})
        return fig
    elif (distribution == 'binomial'):
        fig = generate_plot(distribution, sample_size, {'n': int(b_r), 'p': float(b_p)})
        return fig
    elif (distribution == 'negbinomial'):
        fig = generate_plot(distribution, sample_size, {'r': int(nb_r), 'p': float(nb_p)})
        return fig
    elif (distribution == 'exponential'):
        fig = generate_plot(distribution, sample_size, {'a': float(e_a)})
        return fig
    elif(distribution == 'poisson'):
        fig = generate_plot(distribution, sample_size,{'l': int(p_l)})
        return fig

@app.callback(
    Output('pdf-graphic', 'figure'),
    Input('btn-submit', 'n_clicks'),
    State('distribution-select', 'value'),
    State('n-mean', 'value'),
    State('n-std', 'value'),
    State('b-r', 'value'),
    State('b-p', 'value'),
    State('nb-r', 'value'),
    State('nb-p', 'value'),
    State('e-a', 'value'),
    State('p-l', 'value'),
    State('sample-size', 'value'),
    prevent_initial_call=True
)
def show_pdf_graph(n_clics, distribution, n_mean, n_std,
                   b_r, b_p, nb_r, nb_p, e_a, p_l, sample_size):
    if(distribution == 'normal'):
        fig = generate_pdf(distribution, sample_size, {'mean': n_mean, 'std': n_std})
        return fig
    elif (distribution == 'binomial'):
        fig = generate_pdf(distribution, sample_size, {'n': b_r, 'p': b_p})
        return fig
    elif (distribution == 'negbinomial'):
        fig = generate_pdf(distribution, sample_size, {'r': nb_r, 'p': nb_p})
        return fig
    elif (distribution == 'exponential'):
        fig = generate_pdf(distribution, sample_size, {'a': e_a})
        return fig
    elif(distribution == 'poisson'):
        fig = generate_pdf(distribution, sample_size,{'l': p_l})
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)
