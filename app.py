import sys
import os
import certifi
import pymongo
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.expection.expection import NetworkSecurityExpection
from NetworkSecurity.pipeline.traning_pipeline import Traning_pipeline
from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi import Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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
templates = Jinja2Templates(directory="template")

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
    return templates.TemplateResponse("table.html",{"request":request,"table":table_html})
   
   except Exception as e:
      raise NetworkSecurityExpection(e,sys)
   

@app.post('/predict_ui', tags=["ui"])
async def predict_ui(
    request: Request,
    having_IP_Address: int = Form(...),
    URL_Length: int = Form(...),
    Shortining_Service: int = Form(...),
    having_At_Symbol: int = Form(...),
    double_slash_redirecting: int = Form(...),
    Prefix_Suffix: int = Form(...),
    having_Sub_Domain: int = Form(...),
    SSLfinal_State: int = Form(...),
    Domain_registeration_length: int = Form(...),
    Favicon: int = Form(...),
    port: int = Form(...),
    HTTPS_token: int = Form(...),
    Request_URL: int = Form(...),
    URL_of_Anchor: int = Form(...),
    Links_in_tags: int = Form(...),
    SFH: int = Form(...),
    Submitting_to_email: int = Form(...),
    Abnormal_URL: int = Form(...),
    Redirect: int = Form(...),
    on_mouseover: int = Form(...),
    RightClick: int = Form(...),
    popUpWidnow: int = Form(...),
    Iframe: int = Form(...),
    age_of_domain: int = Form(...),
    DNSRecord: int = Form(...),
    web_traffic: int = Form(...),
    Page_Rank: int = Form(...),
    Google_Index: int = Form(...),
    Links_pointing_to_page: int = Form(...),
    Statistical_report: int = Form(...)
):
    try:
        features = [[
            having_IP_Address, URL_Length, Shortining_Service,
            having_At_Symbol, double_slash_redirecting, Prefix_Suffix,
            having_Sub_Domain, SSLfinal_State, Domain_registeration_length,
            Favicon, port, HTTPS_token, Request_URL, URL_of_Anchor,
            Links_in_tags, SFH, Submitting_to_email, Abnormal_URL, Redirect,
            on_mouseover, RightClick, popUpWidnow, Iframe, age_of_domain,
            DNSRecord, web_traffic, Page_Rank, Google_Index,
            Links_pointing_to_page, Statistical_report
        ]]

        preprocessor = load_object('final_model/preprocessor.pkl')
        model = load_object('final_model/model.pkl')

        network_model = NetworkModel(preprocessor=preprocessor, model=model)
        prediction = network_model.predict(features)[0]

        label = "⚠️ Phishing Detected" if prediction == 1 else "✅ Legitimate Website"
        return templates.TemplateResponse("result.html", {"request": request, "result": label})
    
    except Exception as e:
        raise NetworkSecurityExpection(e, sys)
    
@app.get("/", response_class=HTMLResponse)
@app.get("/form", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})




if __name__=='__main__':
    app_run(app,host="localhost",port=8000)

