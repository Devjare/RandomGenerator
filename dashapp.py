import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State
import plotly.express as px

from dash_extensions.enrich import DashProxy, TriggerTransform, MultiplexerTransform, ServersideOutputTransform, NoOutputTransform

# app = DashProxy(transforms=[
#     TriggerTransform(),  # enable use of Trigger objects
#     MultiplexerTransform(),  # makes it possible to target an output multiple times in callbacks
#     ServersideOutputTransform(),  # enable use of ServersideOutput objects
#     NoOutputTransform(),  # enable callbacks without output
# ])


################################################
from DistributionFactory import DistributionFactory


################################################

#app = dash.Dash(__name__)
# app = dash.Dash(
#     external_stylesheets=[dbc.themes.BOOTSTRAP],
#     suppress_callback_exceptions=True
# )
app = DashProxy(transforms=[
    
    MultiplexerTransform(),  # makes it possible to target an output multiple times in callbacks
    
],external_stylesheets=[dbc.themes.BOOTSTRAP],)

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

        # html.Div([
        #     dcc.Dropdown(
        #         id='yaxis-column',
        #         options=[{'label': i, 'value': i} for i in available_indicators],
        #         value='Life expectancy at birth, total (years)'
        #     ),
            
        # ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    
    html.Br(),

    dbc.Label('Parameters:'),

    dbc.Card([
        html.Div(id='parameters-container'),

    ], className='col-6', style={'padding':'30px'}),

    html.Br(),
    dbc.Label('Output:'),

    dcc.Graph(id='indicator-graphic'),
],className='container')

@app.callback(
    Output('parameters-container', 'children'),
    Input('distribution-select', 'value')
)
def update_output(distribution):
    content = ''
    if distribution =='normal':
        content = html.Div([

            dbc.Input(id='n-mean', type='number', placeholder='Mean',step=0.1),
            html.Br(),
            dbc.Input(id='n-std', type='number', placeholder='Standard Deviation', step=0.1),
            html.Br(),
            dbc.Input(id='sample-size', type='number', placeholder='Sample size', step=1),
            html.Br(),
            dbc.Button("Get Sample", id='btn-submit', color="primary", style={'width':'100%'})
            
        ]),
    
    elif distribution =='binomial':
        content = html.Div([

            dbc.Input(id='b-n', type='number', placeholder='N',step=0.1),
            html.Br(),
            dbc.Input(id='b-p', type='number', placeholder='P', min=0, max=1, step=0.1),
            html.Br(),
            dbc.Input(id='sample-size', type='number', placeholder='Sample size', step=1),
            html.Br(),
            dbc.Button("Get Sample", id='btn-submit', color="primary", style={'width':'100%'})
            
        ]),
    
    elif distribution =='negbinomial':
        content = html.Div([

            dbc.Input(id='nb-r', type='number', placeholder='R',step=0.1),
            html.Br(),
            dbc.Input(id='nb-p', type='number', placeholder='P', min=0, max=1, step=0.1),
            html.Br(),
            dbc.Input(id='sample-size', type='number', placeholder='Sample size', step=1),
            html.Br(),
            dbc.Button("Get Sample", id='btn-submit', color="primary", style={'width':'100%'})
            
        ]),
        

    return content

def generate_plot(distribution, sample_size, params):
    x = []
    sample = []

    if distribution =='normal':
        try:
            distribution = DistributionFactory.get_distribution('normal', params)
            sample = distribution.get_sample(int(sample_size))
        except Exception as e:
            print({'status': 'failed', 'error': str(e)})
        
    elif distribution =='binomial':
        try:
            distribution = DistributionFactory.get_distribution('binomial', params)
            sample = distribution.get_sample(int(sample_size))
        except Exception as e:
            print({'status': 'failed', 'error': str(e)})
    
    elif distribution =='negbinomial':
        try:
            distribution = DistributionFactory.get_distribution('negativebinomial', params)
            sample = distribution.get_sample(int(sample_size))
        except Exception as e:
            print({'status': 'failed', 'error': str(e)})
    

    for i in range(len(sample)):
        x.append(i)
    
    #print(sample_size)
    #print(sample)

    fig = px.scatter(x=x,y=sample)

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


###########################################################
# NORMAL DISTRIBUTION
###########################################################
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('distribution-select', 'value'),
    
    Input('btn-submit', 'n_clicks'),

    State('n-mean', 'value'),
    State('n-std', 'value'),

    # [State('b-n', 'value'),
    # State('b-p', 'value'),],


    Input('sample-size', 'value'),
        prevent_initial_call=True
    )
def update_graph(distribution, _,sample_size, n_mean, n_std):

    print('Params')
    print(n_mean,' ', n_std,' ', sample_size)
    
    fig = generate_plot(distribution, sample_size,{'mean': n_mean, 'std': n_std})
    return fig


###########################################################
# BINOMIAL DISTRIBUTION
###########################################################
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('distribution-select', 'value'),
    
    Input('btn-submit', 'n_clicks'),

    State('b-n', 'value'),
    State('b-p', 'value'),

    Input('sample-size', 'value'),
        prevent_initial_call=True
    )
def update_graph(distribution, _, sample_size,b_n, b_p):
    print('Params')
    print(b_n,' ', b_p,' ', sample_size)

    fig = generate_plot(distribution, sample_size,{'n': b_n, 'p': b_p})
    return fig


###########################################################
# NEGATIVE BINOMIAL DISTRIBUTION
###########################################################
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('distribution-select', 'value'),
    
    Input('btn-submit', 'n_clicks'),

    State('nb-r', 'value'),
    State('nb-p', 'value'),

    Input('sample-size', 'value'),
        prevent_initial_call=True
    )
def update_graph(distribution, _, sample_size,nb_r, nb_p):
    print('Params')
    print(nb_r,' ', nb_p,' ', sample_size)

    fig = generate_plot(distribution, sample_size,{'r': int(nb_r), 'p': float(nb_p)})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)