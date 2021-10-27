import base64
import pandas as pd
from flask import Blueprint, request
from flask.templating import render_template
from io import BytesIO
from matplotlib.figure import Figure
from data import load_data
from utils import clf_dict

dashboard = Blueprint('dashboard', __name__)

df = load_data()
df_setosa = df.loc[df['target'] == 0]
df_versicolor = df.loc[df['target'] == 1]
df_virginica = df.loc[df['target'] == 2]
df_list = [df_setosa, df_versicolor, df_virginica]

@dashboard.route('/')
def show_dashboard():
    return render_template('dashboard.html')


@dashboard.route('/multivariate', methods=['POST', 'GET'])
def show_plot():
    if request.method == 'POST':
        if 'show_plot' in request.form:
            # Get selected features
            feat_1 = request.form['feature_1'].replace('_', ' ') + ' (cm)'
            feat_2 = request.form['feature_2'].replace('_', ' ') + ' (cm)'

            # Create plot
            fig = Figure()
            ax = fig.subplots()
            for i, df in enumerate(df_list):
                ax.scatter(df.loc[:, feat_1], df.loc[:, feat_2], label=clf_dict[i])
            ax.set_title('Iris Data Scatterplot')
            ax.set_xlabel(feat_1)
            ax.set_ylabel(feat_2)
            ax.legend()
            for spine in ax.spines:
                ax.spines[spine].set_visible(False)

            # Save and encode plot
            buf = BytesIO()
            fig.savefig(buf, format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return render_template('dashboard.html', plot=data, plot_type='multivariate')
        else:
             return render_template('dashboard.html', plot_type='multivariate')

@dashboard.route('/univariate', methods=['POST', 'GET'])
def show_univariate():
    if request.method == 'GET':
        return render_template('dashboard.html', plot_type='univariate')
    else:
        if 'show_plot' in request.form:
            # Get selected features
            feat = request.form['feature_1'].replace('_', ' ') + ' (cm)'

            # Create plot
            fig = Figure()
            ax = fig.subplots()
            for i, df in enumerate(df_list):
                ax.hist(df.loc[:, feat], label=clf_dict[i], alpha=0.7)
            
            ax.set_title('Iris Data Histogram')
            ax.set_xlabel(feat)
            ax.legend()
            for spine in ax.spines:
                ax.spines[spine].set_visible(False)
            # Save and encode plot
            buf = BytesIO()
            fig.savefig(buf, format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return render_template('dashboard.html', plot=data, plot_type='univariate')
        else:
             return render_template('dashboard.html', plot_type='univariate')