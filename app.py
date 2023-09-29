import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from Models import black_scholes_option, european_option_crr

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Mise en page de l'interface utilisateur
app.layout = html.Div(
    children=[
        html.H1("Comparaison des Modèles: BSM et CRR", style={'textAlign': 'center', 'color': 'black'}),
        
        # Choix du modèle
        html.Div(
            children=[
                html.Label("Choisissez le modèle :", style={'color': 'black'}),
                dcc.Dropdown(
                    id='dropdown-model',
                    options=[
                        {'label': 'Black-Scholes-Merton (BSM)', 'value': 'BSM'},
                        {'label': 'Modèle Binomial Cox-Ross-Rubinstein (CRR)', 'value': 'CRR'}
                    ],
                    value='BSM',
                ),
            ],
            style={'marginBottom': '20px'}
        ),
        
        # Type d'option
        html.Div(
            children=[
                html.Label("Choisissez le type d'option :", style={'color': 'black'}),
                dcc.Dropdown(
                    id='dropdown-option-type',
                    options=[
                        {'label': 'Call', 'value': 'call'},
                        {'label': 'Put', 'value': 'put'}
                    ],
                    value='call',
                ),
            ],
            style={'marginBottom': '20px'}
        ),

        # Paramètres d'entrée
        html.Div(
            children=[
                html.Div([
                    html.Label("Prix de l'actif sous-jacent (S) :", style={'color': 'black'}),
                    dcc.Input(id='input-s', type='number', value=100, className='input-field'),
                ], style={'marginBottom': '20px'}),
                
                html.Div([
                    html.Label("Prix d'exercice (K) :", style={'color': 'black'}),
                    dcc.Input(id='input-k', type='number', value=100, className='input-field'),
                ], style={'marginBottom': '20px'}),
                
                html.Div([
                    html.Label("Durée jusqu'à l'échéance (T ans) :", style={'color': 'black'}),
                    dcc.Input(id='input-t', type='number', value=1, className='input-field'),
                ], style={'marginBottom': '20px'}),
                
                html.Div([
                    html.Label("Taux d'intérêt (r) :", style={'color': 'black'}),
                    dcc.Input(id='input-r', type='number', value=0.05, className='input-field'),
                ], style={'marginBottom': '20px'}),
                
                html.Div([
                    html.Label("Volatilité (sigma) :", style={'color': 'black'}),
                    dcc.Input(id='input-sigma', type='number', value=0.2, className='input-field'),
                ], style={'marginBottom': '20px'}),
                
                html.Div([
                    html.Label("Nombre d'étapes (n) :", style={'color': 'black'}),
                    dcc.Input(id='input-n', type='number', value=100, className='input-field'),
                ], style={'marginBottom': '20px', 'display': 'none'}, id='div-input-n'),
            ],
            style={'textAlign': 'left', 'marginBottom': '20px'}
        ),
        
        # Résultat
        html.Div(id='output-text', style={'textAlign': 'center', 'fontSize': '18px', 'fontWeight': 'bold'}),
    ],
    style={'maxWidth': '400px', 'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc', 'borderRadius': '10px'}
)

# Définition des callbacks
@app.callback(
    [Output('output-text', 'children'),
     Output('div-input-n', 'style')],
    [Input('input-s', 'value'),
     Input('input-k', 'value'),
     Input('input-t', 'value'),
     Input('input-r', 'value'),
     Input('input-sigma', 'value'),
     Input('input-n', 'value'),
     Input('dropdown-model', 'value'),
     Input('dropdown-option-type', 'value')]
)
def update_output_text(S, K, T, r, sigma, n, model, option_type):
    if model == 'BSM':
        option_price = black_scholes_option(S, K, T, r, sigma, option_type)
        style_input_n = {'display': 'none'}
    elif model == 'CRR':
        option_price = european_option_crr(S, K, T, r, sigma, n, option_type)
        style_input_n = {'marginBottom': '20px'}
    else:
        option_price = None
        style_input_n = {'display': 'none'}
    
    return [f"Le prix de l'option est : {option_price:.4f}", style_input_n]

# Exécution de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
