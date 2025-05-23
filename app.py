import pickle
import os
import numpy as np
import pandas as pd
from flask import Flask,redirect,url_for,render_template,request,jsonify
 

app=Flask(__name__)
scalar=pickle.load(open('scaling.pkl','rb'))
regmodel = pickle.load(open('regressionModel.pkl','rb'))


@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')

@app.route('/predict_api', methods=['POST'])
def predict_Api():
    data = request.json['data']
    print(data)
    
    # Convert input to numpy array
    input_array = np.array(list(data.values())).reshape(1, -1)
    
    # Apply scaling
    new_data = scalar.transform(input_array)
    
    # Predict
    output = regmodel.predict(new_data)
    
    # Convert to native float and return as JSON
    return jsonify({'prediction': float(output[0])})






if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)