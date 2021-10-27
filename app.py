import numpy as np
from flask import Flask, render_template, request, redirect, sessions, url_for, session
from data import load_data
from utils import clf_dict, load_model
from dashboard import dashboard

app = Flask(__name__)
app.secret_key = 'secret'

# Register dashboard blueprint
app.register_blueprint(dashboard, url_prefix='/dashboard')

# Load model and data
data = load_data()
model = load_model()


# Index route
@app.route('/')
def index():
    return render_template('base.html')

# Route for prediction
@app.route('/prediction', methods=['POST', 'GET'])
def get_prediction():
    if request.method == 'POST':
        session['sepal_width'] = float(request.form['sepal_width'])
        session['sepal_length'] = float(request.form['sepal_length'])
        session['petal_width'] = float(request.form['petal_width'])
        session['petal_length'] = float(request.form['petal_length'])
        return redirect(url_for('show_result'))
    if request.method == 'GET':
        return render_template('prediction.html')

# Route for result
@app.route('/result')
def show_result():
    x = np.array([[session['sepal_width'], session['sepal_length'], session['petal_width'], session['petal_length']]])
    y_pred = model.predict(x)[0]
    prediction = clf_dict[y_pred]
    return render_template('result.html', prediction=prediction)

#Route for data
@app.route('/data', methods=['GET', 'POST'])
def show_data():
    if request.method == 'GET':
        return render_template('data.html', tables=[data.to_html()], feature="sepal_length", lower="4", upper="4")
    if request.method == 'POST':
        feature = request.form['feature']
        feature_processed = request.form['feature'].replace('_', ' ') + ' (cm)'
        upper = float(request.form['upper'])
        lower = float(request.form['lower'])

        df = data.loc[(data[feature_processed] <= upper) & (data[feature_processed] >= lower)]
        return render_template('data.html', tables=[df.to_html()], feature=feature, upper=upper, lower=lower, filtered=True)

if __name__ == '__main__':
    app.run(port=3000, debug=True)