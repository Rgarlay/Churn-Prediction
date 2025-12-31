
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os,sys

import pandas as pd
import numpy as np

from uvicorn import run as app_run
#from src.pipelines.training_pipeline import TrainingPipeline
from src.utils.utils import load_pickle_file, df_transform
from src.utils.ml_utils.eval_models import ChurnModel
from src.constants.training_pipeline import DATA_TRANSFORMATION_FEATURE_MAPPING

app = FastAPI()

# Point to templates folder
templates = Jinja2Templates(directory="templates")
# Home route - shows the form

model = load_pickle_file('final_obj/model.pkl')
preprocessor = load_pickle_file('final_obj/preprocessor.pkl')

@app.get("/")
def index():
    return f'This is the first page'

# @app.get("/train")
# async def train_route():
#     training_pipeline = TrainingPipeline()
#     training_pipeline.run_pipeline()
#     return f"Tranining has finished"
    
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    age: int = Form(...),
    subscription_type: str = Form(...),
    num_subscription_pauses: int = Form(...),
    customer_service_inquiries: str = Form(...),
    weekly_hours: float = Form(...),
    song_skip_rate: float = Form(...),
    num_platform_friends: int = Form(...),
    num_shared_playlists: int = Form(...),
    notifications_clicked: int = Form(...)
):

    df = pd.DataFrame([{
        'age': age,
        'subscription_type': subscription_type,
        'num_subscription_pauses': num_subscription_pauses,
        'customer_service_inquiries': customer_service_inquiries,
        'weekly_hours': weekly_hours,
        'song_skip_rate': song_skip_rate,
        'num_platform_friends': num_platform_friends,
        'num_shared_playlists': num_shared_playlists,
        'notifications_clicked': notifications_clicked
    }])

    df = df_transform(x = df, mapping=DATA_TRANSFORMATION_FEATURE_MAPPING)

    churn_model = ChurnModel(
        model=model,
        processor=preprocessor
    )

    prediction = churn_model.predict(df)

    if int(prediction) == 0:
        answer = "The user will churn"
    else:
        answer = "The user will not churn"

    return templates.TemplateResponse(
        "prediction.html",
        {
            "request": request,
            "answer": answer
        }
    )

if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)
