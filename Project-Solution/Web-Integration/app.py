import numpy as np
import pandas as pd
from flask import Flask,render_template,request
app = Flask(__name__)
import pickle

model = pickle.load(open("Prediction.pkl","rb"))

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
    output = model.predict(test)
    if(output[0] == 1):
        output="Placed"
    else:
        output="Not placed"
    print(output)
    return render_template('index.html',y="Predicted Profit: "+output)

if __name__ == '__main__':
    app.run()
