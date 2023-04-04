import joblib
import os
from main_preprocessing import preprocessing
import supervised_ml
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

initial_data = preprocessing()[0]

def make_predictions(data):

    model_results = {'amodelName': [],
                    'bmodelPrediction': [],
                    'cmodelAccuracy': [],
                    'dmodelF1': [],
                    'emodelPrecision': [],
                    'fmodelRecall': []}
  
    data['cap-diameter'] = float(data['cap-diameter'])
    data['stem-height'] = float(data['stem-height'])
    data['stem-width'] = float(data['stem-width'])

    input_df = pd.DataFrame(data, index=[0])
    input_dummies = pd.get_dummies(input_df)

    merged_df = initial_data.merge(input_dummies, how = 'outer')
    merged_df.fillna(0.0, inplace = True)
    input_data = merged_df.iloc[1, :].values

    scaler = StandardScaler()
    X_train = preprocessing()[1]
    scaler.fit(X_train)
    scaled_input_data = scaler.transform([input_data])

    for index, file in enumerate(os.listdir('static/models/')):
        filename = os.fsdecode(file)
        model_list = ['Extremely Random Forest', 'K-Nearest Neighbor', 'Logistic Regression', 'Random Forest Classifier', 'SVM']
        model = joblib.load('Main/Resources/Models/' + filename)
        prediction = model.predict(scaled_input_data)
        model_scores = supervised_ml.model_score(model)
        model_scores = [float(score) for score in model_scores]
        model_results['amodelName'].append(model_list[index])
        model_results['bmodelPrediction'].append(float(prediction[0]))
        model_results['cmodelAccuracy'].append(model_scores[0])
        model_results['dmodelF1'].append(model_scores[1])
        model_results['emodelPrecision'].append(model_scores[2])
        model_results['fmodelRecall'].append(model_scores[3])
    return model_results