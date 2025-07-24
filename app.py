import sys
import os
import certifi
import pymongo
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.expection.expection import NetworkSecurityExpection
from NetworkSecurity.pipeline.traning_pipeline import Traning_pipeline
from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from NetworkSecurity.utils.main_utils.utils import load_object


ca=certifi.where()
from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)


client=pymongo.MongoClient(MONGO_DB_URL,tlsCAFile=ca)

from NetworkSecurity.constant.traning_pipeline import DATA_INGESION_DATABASE_NAME
from NetworkSecurity.constant.traning_pipeline import DATA_INGESION_COLLECTION_NAME

database=client[DATA_INGESION_DATABASE_NAME]
collection=database[DATA_INGESION_COLLECTION_NAME]
 
from fastapi.templating import Jinja2Templates
template=Jinja2Templates(directory='./template')


app=FastAPI()
origins=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*'],
)

@app.get('/',tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')


@app.get('/train')
async def train_route():
    try:
        traning_pipeline=Traning_pipeline()
        traning_pipeline.run_pipeline()
        return Response("Traning is sucessfull")
    except Exception as e:
        NetworkSecurityExpection(e,sys)

    
@app.post('/predict')
async def predict_route(request:Request,file:UploadFile=File(...)):
   try: 
    df=pd.read_csv(file.file)
    #print(df)
    preprocessor=load_object('final_model/preprocessor.pkl')
    model=load_object('final_model/model.pkl')
    network_model=NetworkModel(preprocessor=preprocessor,model=model)
    y_pred=network_model.predict(df)
    #print(df)
    df["predicted_column"]=y_pred
    df["predicted_column"].replace(-1,0)
    
    df.to_csv("predication_output/output.csv")
    table_html=df.to_html(classes='table table-striped')
    #print(table_html)
    return template.TemplateResponse("table.html",{"request":request,"table":table_html})
   
   except Exception as e:
      raise NetworkSecurityExpection(e,sys)




if __name__=='__main__':
    app_run(app,host="localhost",port=8000)

