from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    fuel_Diesel=0
    fuel_Electric=0
    fuel_LPG=0
    owner_second = 0
    owner_third = 0
    owner_forth = 0

    if request.method == 'POST':
        year = int(request.form['year'])
        km_driven=int(request.form['km_driven'])
        km_driven2=np.log(km_driven)
        owner_first = request.form['owner_first']
        if(owner_first=='first'):
            owner_first=1
            owner_second=0
            owner_third=0
            owner_forth=0
        elif(owner_first == 'second'):
            owner_first = 0
            owner_second = 1
            owner_third = 0
            owner_forth = 0
        elif(owner_first == 'third'):
            owner_first = 0
            owner_second = 0
            owner_third = 1
            owner_forth = 0
        else:
            owner_first = 0
            owner_second = 0
            owner_third = 0
            owner_forth = 1
        fuel_Petrol = request.form['fuel_Petrol']
        if (fuel_Petrol == 'Petrol'):
            fuel_Petrol = 1
            fuel_Diesel = 0
            fuel_Electric = 0
            fuel_LPG = 0
        elif(fuel_Petrol=='Diesel'):
            fuel_Petrol = 0
            fuel_Diesel = 1
            fuel_Electric = 0
            fuel_LPG = 0
        elif (fuel_Petrol=='Electric'):
            fuel_Petrol = 0
            fuel_Diesel = 0
            fuel_Electric = 1
            fuel_LPG = 0
        else:
            fuel_Petrol = 0
            fuel_Diesel = 0
            fuel_Electric = 0
            fuel_LPG = 1
        seller_type_individual=request.form['seller_type_individual']
        if(seller_type_individual=='individual'):
            seller_type_individual=1
        else:
            seller_type_individual=0
        transmission_Mannual=request.form['transmission_Mannual']
        if(transmission_Mannual=='Mannual'):
            transmission_Mannual=1
        else:
            transmission_Mannual=0
        prediction=model.predict([[km_driven2,owner_first,owner_second,owner_third,owner_forth,year,fuel_Petrol,fuel_Diesel,fuel_Electric,fuel_LPG,seller_type_individual,transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
