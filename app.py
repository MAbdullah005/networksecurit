from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import pandas as pd
from fastapi.templating import Jinja2Templates
import numpy as np
import joblib
from predication_output.feature_extraction import extract_features

app = FastAPI()
templates = Jinja2Templates(directory="template")  # Make sure folder is named correctly: "template", not "templates"

# Load trained model
try:
    preprocessor = joblib.load('final_model/preprocessor.pkl')
    model = joblib.load('final_model/model.pkl') # Assuming you have saved your model
except FileNotFoundError as e:
    print(f"Error: Missing model or preprocessor file. Please check the path. {e}")
    preprocessor, model = None, None
    
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
def predict(request: Request, url: str = Form(...)):
    try:
        if not model or not preprocessor:
          print("Model or preprocessor not loaded.")
          return None
        

        feature_names = [
        'having_IP_Address', 'URL_Length', 'Shortining_Service', 'having_At_Symbol', 'double_slash_redirecting',
        'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State', 'Domain_registeration_length', 'Favicon',
        'port', 'HTTPS_token', 'Request_URL', 'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Submitting_to_email',
        'Abnormal_URL', 'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain',
        'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page', 'Statistical_report'
        ]

        features_dict = extract_features(url)
    
    # Order the features correctly and convert to a 2D array
        ordered_features = pd.DataFrame([features_dict], columns=feature_names)

        #ordered_features = pd.DataFrame([features_dict[name] for name in feature_names])
    
    # Apply the preprocessor (imputer) to the ordered features
        imputed_features = preprocessor.transform(ordered_features)
    
    # Make the final prediction
        prediction = model.predict(imputed_features)[0]
        print("Predication ==",prediction,"--url is== ",url)


        if prediction == 1 or prediction == 1.0:
           result = "🚨 Phishing (Bad URL)"
        else:
           print("predication--",prediction)
           result = "✅ Legitimate (Good URL)"

        return templates.TemplateResponse("index.html", {"request": request, "result": result})

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": f"❌ Error during prediction: {str(e)}"
        })
