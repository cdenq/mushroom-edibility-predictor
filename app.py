#imports
from flask import Flask, render_template, redirect, jsonify, request
import predict

#create flask instance
app = Flask(__name__, static_url_path='/static')

# Set root route
@app.route('/')
def index():
    return render_template('index.html')

# Set root route
@app.route('/input')
def input():
    return render_template('index.html')

#route for predicting from user input
@app.route('/predict', methods = ['POST'])
def prediction():
    predict_list = request.get_json()
    data = predict.make_predictions(predict_list)
    return jsonify(data)

#route for mushroom eda page
@app.route('/mushroom_facts')
def facts():
    return render_template('mushroom_facts.html')

#route for page about comparing ML models
@app.route('/compare_models')
def models():
    return render_template('compare_models.html')

@app.route('/eda_stats')
def edastats():
    return render_template('eda_stats.html')

@app.route('/eda_color')
def edacolor():
    return render_template('eda_color.html')

#route for about page
@app.route('/about')
def about():
    return render_template('about.html')
   
if __name__ == "__main__":
    app.run(debug=True)