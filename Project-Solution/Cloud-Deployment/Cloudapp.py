import numpy as np
import pandas as pd
from flask import Flask,render_template,request
app = Flask(__name__)

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "YHDJcF33s3v8NO0E7-18A3aoCISM6BC7NB4C0qfFF2YQ"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/login',methods=['POST'])
def login():
    i1 = request.form['sscp']
    i2 = request.form['dgp']
    i3 = request.form['hscp']
    i4 = request.form['mbap']
    i5 = request.form['spc']
    if(i5 == 'Mkt&HR'):
        i5=1
    else:
        i5=0
    
    test = [[int(i1),int(i2),int(i3),int(i4),int(i5)]]

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": [[int(i1),int(i2),int(i3),int(i5),int(i4)]], "values": test}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b728d70c-2c60-4740-a34c-58164628f288/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring)
    predictions = response_scoring.json()
    output = predictions['predictions'][0]['values'][0][0]
    print('Final Prediction:',output)

    print(output)

    if(output == 1):
        output="Placed"
    else:
        output="Not placed"
    print(output)

    return render_template('index.html',y="This Result is from IBM Cloud-Predicted Placement: "+str(output))

if __name__ == '__main__':
    app.run()
