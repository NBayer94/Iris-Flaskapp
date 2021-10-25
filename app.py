from flask import Flask, render_template, request, redirect, sessions, url_for, session

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/prediction', methods=['POST', 'GET'])
def prediction():
    if request.method == 'POST':
        feat_1 = request.form['feat_1']
        feat_2 = request.form['feat_2']
        session['feat_1'] = feat_1
        session['feat_2'] = feat_2
        return redirect(url_for('result'))
    if request.method == 'GET':
        return render_template('prediction.html')

@app.route('/result')
def result():
    return render_template('result.html', name=session['feat_1'])

if __name__ == '__main__':
    app.run(port=3000, debug=True)