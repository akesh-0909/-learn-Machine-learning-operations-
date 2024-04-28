from flask import Flask, request,render_template, url_for
import numpy as np
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.pipeline.predict_pipeline import CustomData,PredictPipeline

application = Flask(__name__)

app = application

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(e)
        raise CustomException(e)

@app.route('/predictdata',methods = ['GET','POST'])
def predictdatapoint():
    try:
        if request.method == "GET":
            return render_template('home.html')
        else:
            data = CustomData(
                gender = request.form.get("gender"),
                parental_level_of_education= request.form.get('parental_level_of_education'),
                race_ethnicity= request.form.get('ethnicity'),
                lunch= request.form.get('lunch'),
                test_preparation_course= request.form.get('test_preparation_course'),
                reading_score= float(request.form.get('reading_score')),
                writing_score= float(request.form.get('writing_score'))
                        
                
            )
            pred_df = data.get_data_as_dataframe()
            print(pred_df)
            prediction_pipeline = PredictPipeline(pred_df)
            results = prediction_pipeline.predict()
            print("results::",results)
            return render_template('home.html',results = results[0])
    except Exception as e:
        logging.error(e)
        raise CustomException(e)

if __name__== "__main__":
    app.run(host = '0.0.0.0',debug=True,port='5000')