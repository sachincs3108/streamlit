import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    # Left Pane (Output Section)
    html.Div([
        html.H2("Financial Metrics and DCF Results"),
        html.Div(id="output-section", children=[
            html.P("Current PE: "),
            html.P("FY23 PE: "),
            html.P("5-Year Median RoCE: "),
            html.P("Compounded Sales Growth (TTM, 3Y, 5Y, 10Y): "),
            html.P("Compounded Profit Growth (TTM, 3Y, 5Y, 10Y): "),
            html.P("Calculated Intrinsic PE: "),
            html.P("Degree of Overvaluation: "),
        ]),
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '20px', 'vertical-align': 'top'}),
    
    # Right Pane (Input Section)
    html.Div([
        html.H2("DCF Parameters"),
        
        # Input fields
        html.Label("Enter NSE/BSE Symbol:"),
        dcc.Input(id="symbol-input", type="text", placeholder="e.g., NESTLEIND"),
        
        html.Label("Cost of Capital (%):"),
        dcc.Input(id="cost-of-capital", type="number", min=0, max=20, step=0.1, placeholder="e.g., 10"),
        
        html.Label("RoCE (%):"),
        dcc.Input(id="roce-input", type="number", min=0, max=100, step=0.1, placeholder="e.g., 20"),
        
        html.Label("Growth Rate during High Growth Period (%):"),
        dcc.Input(id="growth-rate", type="number", min=0, max=30, step=0.1, placeholder="e.g., 15"),
        
        html.Label("High Growth Period (years):"),
        dcc.Input(id="high-growth-period", type="number", min=1, max=30, step=1, placeholder="e.g., 15"),
        
        html.Label("Fade Period (years):"),
        dcc.Input(id="fade-period", type="number", min=1, max=30, step=1, placeholder="e.g., 15"),
        
        html.Label("Terminal Growth Rate (%):"),
        dcc.Input(id="terminal-growth-rate", type="number", min=0, max=10, step=0.1, placeholder="e.g., 3"),
        
        # Button to trigger computation
        html.Button("Calculate", id="calculate-button", n_clicks=0),
    ], style={'width': '40%', 'display': 'inline-block', 'padding': '20px'}),
])

# Callback for updating output based on inputs
@app.callback(
    Output("output-section", "children"),
    Input("calculate-button", "n_clicks"),
    # Additional Input components from user inputs can be added here
)
def update_output(n_clicks):
    # Placeholder for the function that processes inputs and returns financial metrics
    if n_clicks > 0:
        return [
            html.P(f"Current PE: {current_pe}"),
            html.P(f"FY23 PE: {fy23_pe}"),
            html.P(f"5-Year Median RoCE: {roce_5y_median}"),
            html.P(f"Compounded Sales Growth (TTM, 3Y, 5Y, 10Y): {sales_growth_rates}"),
            html.P(f"Compounded Profit Growth (TTM, 3Y, 5Y, 10Y): {profit_growth_rates}"),
            html.P(f"Calculated Intrinsic PE: {intrinsic_pe}"),
            html.P(f"Degree of Overvaluation: {degree_overvaluation}"),
        ]
    return "Please enter inputs and click Calculate"

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
