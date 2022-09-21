# 1. Library imports
import uvicorn
from fastapi import FastAPI
from HomeCredit import HomeCredit
import numpy as np
import joblib
import json

# https://www.maartengrootendorst.com/blog/deploy/

# 2. Create the app object
app = FastAPI()

# Initialize files
classifier = joblib.load("best_model_prototype.pickle")
print('Classifier: ', classifier)
enc = joblib.load('encoder.pickle')
features = joblib.load('features.pickle')


# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Welcome to the Credit Scoring API.'}

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {f'Hello {name}, welcome to the Credit Scoring API. We try to predict if you will be in default or not.'}


# 3. Expose the prediction functionality, make a prediction from the passed
#   JSON data and return the predicted HomeCredit score with the confidence
@app.post('/predict')
def predict_homecredit(data: HomeCredit):
    print("Starting prediction...")

    # Extract data in correct order
    # Store the data into a dictionary
    data = data.dict()

    # Defining the features from the loaded data
    CNT_CHILDREN = data['CNT_CHILDREN']
    AMT_INCOME_TOTAL = data['AMT_INCOME_TOTAL']
    AMT_CREDIT = data['AMT_CREDIT']
    DAYS_BIRTH = data['DAYS_BIRTH']
    EXT_SOURCE_2 = data['EXT_SOURCE_2']
    FLAG_PHONE = data['FLAG_PHONE']
    NAME_CONTRACT_TYPE = data['NAME_CONTRACT_TYPE']
    CODE_GENDER = data['CODE_GENDER']
    FLAG_OWN_CAR = data['FLAG_OWN_CAR']
    FLAG_OWN_REALTY = data['FLAG_OWN_REALTY']
    NAME_INCOME_TYPE = data['NAME_INCOME_TYPE']
    NAME_EDUCATION_TYPE = data['NAME_EDUCATION_TYPE']


    # Features with no preprocessing
    col_not_to_encode = ['CNT_CHILDREN','AMT_INCOME_TOTAL','AMT_CREDIT', 'DAYS_BIRTH', 'EXT_SOURCE_2', 'FLAG_PHONE']
    other_features = [data[feature] for feature in col_not_to_encode]

    # Apply one-hot encoding to categorical features
    col_to_encode = ['NAME_CONTRACT_TYPE', 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE']
    to_encode = [data[feature] for feature in col_to_encode]
    encoded_features = list(enc.transform(np.array(to_encode).reshape(1, -1))[0])

    # Store all the features for prediction
    to_predict = np.array(other_features + encoded_features)

    # Prediction with our trained model
    prediction = classifier.predict_proba(to_predict.reshape(1, -1))

    print(prediction)

    #The training application data comes with the TARGET indicating
    # 0: the loan was repaid => "Solvent client"
    # 1: the loan was not repaid. => "Insolvent client"


    return {
        'prediction': prediction
    }

#@app.post('/explain')
#def explain_score():



# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    #uvicorn.run(app, host='p7-fastapi.herokuapp.com')

    

# uvicorn app:app --reload
# uvicorn main:app --reload

# à déployer sur Heroku et récupérer URL