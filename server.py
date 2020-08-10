import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
from sklearn.model_selection import train_test_split
from flask import Flask, request, jsonify
import json
import os.path

MY_MODEL_JOBLIB_FILENAME = 'my_modal.joblib'
regress = None

if os.path.isfile(MY_MODEL_JOBLIB_FILENAME):
    regress = joblib.load(MY_MODEL_JOBLIB_FILENAME)
else:
    data = pd.read_excel('dataset_train_test_3000.xlsx', sheet_name='Sheet1')
    regress = RandomForestRegressor(random_state=42, bootstrap=False, max_depth=40, max_features=2, min_samples_split=2,
                                    n_estimators=750, min_samples_leaf=1)
    result = np.array(data)

    X = []
    Y = []

    for index, value in enumerate(result):
        X.append(value[1:-1])
        Y.append(value[-1])

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.15, random_state=42)

    regress.fit(X_train, Y_train)

    joblib.dump(regress, MY_MODEL_JOBLIB_FILENAME)

app = Flask(__name__)

@app.route('/predict')
def do_prediction():
    predict_result = regress.predict(json.loads(request.form.to_dict()['data']))
    return jsonify(error=False, message='', data=predict_result.tolist())
