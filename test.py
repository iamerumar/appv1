import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash.exceptions
import base64
import io
import seaborn as sns
import matplotlib.pyplot as plt
import os
import tempfile
import subprocess
import pandas as pd

# Initialize the Dash app with the JOURNAL theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

# Create a Flask server to run Seaborn separately
from flask import Flask
server = Flask(__name__)

@server.route('/seaborn', methods=['GET'])
def run_seaborn():
    try:
        # Load your dataset or generate sample data
        df = sns.load_dataset("iris")

        # Create a temporary directory to save Seaborn plots
        temp_dir = tempfile.mkdtemp()
        os.chdir(temp_dir)

        # Create and save Seaborn plots
        sns.set(style="whitegrid")

        # Pair Plot
        pairplot = sns.pairplot(df, hue="species")
        pairplot.savefig("pairplot.png")

        # Box Plot
        boxplot = sns.boxplot(data=df, x="species", y="sepal_width")
        boxplot.get_figure().savefig("boxplot.png")

        # Violin Plot
        violinplot = sns.violinplot(data=df, x="species", y="sepal_width")
        violinplot.get_figure().savefig("violinplot.png")

        # KDE Plot
        kdeplot = sns.kdeplot(data=df, x="sepal_width", hue="species", fill=True)
        kdeplot.get_figure().savefig("kdeplot.png")

        # Save plots in the temp directory
        pairplot.savefig("pairplot.png")
        boxplot.get_figure().savefig("boxplot.png")
        violinplot.get_figure().savefig("violinplot.png")
        kdeplot.get_figure().savefig("kdeplot.png")

        # Close Seaborn figures
        plt.close(pairplot.fig)
        plt.close(boxplot.get_figure())
        plt.close(violinplot.get_figure())
        plt.close(kdeplot.get_figure())

        return 'Seaborn plots saved in the temp directory'

    except Exception as e:
        return str(e)

# Define the layout of the app
app.layout = dbc.Container([
    html.H1('Seaborn Visualization', style={'textAlign': 'center'}),
    dcc.Graph(id='visualization'),
    html.Button('Generate Seaborn Plots', id='generate-seaborn-button', n_clicks=0),
])

@app.callback(
    Output('visualization', 'figure'),
    Input('generate-seaborn-button', 'n_clicks')
)
def update_seaborn_plots(n_clicks):
    if n_clicks == 0:
        return {}
    else:
        # Start Seaborn visualization in a separate process
        subprocess.Popen(['python', 'your_seaborn_script.py'])

# Parses the dataset (if needed)
def parse_data(contents):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    return df

if __name__ == '__main__':
    # Run the Dash app with the Flask server
    server.run(host='0.0.0.0', port=8050, debug=True)
